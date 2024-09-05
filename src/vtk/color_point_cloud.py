from __future__ import annotations

import colorsys
from typing import Optional, List, Tuple, overload, Iterable

import numpy as np
import vtk
from PIL.Image import Image

from src.utils.getpixel import sample_image_colors

MaskPointColor = Tuple[float, float, float]
Point3D = Tuple[float, float, float]


class PointCloudActor:
    @overload
    def __init__(self, color_point_cloud: ColorPointCloud, sphere_radius: int, sample_count: int) -> None:
        ...

    @overload
    def __init__(self, color_point_cloud: ColorPointCloud, sphere_radius: int, image: Image, sample_count: int,
                 mask_point_color: MaskPointColor = None) -> None:
        ...

    @overload
    def __init__(self, color_point_cloud: ColorPointCloud, sphere_radius: int, points: List[Point3D],
                 mask_point_color: MaskPointColor = None) -> None:
        ...

    def __init__(self, color_point_cloud: ColorPointCloud, sphere_radius: int,
                 image: Image = None, sample_count: int = None,
                 points: List[Point3D] = None,
                 mask_point_color: MaskPointColor = None) -> None:
        """
        初始化 PointCloudActor。

        :param sphere_radius: 点云的整体大小，控制点分布的半径。
        :param image: 用于采样点的图像。
        :param sample_count: 图像的采样点数量。
        :param points: 点的坐标列表，用于直接创建点云。
        :param mask_point_color: 点云的颜色，若未设置则使用图像颜色。
        """
        self.color_point_cloud = color_point_cloud
        self.sphere_radius = sphere_radius
        self.image = image
        self.sample_count = sample_count
        self.custom_points = points
        self.mask_point_color = mask_point_color

        # 初始化 VTK 点和颜色数组
        self.vtk_points = vtk.vtkPoints()
        self.vtk_colors = vtk.vtkUnsignedCharArray()
        self.vtk_colors.SetNumberOfComponents(3)
        self.vtk_colors.SetName("Colors")

        self.actor = vtk.vtkActor()

    def set_image(self, image: Image, update: bool = True):
        """
        设置图像并从中重新采样点。

        :param image: 新图像。
        :param update: 是否立即更新点云。
        """
        self.image = image
        if update:
            self.update_point_cloud()

    def set_sample_count(self, sample_count: int, update: bool = True):
        """
        设置采样点数量。

        :param sample_count: 新的图像的采样点数量。
        :param update: 是否立即更新点云。
        """
        self.sample_count = sample_count
        if update:
            self.update_point_cloud()

    def set_points(self, points: List[Point3D], update: bool = True):
        """
        设置点坐标列表。

        :param points: 新的点坐标列表。
        :param update: 是否立即更新点云。
        """
        self.custom_points = points
        if update:
            self.update_point_cloud()

    def set_mask_point_color(self, color: MaskPointColor, update: bool = True):
        """
        设置点的颜色。

        :param color: 新的点颜色。
        :param update: 是否立即更新点云。
        """
        self.mask_point_color = color
        if update:
            self.update_point_cloud()

    def remove_mask_point_color(self, update: bool = True):
        """
        移除点的颜色。

        :param update: 是否立即更新点云。
        """
        self.mask_point_color = None
        if update:
            self.update_point_cloud()

    def _generate_point_cloud(self):
        """生成点云并更新 VTK 演员。"""
        self.reset()

        # 从图像采样颜色并添加点
        for color in self._get_points():
            coordinates = self._calculate_point_coordinates(color)
            self.vtk_points.InsertNextPoint(coordinates)
            self.vtk_colors.InsertNextTuple3(*self._determine_mask_point_color(color))

        # 设置点云数据
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(self.vtk_points)
        polydata.GetPointData().SetScalars(self.vtk_colors)

        # 使用顶点图形过滤器处理点云
        vertex_filter = vtk.vtkVertexGlyphFilter()
        vertex_filter.SetInputData(polydata)
        vertex_filter.Update()

        # 设置映射器和演员
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(vertex_filter.GetOutput())
        self.actor.SetMapper(mapper)

    def _get_points(self) -> Iterable:
        if self.custom_points is None:
            if self.image is None:
                return []
            return sample_image_colors(self.image, self.sample_count, color_space='RGB')
        else:
            return self.custom_points

    def _calculate_point_coordinates(self, color: MaskPointColor) -> MaskPointColor:
        """
        根据 RGB 颜色计算点的三维坐标。

        :param color: RGB 颜色元组。
        :return: 三维坐标 (x, y, z)。
        """
        r, g, b = color
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        h_rad = h * 2 * np.pi

        z = 2 * (l - 0.5) * self.sphere_radius
        m = np.sqrt(1 - np.square(2 * (l - 0.5))) * s
        x = m * np.sin(h_rad) * self.sphere_radius
        y = m * np.cos(h_rad) * self.sphere_radius

        return x, y, z

    def _determine_mask_point_color(self, color: MaskPointColor) -> MaskPointColor:
        """
        确定点的颜色。

        :param color: 原始 RGB 颜色。
        :return: 确定的点颜色。
        """
        # 获取全局的 mask color
        global_mask_color = self.color_point_cloud.get_global_mask_point_color()

        # 返回顺序为：global_mask_color > self.mask_point_color > color
        return global_mask_color or self.mask_point_color or color

    def update_point_cloud(self):
        """更新点云数据并重新渲染。"""
        self._generate_point_cloud()

    def reset(self):
        """重置 VTK 点和颜色数据。"""
        self.vtk_points.Reset()
        self.vtk_colors.Reset()


class ColorPointCloud:
    def __init__(self, renderer: vtk.vtkRenderer, sphere_radius: int, sample_count: int,
                 global_mask_point_color: Optional[MaskPointColor] = None):
        """
        用于生成点云，管理多个 PointCloudActor。

        :param renderer: VTK 渲染器。
        :param sphere_radius: 控制点云的整体大小。
        :param sample_count: 每个图像的采样点数量。
        :param global_mask_point_color: 全局点云颜色。
        """
        self.renderer = renderer
        self.sphere_radius = sphere_radius
        self.sample_count = sample_count
        self.global_mask_point_color = global_mask_point_color
        self.point_cloud_actors: List[PointCloudActor] = []

    @overload
    def add_point_cloud(self) -> PointCloudActor:
        ...

    @overload
    def add_point_cloud(self, mask_point_color: MaskPointColor) -> PointCloudActor:
        ...

    @overload
    def add_point_cloud(self, image: Image, mask_point_color: Optional[MaskPointColor] = None) -> PointCloudActor:
        ...

    @overload
    def add_point_cloud(self, points: List[Point3D],
                        mask_point_color: Optional[MaskPointColor] = None) -> PointCloudActor:
        ...

    def add_point_cloud(self, image: Optional[Image] = None,
                        points: Optional[List[Point3D]] = None,
                        mask_point_color: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        添加新的点云到渲染器中。

        :param image: 用于采样点的图像。
        :param points: 点的坐标列表。
        :param mask_point_color: 点云的颜色。
        :return: 创建的 PointCloudActor 对象。
        """
        # 检查必须的输入参数
        # assert not (image is None and points is None), '必须提供图像或点坐标列表。'

        point_actor = PointCloudActor(color_point_cloud=self, sphere_radius=self.sphere_radius,
                                      sample_count=self.sample_count)

        if image is not None:
            point_actor.set_image(image, update=False)

        if points is not None:
            point_actor.set_points(points, update=False)

        if mask_point_color is None:
            mask_point_color = self.global_mask_point_color
        point_actor.set_mask_point_color(mask_point_color, update=False)

        # 更新点云数据并添加到渲染器中
        point_actor.update_point_cloud()
        self.point_cloud_actors.append(point_actor)
        self.renderer.AddActor(point_actor.actor)

        return point_actor

    def remove_point_cloud(self, point_actor: PointCloudActor) -> bool:
        """
        从渲染器中移除指定的点云。

        :param point_actor: 要移除的 PointCloudActor 对象。
        :return: 是否成功移除。
        """
        if point_actor in self.point_cloud_actors:
            self.renderer.RemoveActor(point_actor.actor)
            self.point_cloud_actors.remove(point_actor)
            return True
        return False

    def remove_all_point_cloud(self):
        """移除所有点云。"""
        for actor in self.point_cloud_actors:
            self.renderer.RemoveActor(actor.actor)
        self.point_cloud_actors.clear()

    def update_all(self):
        """更新所有点云。"""
        for actor in self.point_cloud_actors:
            actor.update_point_cloud()

    def set_sample_count(self, value: int, update: bool = True):
        """
        设置采样点数量。

        :param value: 新的采样点数量。
        :param update: 是否立即更新所有点云。
        """
        self.sample_count = value
        for actor in self.point_cloud_actors:
            actor.sample_count = value
        if update:
            self.update_all()

    def get_global_mask_point_color(self) -> Optional[MaskPointColor]:
        return self.global_mask_point_color
