from PySide6.QtWidgets import QWidget

from ..ui.ui_ImitatePage import Ui_ImitatePage


class ImitatePage(QWidget, Ui_ImitatePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
