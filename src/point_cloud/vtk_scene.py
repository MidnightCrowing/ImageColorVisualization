from functools import singledispatchmethod

import numpy as np
import vtk
from qfluentwidgets import Theme
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor


class VTKScene:
    """负责设置和管理VTK渲染场景，包括坐标轴、经纬线。"""

    def __init__(self, vtk_widget: QVTKRenderWindowInteractor, ball_round: int):
        self.ball_round = ball_round

        # 经纬线配置
        self.number_sides = 100  # 设置圆的边数
        self.lines_color = (0.5, 0.5, 0.5)  # 初始颜色为灰色
        self.lines_opacity = 0.2  # 设置透明度
        self.lines_width = 1.0  # 设置线宽

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

        self.reset_camera()

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

    def add_latitude_lines(self, num_lines: int = 5):
        """绘制并添加纬线到渲染器中。"""
        for i in range(num_lines):
            # 计算纬线的角度、半径和高度
            angle = (i - (num_lines - 1) / 2) * np.pi / (num_lines - 1)
            radius = np.cos(angle) * self.ball_round
            height = np.sin(angle) * self.ball_round

            # 创建纬线的圆形源
            circle_source = vtk.vtkRegularPolygonSource()
            circle_source.SetRadius(radius)
            circle_source.SetNumberOfSides(self.number_sides)  # 设置圆的边数
            circle_source.SetCenter(0, 0, height)
            circle_source.SetGeneratePolygon(False)  # 不生成多边形
            circle_source.Update()

            # 映射圆形源
            circle_mapper = vtk.vtkPolyDataMapper()
            circle_mapper.SetInputConnection(circle_source.GetOutputPort())

            # 创建并配置圆形演员
            circle_actor = vtk.vtkActor()
            circle_actor.SetMapper(circle_mapper)
            circle_actor.GetProperty().SetColor(*self.lines_color)  # 设置颜色
            circle_actor.GetProperty().SetOpacity(self.lines_opacity)  # 设置透明度
            circle_actor.GetProperty().SetRepresentationToWireframe()  # 设置为线框模式
            circle_actor.GetProperty().SetLineWidth(self.lines_width)  # 设置线宽

            # 将演员添加到渲染器
            self.renderer.AddActor(circle_actor)

    def add_longitude_lines(self, num_lines: int = 3):
        """绘制并添加经线到渲染器中。"""
        for i in range(num_lines):
            # 计算经线的角度
            angle = i * 360 / num_lines

            # 创建经线的圆形源
            circle_source = vtk.vtkRegularPolygonSource()
            circle_source.SetRadius(self.ball_round)
            circle_source.SetNumberOfSides(self.number_sides)  # 设置圆的边数
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
            circle_actor.GetProperty().SetColor(*self.lines_color)  # 设置颜色
            circle_actor.GetProperty().SetOpacity(self.lines_opacity)  # 设置透明度
            circle_actor.GetProperty().SetRepresentationToWireframe()  # 设置为线框模式
            circle_actor.GetProperty().SetLineWidth(self.lines_width)  # 设置线宽

            # 将演员添加到渲染器
            self.renderer.AddActor(circle_actor)

    def reset_camera(self):
        self.renderer.ResetCamera()  # 重置相机以适应点云
        self.renderWindow.Render()

    def set_theme(self, theme: Theme):
        """设置主题颜色。"""
        if theme == Theme.DARK:
            self.set_background('dark')
        else:
            self.set_background('light')
        self.update_lines_color(theme)

    @singledispatchmethod
    def set_background(self, arg):
        raise NotImplementedError("Unsupported type")

    @set_background.register
    def _(self, theme: str):
        if theme == 'dark':
            self.renderer.SetBackground(0.09, 0.09, 0.09)
        elif theme == 'light':
            self.renderer.SetBackground(0.91, 0.91, 0.91)
        else:
            raise ValueError("Invalid theme. Expected 'dark' or 'light'.")

    @set_background.register
    def _(self, color: tuple):
        if len(color) == 3 and all(isinstance(c, float) for c in color):
            self.renderer.SetBackground(*color)
        else:
            raise ValueError("Invalid color. Expected a tuple of three floats.")

    def update_lines_color(self, theme: Theme):
        """更新经纬线的颜色以适配主题。"""
        if theme == Theme.LIGHT:
            self.lines_color = (0.3, 0.3, 0.3)
            self.lines_opacity = 0.5
        else:
            self.lines_color = (0.5, 0.5, 0.5)
            self.lines_opacity = 0.3
        self.add_latitude_lines()  # 重新添加纬线以更新颜色
        self.add_longitude_lines()  # 重新添加经线以更新颜色

    def render(self):
        self.interactor.Render()

    def sync_scene(self, renderer: vtk.vtkRenderer, interactor: vtk.vtkRenderWindowInteractor):
        def sync_cameras(caller, event):
            cam1 = self.renderer.GetActiveCamera()
            cam2 = renderer.GetActiveCamera()

            # 将相机的参数同步到另一个相机
            cam1.SetPosition(cam2.GetPosition())
            cam1.SetFocalPoint(cam2.GetFocalPoint())
            cam1.SetViewUp(cam2.GetViewUp())
            cam1.SetViewAngle(cam2.GetViewAngle())
            cam1.SetClippingRange(cam2.GetClippingRange())

            # 刷新第二个渲染窗口
            self.renderWindow.Render()

        # 绑定 'StartInteractionEvent' 事件，当用户开始与交互器进行交互（如拖动、旋转、缩放）时，调用 sync_cameras 函数
        interactor.AddObserver('StartInteractionEvent', sync_cameras)

        # 绑定 'EndInteractionEvent' 事件，当用户完成与交互器的交互（如释放鼠标）时，调用 sync_cameras 函数
        interactor.AddObserver('EndInteractionEvent', sync_cameras)

        # 绑定 'InteractionEvent' 事件，在用户与交互器进行交互的整个过程中（如拖动、旋转、缩放）时，调用 sync_cameras 函数
        interactor.AddObserver('InteractionEvent', sync_cameras)
