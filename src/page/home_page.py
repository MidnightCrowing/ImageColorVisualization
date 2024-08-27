import colorsys

import numpy as np
import vtk
from PySide6.QtWidgets import QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor

from src.getpixel import sample_image_colors
from ..ui.ui_HomePage import Ui_HomePage

ROUND = 10
image_preview = r'C:\Users\lenovo\Desktop\PixPin_2024-08-27_15-21-53.png'


class VTKScene:
    """负责设置和管理VTK渲染场景，包括坐标轴、经纬线和颜色点云。"""

    def __init__(self, vtk_widget: QVTKRenderWindowInteractor):
        # 初始化渲染器和渲染窗口
        self.renderer = vtk.vtkRenderer()
        self.renderWindow = vtk_widget.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        # 设置交互器
        self.interactor = self.renderWindow.GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        # 添加场景组件
        self.add_axes_widget()  # 添加坐标轴
        self.add_latitude_lines()  # 添加纬线
        self.add_longitude_lines()  # 添加经线

        # 添加颜色点云
        self.color_point_cloud = ColorPointCloud(self.renderer, image_preview)

        self.renderer.SetBackground(0.09, 0.09, 0.09)  # 设置背景颜色
        self.renderer.ResetCamera()  # 重置相机以适应点云

        # 启动交互器
        self.interactor.Initialize()
        self.interactor.Start()

    def add_axes_widget(self):
        """在渲染窗口中添加坐标轴标记。"""
        axes_actor = vtkAxesActor()  # 创建坐标轴演员
        self.axes_widget = vtkOrientationMarkerWidget()  # 创建坐标轴标记小部件
        self.axes_widget.SetOrientationMarker(axes_actor)  # 设置坐标轴演员
        self.axes_widget.SetInteractor(self.interactor)  # 设置交互器
        self.axes_widget.EnabledOn()  # 启用小部件
        self.axes_widget.SetEnabled(True)  # 确保小部件启用
        self.axes_widget.InteractiveOff()  # 禁用交互

    def add_latitude_lines(self, num_lines: int=5):
        """绘制并添加纬线到渲染器中。"""
        for i in range(num_lines):
            # 计算纬线的角度、半径和高度
            angle = (i - (num_lines - 1) / 2) * np.pi / (num_lines - 1)
            radius = np.cos(angle) * ROUND
            height = np.sin(angle) * ROUND

            # 创建纬线的圆形源
            circle_source = vtk.vtkRegularPolygonSource()
            circle_source.SetRadius(radius)
            circle_source.SetNumberOfSides(100)  # 设置圆的边数
            circle_source.SetCenter(0, 0, height)
            circle_source.SetGeneratePolygon(False)  # 不生成多边形
            circle_source.Update()

            # 映射圆形源
            circle_mapper = vtk.vtkPolyDataMapper()
            circle_mapper.SetInputConnection(circle_source.GetOutputPort())

            # 创建并配置圆形演员
            circle_actor = vtk.vtkActor()
            circle_actor.SetMapper(circle_mapper)
            circle_actor.GetProperty().SetColor(0.5, 0.5, 0.5)  # 设置颜色为灰色
            circle_actor.GetProperty().SetOpacity(0.5)  # 设置透明度
            circle_actor.GetProperty().SetRepresentationToWireframe()  # 设置为线框模式
            circle_actor.GetProperty().SetLineWidth(1.0)  # 设置线宽

            # 将演员添加到渲染器
            self.renderer.AddActor(circle_actor)

    def add_longitude_lines(self, num_lines: int=3):
        """绘制并添加经线到渲染器中。"""
        for i in range(num_lines):
            # 计算经线的角度
            angle = i * 360 / num_lines

            # 创建经线的圆形源
            circle_source = vtk.vtkRegularPolygonSource()
            circle_source.SetRadius(ROUND)
            circle_source.SetNumberOfSides(100)  # 设置圆的边数
            circle_source.SetCenter(0, 0, 0)
            circle_source.SetGeneratePolygon(False)  # 不生成多边形
            circle_source.Update()

            # 应用旋转变换
            transform = vtk.vtkTransform()
            transform.RotateX(90)  # 旋转X轴90度
            transform.RotateY(angle)  # 绕Y轴旋转角度

            # 转换圆形源的数据
            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetInputConnection(circle_source.GetOutputPort())
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            # 映射经线数据
            circle_mapper = vtk.vtkPolyDataMapper()
            circle_mapper.SetInputConnection(transform_filter.GetOutputPort())

            # 创建并配置经线演员
            circle_actor = vtk.vtkActor()
            circle_actor.SetMapper(circle_mapper)
            circle_actor.GetProperty().SetColor(0.5, 0.5, 0.5)  # 设置颜色为灰色
            circle_actor.GetProperty().SetOpacity(0.5)  # 设置透明度
            circle_actor.GetProperty().SetRepresentationToWireframe()  # 设置为线框模式
            circle_actor.GetProperty().SetLineWidth(1.0)  # 设置线宽

            # 将演员添加到渲染器
            self.renderer.AddActor(circle_actor)


class ColorPointCloud:
    """处理颜色点云，负责将图像颜色样本转换为三维点云并渲染。"""

    def __init__(self, renderer: vtk.vtkRenderer, image_path: str, sample_count: int=10000000):
        self.renderer = renderer
        self.image_path = image_path
        self.sample_count = sample_count

        # 创建点云数据存储
        self.points = vtk.vtkPoints()
        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)  # RGB三种颜色
        self.colors.SetName("Colors")  # 设置颜色数组名称

        # 生成点云
        self.generate_point_cloud()

    def generate_point_cloud(self):
        """从图像中生成颜色点云并添加到渲染器中。"""
        for color in sample_image_colors(self.image_path, self.sample_count, color_space='RGB'):
            r, g, b = color
            # 将RGB转换为HLS
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            h_rad = h * 2 * np.pi  # 转换为弧度

            # 计算点云的三维坐标
            z = 2 * (l - 0.5) * ROUND
            m = np.sqrt(1 - np.square(2 * (l - 0.5))) * s
            x = m * np.sin(h_rad) * ROUND
            y = m * np.cos(h_rad) * ROUND

            # 插入点和颜色到数据集中
            self.points.InsertNextPoint(x, y, z)
            self.colors.InsertNextTuple3(r, g, b)

        # 创建点云数据
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(self.points)
        polydata.GetPointData().SetScalars(self.colors)

        # 使用顶点图形过滤器处理点云
        vertex_filter = vtk.vtkVertexGlyphFilter()
        vertex_filter.SetInputData(polydata)
        vertex_filter.Update()

        # 映射点云数据
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(vertex_filter.GetOutput())

        # 创建并配置点云演员
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # 将演员添加到渲染器
        self.renderer.AddActor(actor)


class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.image_preview.setImage(image_preview)
        self.image_preview.scaledToHeight(140)
        self.image_preview.setBorderRadius(8, 8, 8, 8)

        self.vtk_scene = VTKScene(self.vtk_widget)
