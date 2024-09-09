from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ImageLabel, isDarkTheme, IconWidget

from ...common.icon import Icon


class ImageLabelCard(ImageLabel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.radius = 8

        # 设置 ImageLabelCard 的外观
        self.setBorderRadius(self.radius, self.radius, self.radius, self.radius)
        self.setDashedBorder()

        # 设置图标
        self._setup_icon()

    def setDashedBorder(self):
        # 使用样式表设置虚线边框
        border_color = '#65656B' if isDarkTheme() else '#C9CBD4'
        self.setStyleSheet(f"border: 2px dashed {border_color}; border-radius: {self.radius}px;")

    def _setup_icon(self):
        # 创建 IconWidget 并设置图标
        self.icon = IconWidget(self)
        self.icon.setIcon(Icon.SelectImage)
        self.icon.setFixedSize(48, 48)

        # 创建一个布局管理器来实现居中
        icon_layout = QVBoxLayout(self)
        icon_layout.addWidget(self.icon)

        # 设置布局中的 widget 居中
        icon_layout.setAlignment(self.icon, Qt.AlignCenter)  # 设置水平和垂直居中对齐

    def setImage(self, image: Union[str, QPixmap, QImage] = None):
        super().setImage(image)
        self.icon.hide()  # 隐藏图标，当设置新图片时

    def removeImage(self):
        size = self.size()
        super().setImage()  # 清除 ImageLabel 的图片
        self.setFixedSize(size)
        self.icon.show()  # 显示图标以代替图像
