from __future__ import annotations

from typing import Union, Optional

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import InfoBar, InfoBarPosition, PushButton, StateToolTip

from src.image_color_analyzer import extract_dominant_colors, export_chart
from src.point_cloud import VTKManager
from src.utils.reveal_file import reveal_file
from ..ui.ui_HomePage import Ui_HomePage


class ImageLoader(QThread):
    """线程类，用于加载图像并处理相关数据"""
    loaded = Signal(str)
    finished = Signal()

    def __init__(self, parent_widget: HomePage):
        super().__init__()
        self.parent_widget = parent_widget
        self.image_path = None

    def set_image_path(self, image_path: str):
        """设置要加载的图像路径"""
        self.image_path = image_path

    def run(self):
        """执行加载图像的操作"""
        self.loaded.emit(self.image_path)
        self.parent_widget.show_dominant_colors(self.image_path)
        self.parent_widget.cloud_actor.set_image(self.image_path)


class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.vtk_manager = VTKManager(self.vtk_widget)
        self.cloud_actor = self.vtk_manager.add_null_cloud_actor()

        # 创建图像加载线程并连接信号
        self.image_loader = ImageLoader(self)

        self.state_tooltip: Optional[StateToolTip] = None  # 状态提示框

        # 连接信号与槽函数
        self._connect_signal()

    def _connect_signal(self):
        self.export_chart_btn.clicked.connect(self.export_chart)
        self.export_point_cloud_btn.clicked.connect(self.export_point_cloud)
        self.import_point_cloud_btn.clicked.connect(self.import_point_cloud)
        self.image_loader.loaded.connect(self.on_image_loaded)
        self.image_loader.finished.connect(self.image_load_finished)

    def open_file_dialog(self):
        # 打开文件选择对话框，设置文件类型为常见的图片格式
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.update_image(file_path)

    def update_image(self, image_path: str):
        """更新图像并显示状态提示框"""
        self.state_tooltip = StateToolTip(self.tr('正在加载图片'), self.tr('客官请耐心等待哦~~'), self)
        self.move_state_tooltip()
        self.state_tooltip.show()

        self.image_loader.set_image_path(image_path)
        self.image_loader.start()

    def on_image_loaded(self, image_path: str):
        """处理图像加载完成后的操作"""
        self.image_display_area.setImage(image_path)
        self.image_display_area.scaledToHeight(140)

    def image_load_finished(self):
        """处理图像加载完成后的状态更新"""
        self.vtk_manager.render()
        self.state_tooltip.setContent(self.tr('图片加载完成啦 😆'))
        self.state_tooltip.setState(True)
        self.state_tooltip = None

    def move_state_tooltip(self):
        """移动状态提示框到指定位置"""
        if self.state_tooltip:
            self.state_tooltip.move((self.width() - self.state_tooltip.width()) // 2, 5)

    def show_dominant_colors(self, image_path: str):
        """Extract and display dominant colors in the ColorBar"""
        dominant_colors = extract_dominant_colors(image_path)
        self.color_bar.setColors(dominant_colors)

    def export_chart(self):
        # 打开保存文件对话框，设置文件类型为 .png 格式
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Export Chart"), "color chart.png",
            "Image Files (*.png)",
        )
        # 检查是否选择了文件路径
        if not file_path:
            return

        colors = self.color_bar.colors()
        if colors:
            export_chart(colors, file_path)
            w = self.show_info_bar(
                InfoBar.warning,
                title=self.tr('Export Chart'),
                content=self.tr("Color chart saved successfully"),
            )
            btn = PushButton(text=self.tr('Open Directory'))
            btn.clicked.connect(lambda: reveal_file(file_path))
            w.addWidget(btn)
            w.show()
        else:
            self.show_info_bar(
                InfoBar.warning,
                title=self.tr('Export Chart'),
                content=self.tr("No colors to export")
            )

    def import_point_cloud(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Import Point Cloud"), "",
            "Point Cloud Files (*.ply *.vtk)")

        if file_path:
            is_open, msg = self.cloud_actor.import_point_cloud(file_path)
            if not is_open:
                self.show_import_result(file_path, msg)
            else:
                self.image_display_area.removeImage()

    def export_point_cloud(self):
        """
        导出点云文件到指定路径，并显示操作结果。
        """
        # 打开保存文件对话框，支持 .ply 和 .vtk 格式
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Export Point Cloud"), "",
            "Point Cloud Files (*.ply *.vtk)"
        )

        # 检查是否选择了文件路径
        if file_path:
            # 尝试导出点云文件
            is_written = self.cloud_actor.export_point_cloud(file_path)

            # 根据导出结果显示提示信息
            self.show_export_result(is_written, file_path)

    def show_import_result(self, file_path: str, msg: str):
        # 使用字典来映射错误类型和对应的消息
        error_message_mapping = {
            "FileNotFoundError": self.tr("File not found, please check the path or file name."),
            "PermissionError": self.tr("File cannot be accessed, please check file permissions."),
            "IsADirectoryError": self.tr("Cannot open directory, please select a file.")
        }

        # 获取对应的错误消息，如果没有则使用默认消息
        message = error_message_mapping.get(msg, self.tr("Failed to open the file"))

        # 显示 InfoBar 警告
        self.show_info_bar(
            InfoBar.warning,
            title=self.tr('Import Point Cloud'),
            content=f"{message}: {file_path}"
        )

    def show_export_result(self, is_written: bool, file_path: str):
        """
        根据点云导出结果显示成功或失败的提示信息。

        :param is_written: 点云是否成功写入文件
        :param file_path: 导出的文件路径
        """
        # 成功时显示成功信息，失败时显示警告信息
        if is_written:
            w = self.show_info_bar(
                InfoBar.warning,
                title=self.tr('Export Point Cloud'),
                content=f"{self.tr("Point cloud saved successfully")}: {file_path}"
            )
            btn = PushButton(text=self.tr('Open Directory'))
            btn.clicked.connect(lambda: reveal_file(file_path))
            w.addWidget(btn)
            w.show()
        else:
            self.show_info_bar(
                InfoBar.warning,
                title=self.tr('Export Point Cloud'),
                content=f"{self.tr("Failed to save the file")}: {file_path}"
            )

    def show_info_bar(self,
                      bar_type: Union[InfoBar.info, InfoBar.success, InfoBar.warning, InfoBar.error],
                      title: str,
                      content: str,
                      orient: Union[Qt.Vertical, Qt.Horizontal] = Qt.Vertical,
                      is_closable: bool = True,
                      position: InfoBarPosition = InfoBarPosition.TOP_RIGHT,
                      duration: int = 5000):
        w = bar_type(
            title=title,
            content=content,
            orient=orient,
            isClosable=is_closable,
            position=position,
            duration=duration,
            parent=self
        )
        return w

    def close_vtk(self):
        self.vtk_manager.close()

    def closeEvent(self, event):
        self.close_vtk()
        event.accept()

    def resizeEvent(self, event):
        self.move_state_tooltip()
        event.accept()
