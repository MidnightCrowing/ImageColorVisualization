from PySide6.QtWidgets import QWidget

from src.vtk.vtk_manager import VTKManager
from ..ui.ui_ComparePage import Ui_ComparePage


class ComparePage(QWidget, Ui_ComparePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.img_label_1.setBorderRadius(8, 8, 8, 8)
        self.img_label_2.setBorderRadius(8, 8, 8, 8)

        self.vtk_manger_1 = VTKManager(self.vtk_widget_1)
        self.vtk_manger_2 = VTKManager(self.vtk_widget_2)

    def close_vtk(self):
        self.vtk_manger_1.close()
        self.vtk_manger_2.close()
