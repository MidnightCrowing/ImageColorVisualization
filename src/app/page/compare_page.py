from PySide6.QtWidgets import QWidget

from ..ui.ui_ComparePage import Ui_ComparePage


class ComparePage(QWidget, Ui_ComparePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

