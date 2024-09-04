from PySide6.QtWidgets import QWidget
from qfluentwidgets import ImageLabel, isDarkTheme


class ImageLabelCard(ImageLabel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.radius = 8

        self.setBorderRadius(self.radius, self.radius, self.radius, self.radius)

        self.setDashedBorder()

    def setDashedBorder(self):
        # 使用样式表设置虚线边框
        border_color = '#999999' if isDarkTheme() else '#666666'
        self.setStyleSheet(f"border: 2px dashed {border_color}; border-radius: {self.radius}px;")
