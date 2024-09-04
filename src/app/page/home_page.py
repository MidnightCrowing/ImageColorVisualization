from PySide6.QtWidgets import QWidget, QFileDialog

from src.vtk.vtk_manager import VTKManager
from ..ui.ui_HomePage import Ui_HomePage


class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.vtk_manager = VTKManager(self.vtk_widget)

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
        self.vtk_manager.set_image(image_path)

    def close_vtk(self):
        self.vtk_manager.close()

    def closeEvent(self, event):
        self.close_vtk()
        event.accept()
