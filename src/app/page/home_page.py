from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import InfoBar, InfoBarPosition

from src.point_cloud import VTKManager
from ..ui.ui_HomePage import Ui_HomePage


class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.vtk_manager = VTKManager(self.vtk_widget)
        self.cloud_actor = self.vtk_manager.add_null_cloud_actor()

        # 连接信号与槽函数
        self._connect_signal()

    def _connect_signal(self):
        self.export_chart_btn.clicked.connect(self.export_chart)
        self.export_point_cloud_btn.clicked.connect(self.export_point_cloud)
        self.import_point_cloud_btn.clicked.connect(self.import_point_cloud)

    def open_file_dialog(self):
        # 打开文件选择对话框，设置文件类型为常见的图片格式
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.update_image(file_path)

    def update_image(self, image_path: str):
        self.image_display_area.setImage(image_path)
        self.image_display_area.scaledToHeight(140)
        self.cloud_actor.set_image(image_path)

    def export_chart(self):
        # TODO: 导出图表
        pass

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
        InfoBar.warning(
            title=self.tr('Import Point Cloud'),
            content=f"{message}: {file_path}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )

    def show_export_result(self, is_written: bool, file_path: str):
        """
        根据点云导出结果显示成功或失败的提示信息。

        :param is_written: 点云是否成功写入文件
        :param file_path: 导出的文件路径
        """
        # 成功时显示成功信息，失败时显示警告信息
        if is_written:
            message = self.tr("Point cloud saved successfully")
            info_bar_type = InfoBar.success
        else:
            message = self.tr("Failed to save the file")
            info_bar_type = InfoBar.warning

        info_bar_type(
            title=self.tr('Export Point Cloud'),
            content=f"{message}: {file_path}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )

    def close_vtk(self):
        self.vtk_manager.close()

    def closeEvent(self, event):
        self.close_vtk()
        event.accept()
