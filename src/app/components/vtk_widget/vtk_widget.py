import os.path
from typing import Callable, Optional

import vtk
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from qfluentwidgets import (Action, CommandBar, FluentIcon, InfoBar, InfoBarIcon, InfoBarPosition, PillToolButton,
                            Theme, ToolTipFilter, ToolTipPosition, isDarkTheme)

from src.utils.config import VTKInteractorStyle, cfg
from .simple_vtk_widget import SimpleVTKWidget
from ..key_prompts_widget import KeyAction, KeyPrompts
from ...common.icon import Icon


class MenuViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.bg_widgets = []

        # 背景覆盖 Widget 解决圆角背景问题
        self.menu_bg = QWidget(self)
        self.menu_bg.setStyleSheet(f"background-color: {"#171717" if isDarkTheme() else "#E8E8E8"};")
        self.bar_bg = QWidget()
        self.bar_bg.setStyleSheet(
            f"background-color: {"#2B2B2B" if isDarkTheme() else "#F9F9F9"}; border-radius: 10px;")
        menu_layout = QVBoxLayout(self.menu_bg)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.addWidget(self.bar_bg)
        self.bg_widgets.append(self.menu_bg)

        # CommandBar 和操作按钮
        self.bar = CommandBar()
        self.bar.addActions([
            Action(FluentIcon.CONSTRACT, self.tr('Change Theme'), checkable=True,
                   triggered=self.change_theme),
            Action(Icon.COORDINATE_SYSTEM, self.tr('Hide Coordinate System'), checkable=True, checked=True,
                   triggered=self.coordinate_action),
            Action(Icon.SCREENSHOT, self.tr('Save Screenshot'), shortcut='Ctrl+S',
                   triggered=self.screenshot_action),
        ])
        self.bar.addHiddenActions([
            Action(FluentIcon.SYNC, self.tr('Refresh'), shortcut='Ctrl+E',
                   triggered=self.refresh_action),
            Action(FluentIcon.INFO, self.tr('Key Prompts'), shortcut='Ctrl+K',
                   triggered=self.key_prompts_action),
            Action(FluentIcon.SETTING, self.tr('Settings'), shortcut='Ctrl+L',
                   triggered=self.setting_action)
        ])
        self.bar.resizeToSuitableWidth()
        bar_layout = QVBoxLayout(self.bar_bg)
        bar_layout.addWidget(self.bar)

        # 定义通用按钮创建方法
        def create_button(icon: FluentIcon, text: str, triggered: Callable) -> PillToolButton:
            btn = PillToolButton(icon, self)
            btn.clicked.connect(triggered)
            btn.setFixedSize(35, 35)
            btn.setCheckable(False)
            btn.setToolTip(text)
            btn.installEventFilter(ToolTipFilter(btn, 300, ToolTipPosition.LEFT))
            return btn

        # 各种控制按钮
        self.home_btn = create_button(FluentIcon.HOME, self.tr('Standard View'),
                                      triggered=self.on_home_clicked)
        self.zoom_in_btn = create_button(FluentIcon.ZOOM_IN, self.tr('Zoom In'),
                                         triggered=self.on_zoom_in_clicked)
        self.zoom_out_btn = create_button(FluentIcon.ZOOM_OUT, self.tr('Zoom Out'),
                                          triggered=self.on_zoom_out_clicked)
        self.full_screen_btn = create_button(FluentIcon.FULL_SCREEN, self.tr('Enter Fullscreen'),
                                             triggered=self.on_full_screen_clicked)

        # 添加背景 widget 并布局按钮
        self.home_bg = self.create_button_bg(self.home_btn)
        self.zoom_in_bg = self.create_button_bg(self.zoom_in_btn)
        self.zoom_out_bg = self.create_button_bg(self.zoom_out_btn)
        self.full_screen_bg = self.create_button_bg(self.full_screen_btn)

        self.home_bg.setHidden(True)

        # 使用 QTimer 延迟调整按钮位置
        QTimer.singleShot(0, self.adjust_widget_position)

    # 帮助函数：为按钮创建背景并布局
    def create_button_bg(self, button: PillToolButton) -> QWidget:
        bg_widget = QWidget(self)
        bg_widget.setStyleSheet(f"background-color: {"#171717" if isDarkTheme() else "#E8E8E8"};")
        layout = QVBoxLayout(bg_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(button)
        self.bg_widgets.append(bg_widget)
        return bg_widget

    def show_home_button(self):
        if self.home_bg.isHidden():
            self.home_bg.setHidden(False)
            self.adjust_widget_position()

    def change_theme(self, checked):
        raise NotImplementedError

    def coordinate_action(self, checked):
        raise NotImplementedError

    def screenshot_action(self):
        raise NotImplementedError

    def refresh_action(self):
        raise NotImplementedError

    def key_prompts_action(self):
        raise NotImplementedError

    def setting_action(self):
        raise NotImplementedError

    def on_home_clicked(self):
        raise NotImplementedError

    def on_zoom_in_clicked(self):
        raise NotImplementedError

    def on_zoom_out_clicked(self):
        raise NotImplementedError

    def on_full_screen_clicked(self):
        raise NotImplementedError

    # 调整按钮位置
    def adjust_widget_position(self):
        self.menu_bg.move(self.width() - self.menu_bg.width() - 10, 10)

        for bg_widget, offset in zip([self.home_bg, self.zoom_in_bg, self.zoom_out_bg, self.full_screen_bg],
                                     [200, 150, 100, 50]):
            bg_widget.move(self.width() - bg_widget.width() - 10, self.height() - offset)

    def resizeEvent(self, event):
        self.adjust_widget_position()
        event.accept()


class VTKViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 初始化 VTK 渲染窗口
        self.vtk_widget = SimpleVTKWidget(self)
        self.vtk_manager = self.vtk_widget.vtk_manager

        self.renderer = self.vtk_manager.vtk_scene.renderer
        self.vtk_manager.vtk_scene.interactor.AddObserver("EndInteractionEvent", self.on_interaction_callback)
        self.vtk_manager.vtk_scene.interactor.AddObserver("KeyPressEvent", self.on_keypress_callback)

        self.default_camera_view_up = None
        self.default_camera_focal_point = None
        self.default_camera_position = None
        self.default_camera_zoom = 1.0  # 默认缩放因子

        self.save_default_view()

    def save_default_view(self):
        self.default_camera_position = self.renderer.GetActiveCamera().GetPosition()
        self.default_camera_focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        self.default_camera_view_up = self.renderer.GetActiveCamera().GetViewUp()
        self.default_camera_zoom = self.renderer.GetActiveCamera().GetParallelScale()

    def restore_default_view(self):
        # 恢复相机的默认视图
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(self.default_camera_position)
        camera.SetFocalPoint(self.default_camera_focal_point)
        camera.SetViewUp(self.default_camera_view_up)
        camera.SetParallelScale(self.default_camera_zoom)

        # 更新渲染器
        self.renderer.ResetCamera()
        self.refresh()

    # 定义回调函数
    def on_interaction_callback(self, caller, event):
        raise NotImplementedError

    def on_keypress_callback(self, obj, event):
        raise NotImplementedError

    def zoom_in(self, factor=1.2):
        """
        放大视图。factor 越大，放大倍数越大。
        默认放大倍数为 1.2。
        """
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(factor)
        self.vtk_widget.Render()

    def zoom_out(self, factor=1.2):
        """
        缩小视图。factor 越大，缩小倍数越大。
        默认缩小倍数为 1.2。
        """
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(1 / factor)
        self.vtk_widget.Render()

    def reset_camera(self):
        self.renderer.ResetCamera()
        self.vtk_widget.Render()

    def refresh(self):
        # 强制渲染窗口刷新
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.Render()
        render_window.GetInteractor().Render()
        render_window.Frame()

    def set_trackball_interaction_mode(self):
        self.vtk_manager.vtk_scene.set_interactor_style(VTKInteractorStyle.Trackball_Camera)

    def set_joystick_interaction_mode(self):
        self.vtk_manager.vtk_scene.set_interactor_style(VTKInteractorStyle.Joystick_Camera)

    def resizeEvent(self, event):
        self.vtk_widget.resize(self.size())
        event.accept()


class VTKWidget(MenuViewWidget, VTKViewWidget):
    saveScreenshot = Signal(str)
    openSetting = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.is_change_theme: bool = False
        self.is_fullscreen: bool = False
        self.is_maximized: bool = False

        self.key_prompts_bar: Optional[InfoBar] = None
        self.key_prompts: Optional[KeyPrompts] = None

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            if self.is_maximized:
                self.window().showMaximized()  # 恢复到最大化模式
            else:
                self.window().showNormal()  # 恢复到普通模式
            if self.parent is not None:
                self.setParent(self.parent)  # 将组件放回中央窗口
                self.parent.layout().addWidget(self)  # 重新添加到布局
        else:
            self.is_maximized = self.window().isMaximized()  # 保存当前最大化状态
            self.window().showFullScreen()  # 设置窗口为全屏模式
            if self.parent is not None:
                self.setParent(self.window())  # 设置组件的父级为主窗口
                self.setGeometry(self.window().rect())  # 将组件的几何形状设置为主窗口的矩形
                self.show()  # 显示组件

        self.is_fullscreen = not self.is_fullscreen

    # 定义回调函数
    def on_interaction_callback(self, caller, event):
        self.show_home_button()

    def on_keypress_callback(self, obj, event):
        key = obj.GetKeySym()
        key = {
            'r': 'R',
            'h': 'H',
            't': 'T',
            'j': 'J',
            'plus': '+',
            'minus': '-'
        }.get(key, key)

        # 根据按键执行操作
        match key:
            case 'H':
                self.on_home_clicked()
            case '+':
                self.on_zoom_in_clicked()
            case '-':
                self.on_zoom_out_clicked()

        if self.key_prompts:
            self.key_prompts.keyPressed.emit(key)

    def change_theme(self, checked):
        self.is_change_theme = checked

        is_dark = isDarkTheme()
        is_dark = not is_dark if checked else is_dark
        self.vtk_manager.vtk_scene.set_inverse_theme_colors(checked)

        # 更新背景颜色
        bg_color = "#171717" if is_dark else "#E8E8E8"
        for bg_widget in self.bg_widgets:
            bg_widget.setStyleSheet(f"background-color: {bg_color};")

        # 更新按钮图标
        if isDarkTheme():
            theme = Theme.DARK if is_dark else Theme.LIGHT
            icons = {
                self.home_btn: FluentIcon.HOME,
                self.zoom_in_btn: FluentIcon.ZOOM_IN,
                self.zoom_out_btn: FluentIcon.ZOOM_OUT,
                self.full_screen_btn: FluentIcon.FULL_SCREEN
            }
            for btn, icon in icons.items():
                btn.setIcon(icon.icon(theme))

    def coordinate_action(self, checked):
        self.vtk_manager.vtk_scene.set_show_grid_lines(checked)
        self.bar.actions()[1].setToolTip(
            self.tr('Hide Coordinate System') if checked else self.tr('Show Coordinate System'))

    def screenshot_action(self):
        # 打开保存文件对话框，设置文件类型为 .png 格式
        directory = os.path.join(cfg.pm_image_export.value, 'screenshot.png')
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Save Screenshot"), directory,
            "Image Files (*.png)",
        )
        # 检查是否选择了文件路径
        if file_path:
            cfg.set(cfg.pm_image_export, os.path.dirname(file_path))
        else:
            return

        # 创建窗口到图像过滤器
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(self.vtk_widget.GetRenderWindow())

        # 创建PNG写入器
        png_writer = vtk.vtkPNGWriter()
        png_writer.SetFileName(file_path)
        png_writer.SetInputConnection(window_to_image_filter.GetOutputPort())

        # 更新过滤器
        window_to_image_filter.Update()

        # 写入PNG文件
        try:
            png_writer.Write()
        except Exception:
            file_path = ''

        # 发送保存截图信号
        self.saveScreenshot.emit(file_path)

    def refresh_action(self):
        self.refresh()

    def key_prompts_action(self):
        if self.key_prompts_bar is None:
            self.key_prompts_bar = self.create_key_prompts_bar()
            self.key_prompts_bar.show()
        else:
            self.key_prompts_bar.close()
            self.reset_key_prompts_bar()

    def create_key_prompts_bar(self):
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title=self.tr('Key Prompts'),
            content='',
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,
            parent=self
        )

        self.key_prompts = KeyPrompts()
        self.setup_key_prompts(self.key_prompts)

        w.addWidget(self.key_prompts)
        w.closedSignal.connect(self.reset_key_prompts_bar)

        return w

    def setup_key_prompts(self, key_prompts):
        key_prompts.addKeyActions([
            KeyAction('R', self.tr('Reset camera view'), triggered=self.reset_camera),
            KeyAction('H', self.tr('Switch to standard view'), triggered=self.on_home_clicked),
            KeyAction('T', self.tr('Switch to trackball interaction mode'),
                      triggered=self.set_trackball_interaction_mode),
            KeyAction('J', self.tr('Switch to joystick interaction mode'),
                      triggered=self.set_joystick_interaction_mode)
        ])

        key_prompts.addKeyActionGroup(
            actions=[
                KeyAction('+', triggered=self.on_zoom_in_clicked),
                KeyAction('-', triggered=self.on_zoom_out_clicked)
            ],
            group_description=self.tr('Zoom view')
        )

    def reset_key_prompts_bar(self):
        self.key_prompts_bar = None
        self.key_prompts = None

    def setting_action(self):
        self.openSetting.emit()

    def on_home_clicked(self):
        self.restore_default_view()
        self.home_bg.setHidden(True)

    def on_zoom_in_clicked(self):
        self.zoom_in()
        self.show_home_button()

    def on_zoom_out_clicked(self):
        self.zoom_out()
        self.show_home_button()

    def on_full_screen_clicked(self):
        self.toggle_fullscreen()

        icon = FluentIcon.BACK_TO_WINDOW if self.is_fullscreen else FluentIcon.FULL_SCREEN
        if isDarkTheme():
            is_dark = not isDarkTheme() if self.is_change_theme else isDarkTheme()
            self.full_screen_btn.setIcon(icon.icon(Theme.DARK if is_dark else Theme.LIGHT))
            self.full_screen_btn.setToolTip(
                self.tr('Exit Fullscreen') if self.is_fullscreen else self.tr('Enter Fullscreen'))

    def resizeEvent(self, event):
        VTKViewWidget.resizeEvent(self, event)
        MenuViewWidget.resizeEvent(self, event)
