from __future__ import annotations

import colorsys
from functools import singledispatchmethod
from typing import Optional, List, Iterable, Tuple

import numpy as np
import vtk
from PIL import Image

from src.utils.getpixel import sample_image_colors
from .point_cloud_conversions import color_list_to_vtk_polydata, vtk_polydata_to_file, file_to_vtk_polydata
from .type import PointColor, MaskPointColor, ColorList


def calculate_point_coordinates(color: PointColor, sphere_radius: int) -> MaskPointColor:
    """
    根据 RGB 颜色计算点的三维坐标。

    :param color: RGB 颜色值，范围为 0-255。
    :param sphere_radius: 球体的半径，用于缩放坐标。
    :return: 计算出的三维坐标 (x, y, z)。
    """
    # 将 RGB 转换为 HLS (色相、亮度、饱和度)
    r, g, b = color
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    h_rad = h * 2 * np.pi  # 将色相转换为弧度

    # 计算 Z 坐标，以亮度为基准
    z = 2 * (l - 0.5) * sphere_radius
    # 计算 X 和 Y 坐标，使用饱和度和色相角度
    m = np.sqrt(1 - np.square(2 * (l - 0.5))) * s
    x = m * np.sin(h_rad) * sphere_radius
    y = m * np.cos(h_rad) * sphere_radius

    return x, y, z


class PointCloudActor:
    def __init__(self, color_point_cloud: ColorPointCloud, sphere_radius: int):
        """
        生成和管理点云数据。

        :param color_point_cloud: 管理此点云的 ColorPointCloud 对象。
        :param sphere_radius: 点云球体的半径，用于计算坐标。
        """
        self.color_point_cloud = color_point_cloud
        self.sphere_radius = sphere_radius
        self.image: Optional[Image] = None  # 保存输入的图像
        self.sample_count: Optional[int] = None  # 采样点数量
        self.mask_cloud_actor: Optional[MaskPointColor] = None  # 掩码颜色

        # 初始化 VTK 点和颜色数组
        self.vtk_points = vtk.vtkPoints()
        self.vtk_colors = vtk.vtkUnsignedCharArray()
        self.vtk_colors.SetNumberOfComponents(3)  # 设置颜色数组的分量数（RGB）
        self.vtk_colors.SetName("Colors")  # 命名颜色数组

        # 初始化 PolyData，用于存储点和颜色数据
        self.polydata = vtk.vtkPolyData()
        self.polydata.SetPoints(self.vtk_points)
        self.polydata.GetPointData().SetScalars(self.vtk_colors)

        # 初始化顶点过滤器，用于将点映射为顶点
        self.vertex_filter = vtk.vtkVertexGlyphFilter()
        self.vertex_filter.SetInputData(self.polydata)

        # 初始化 Mapper 和 Actor，用于将数据渲染到屏幕上
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.vertex_filter.GetOutputPort())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

    @singledispatchmethod
    def set_image(self, image: Image, sample_count: int = None):
        """
        设置输入图像，并根据采样点数量生成点云。

        :param image: 输入的 PIL 图像。
        :param sample_count: 采样点数量，默认为 None 使用当前设定值。
        """
        assert isinstance(image, Image.Image), "输入图像必须是 PIL.Image.Image 对象"
        self.image = image
        if sample_count is not None:
            self.sample_count = sample_count
        self._generate_point_cloud()  # 生成点云

    @set_image.register
    def _(self, image: str, sample_count: int = None):
        """
        设置输入图像文件路径，并根据采样点数量生成点云。

        :param image: 输入的图像文件路径。
        :param sample_count: 采样点数量，默认为 None 使用当前设定值。
        """
        assert isinstance(image, str), "输入图像必须是文件路径"
        self.image = Image.open(image)
        if sample_count is not None:
            self.sample_count = sample_count
        self._generate_point_cloud()

    def set_sample_count(self, sample_count: int):
        """
        设置采样点数量，并重新生成点云。

        :param sample_count: 采样点数量。
        """
        self.sample_count = sample_count
        if self.image:
            self._generate_point_cloud()  # 如果图像存在，重新生成点云

    def set_color_list(self, color_list: ColorList):
        """
        根据提供的颜色列表设置点云。

        :param color_list: 颜色列表，包含 RGB 颜色值。
        """
        vtk_polydata = color_list_to_vtk_polydata(color_list)  # 将颜色列表转换为 VTK 格式
        self.set_vtk_polydata(vtk_polydata)

    def set_mask_cloud_actor(self, color: MaskPointColor):
        """
        设置点云的掩码颜色。

        :param color: 掩码颜色。
        """
        self.mask_cloud_actor = color
        self._apply_mask_color()  # 应用掩码颜色

    def set_vtk_polydata(self, polydata: vtk.vtkPolyData, copy: bool = False):
        """
        设置 VTK 的点云数据。

        :param polydata: VTK 点云数据。
        :param copy: 是否复制数据，默认为 False。
        """
        if copy:
            new_polydata = vtk.vtkPolyData()
            new_polydata.ShallowCopy(polydata)
        else:
            new_polydata = polydata
        self.polydata = new_polydata
        self.vtk_points = new_polydata.GetPoints()
        self.vtk_colors = new_polydata.GetPointData().GetScalars()
        self.vertex_filter.SetInputData(new_polydata)

        assert self.vtk_points is not None, "VTK 点数据为空"
        assert self.vtk_colors is not None, "VTK 颜色数据为空"
        assert self.vtk_colors.GetNumberOfTuples() == self.vtk_points.GetNumberOfPoints(), "点和颜色数量不匹配"

        if self.mask_cloud_actor is not None:
            self._apply_mask_color()  # 应用掩码颜色
            return  # self._apply_mask_color()有self.update()方法

        self.update()  # 更新渲染

    def get_vtk_polydata(self) -> vtk.vtkPolyData:
        """
        获取当前的 VTK 点云数据。

        :return: 当前的 VTK 点云数据。
        """
        return self.polydata

    def get_visible(self) -> bool:
        """
        获取点云的可见状态。

        :return: 点云是否可见。
        """
        return self.actor.GetVisibility() == 1

    def remove_mask_cloud_actor(self):
        """
        移除点的掩码颜色，恢复原始颜色。
        """
        self.mask_cloud_actor = None
        self.polydata.GetPointData().SetScalars(self.vtk_colors)
        self.update()

    def import_point_cloud(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        从文件导入点云数据。

        :param file_path: 点云文件路径。
        :return: 导入是否成功以及错误消息（如果有）
        """
        error_messages = {
            FileNotFoundError: "FileNotFoundError",
            PermissionError: "PermissionError",
            IsADirectoryError: "IsADirectoryError"
        }

        try:
            polydata = file_to_vtk_polydata(file_path)
        except tuple(error_messages.keys()) as e:
            # 捕获并返回对应的错误消息
            return False, error_messages[type(e)]
        except Exception as e:
            # 捕获其他未预见的异常
            return False, str(e)

        self.set_vtk_polydata(polydata)
        return True, None

    def export_point_cloud(self, file_path: str) -> bool:
        """
        将点云数据导出到文件。

        :param file_path: 保存文件的路径。
        :return: 成功写入文件返回 True，否则返回 False
        """
        return vtk_polydata_to_file(self.polydata, file_path)

    def modified(self):
        """
        更新点云数据并重新渲染。
        """
        self._generate_point_cloud()

    def hide(self):
        """
        隐藏点云 actor。
        """
        self.actor.VisibilityOff()

    def show(self):
        """
        显示点云 actor。
        """
        self.actor.VisibilityOn()

    def toggle_visibility(self):
        """
        切换点云 actor 的可见性。
        """
        self.actor.SetVisibility(not self.actor.GetVisibility())

    def update(self):
        """
        更新点云并重新渲染。
        """
        self.vertex_filter.Update()

    def reset(self):
        """
        重置 VTK 点和颜色数据，清空当前点云。
        """
        self.vtk_points.Reset()
        self.vtk_colors.Reset()

    def _generate_point_cloud(self):
        """
        根据当前的图像和采样点生成点云，并更新 VTK 演员。
        """
        self.reset()  # 重置现有数据
        for color in self._get_points():
            coordinates = calculate_point_coordinates(color, self.sphere_radius)  # 计算点坐标
            self.vtk_points.InsertNextPoint(coordinates)
            self.vtk_colors.InsertNextTuple3(*self._determine_mask_color(color))  # 设置颜色
        self.update()  # 更新渲染

    def _get_points(self) -> Iterable:
        """
        从图像中获取采样点颜色。

        :return: 采样的颜色点。
        """
        if not self.image:
            return []
        return sample_image_colors(self.image, self.sample_count, color_space='RGB')

    def _determine_mask_color(self, color: MaskPointColor) -> MaskPointColor:
        """
        确定点的颜色，优先级为：全局掩码 > 实例掩码 > 原始颜色。

        :param color: 原始颜色。
        :return: 确定后的颜色。
        """
        return (
                self.color_point_cloud.get_global_mask_cloud_actor()
                or self.mask_cloud_actor
                or color
        )

    def _apply_mask_color(self):
        """
        应用掩码颜色到所有点。
        """
        assert self.vtk_colors is not None, "VTK 颜色数据为空"
        if not self.vtk_colors.GetNumberOfTuples():
            return
        mask_colors = vtk.vtkUnsignedCharArray()
        mask_colors.SetNumberOfComponents(3)
        mask_colors.SetName("MaskColors")

        # 为每个点应用掩码颜色
        for _ in range(self.vtk_colors.GetNumberOfTuples()):
            mask_colors.InsertNextTuple3(*self.mask_cloud_actor)
        self.polydata.GetPointData().SetScalars(mask_colors)
        self.update()


class ColorPointCloud:
    def __init__(self, renderer: vtk.vtkRenderer, sphere_radius: int, sample_count: int,
                 global_mask_cloud_actor: Optional[MaskPointColor] = None):
        """
        管理和生成多个 PointCloudActor，用于点云的渲染。

        :param renderer: VTK 渲染器。
        :param sphere_radius: 点云球体的半径。
        :param sample_count: 采样点数量。
        :param global_mask_cloud_actor: 全局掩码颜色。
        """
        self.renderer = renderer
        self.sphere_radius = sphere_radius
        self.sample_count = sample_count
        self.global_mask_cloud_actor = global_mask_cloud_actor
        self.point_cloud_actors: List[PointCloudActor] = []  # 存储管理的点云

    def add_point_cloud(self, image: Optional[Image] = None,
                        color_list: Optional[ColorList] = None,
                        mask_cloud_actor: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        添加新的点云到渲染器中。

        :param image: 输入的图像。
        :param color_list: 颜色列表。
        :param mask_cloud_actor: 掩码颜色。
        :return: 创建的点云演员对象。
        """
        cloud_actor = PointCloudActor(color_point_cloud=self, sphere_radius=self.sphere_radius)
        if image:
            cloud_actor.set_image(image, self.sample_count)  # 根据图像生成点云
        else:
            cloud_actor.set_sample_count(self.sample_count)  # 设置采样点数量
        if color_list:
            cloud_actor.set_color_list(color_list)  # 根据颜色列表生成点云
        if mask_cloud_actor or self.global_mask_cloud_actor:
            cloud_actor.set_mask_cloud_actor(mask_cloud_actor or self.global_mask_cloud_actor)

        cloud_actor.update()
        self.renderer.AddActor(cloud_actor.actor)  # 将点云添加到渲染器
        self.point_cloud_actors.append(cloud_actor)
        return cloud_actor

    def set_sample_count(self, value: int):
        """
        设置采样点数量，并更新所有点云。

        :param value: 采样点数量。
        """
        self.sample_count = value
        for actor in self.point_cloud_actors:
            actor.set_sample_count(value)

    def get_global_mask_cloud_actor(self) -> Optional[MaskPointColor]:
        """
        获取全局掩码颜色。

        :return: 全局掩码颜色。
        """
        return self.global_mask_cloud_actor

    def remove_point_cloud(self, cloud_actor: PointCloudActor) -> bool:
        """
        从渲染器中移除指定的点云。

        :param cloud_actor: 要移除的点云对象。
        :return: 如果成功移除，返回 True；否则返回 False。
        """
        if cloud_actor in self.point_cloud_actors:
            self.renderer.RemoveActor(cloud_actor.actor)
            self.point_cloud_actors.remove(cloud_actor)
            return True
        return False

    def remove_all_point_cloud(self):
        """
        移除所有点云。
        """
        for actor in self.point_cloud_actors:
            self.renderer.RemoveActor(actor.actor)
        self.point_cloud_actors.clear()

    def update_all(self):
        """
        更新所有点云。
        """
        for actor in self.point_cloud_actors:
            actor.update()
