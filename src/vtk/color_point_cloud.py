import colorsys
from typing import Optional

import numpy as np
import vtk
from PIL.Image import Image

from src.utils.getpixel import sample_image_colors


class ColorPointCloud:
    """处理颜色点云，负责将图像颜色样本转换为三维点云并渲染。"""

    def __init__(self, renderer: vtk.vtkRenderer, ball_round: int, sample_count: int):
        self.renderer = renderer
        self.ball_round = ball_round
        self.sample_count = sample_count
        self.image: Optional[Image] = None

        # 初始化点云数据存储
        self.points = vtk.vtkPoints()
        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)  # RGB三种颜色
        self.colors.SetName("Colors")  # 设置颜色数组名称

        # 初始化点云
        self.actor = vtk.vtkActor()
        self.polydata = vtk.vtkPolyData()

    def _generate_point_cloud(self):
        """从图像中生成颜色点云并更新渲染器中的演员。"""
        # 清除现有的点和颜色
        self.points.Reset()
        self.colors.Reset()

        # 从图像中采样颜色并生成点云
        for color in sample_image_colors(self.image, self.sample_count, color_space='RGB'):
            r, g, b = color
            # 将RGB转换为HLS
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            h_rad = h * 2 * np.pi  # 转换为弧度

            # 计算点云的三维坐标
            z = 2 * (l - 0.5) * self.ball_round
            m = np.sqrt(1 - np.square(2 * (l - 0.5))) * s
            x = m * np.sin(h_rad) * self.ball_round
            y = m * np.cos(h_rad) * self.ball_round

            # 插入点和颜色到数据集中
            self.points.InsertNextPoint(x, y, z)
            self.colors.InsertNextTuple3(r, g, b)

        # 更新点云数据
        self.polydata.SetPoints(self.points)
        self.polydata.GetPointData().SetScalars(self.colors)

        # 使用顶点图形过滤器处理点云
        vertex_filter = vtk.vtkVertexGlyphFilter()
        vertex_filter.SetInputData(self.polydata)
        vertex_filter.Update()

        # 映射点云数据
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(vertex_filter.GetOutput())

        # 设置演员的映射器
        self.actor.SetMapper(mapper)

        # 如果Actor不在渲染器中，添加Actor
        if not self.renderer.HasViewProp(self.actor):
            self.renderer.AddActor(self.actor)

    def set_image(self, new_image: Image, update: bool = True):
        """更新图像路径并重新生成点云。"""
        self.image = new_image
        if update:
            self.update_point_cloud()

    def set_sample_count(self, new_sample_count: int, update: bool = True):
        """更新采样点数量并重新生成点云。"""
        self.sample_count = new_sample_count
        if update:
            self.update_point_cloud()

    def update_point_cloud(self):
        """更新点云数据。"""
        self._generate_point_cloud()
