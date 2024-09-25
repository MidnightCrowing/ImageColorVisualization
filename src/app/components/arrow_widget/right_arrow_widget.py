from typing import Optional

from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, QPolygon, QColor, QBrush, QPen
from PySide6.QtWidgets import QWidget
from qfluentwidgets import isDarkTheme, Theme, qconfig


class RightArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.brush_color: Optional[QColor] = None

        self.getBrushColor()
        self._connect_signals()

    def getBrushColor(self):
        self.brush_color = '#65656B' if isDarkTheme() else '#C9CBD4'

    def themeChanged(self, theme: Theme):
        self.brush_color = '#65656B' if theme == Theme.DARK else '#C9CBD4'
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 开启抗锯齿

        # 设置画笔颜色为与填充色一致（可选）
        pen = QPen(self.brush_color)
        pen.setWidth(0)  # 设置边框宽度为0，可以减少边缘突出感
        painter.setPen(pen)  # 方法1：设置边框颜色与填充颜色一致
        # painter.setPen(Qt.NoPen)  # 方法2：禁用边框

        # 获取当前组件的宽度和高度
        w = self.width()
        h = self.height()

        # 定义箭头的目标宽高比，防止箭头过于窄高
        target_aspect_ratio = 3.0  # 目标宽高比为3:1

        # 根据组件大小计算箭头的实际宽度和高度
        arrow_width = w * 0.8
        arrow_height = h * 0.6

        # 调整箭头的宽高比
        current_aspect_ratio = arrow_width / arrow_height
        if current_aspect_ratio < target_aspect_ratio:
            arrow_height = arrow_width / target_aspect_ratio
        else:
            arrow_width = arrow_height * target_aspect_ratio

        # 计算箭头在窗口中的位置居中
        left_x = int((w - arrow_width) / 2)
        right_x = int(left_x + arrow_width * 0.7)
        arrow_tip_x = int(left_x + arrow_width)
        mid_y = int(h / 2)
        thickness = int(max(arrow_height / 4, 10))

        # 定义箭头的多边形顶点
        arrow_polygon = QPolygon([
            QPoint(left_x, mid_y - thickness),  # 左上角
            QPoint(right_x, mid_y - thickness),  # 主干上方
            QPoint(right_x, mid_y - thickness * 2),  # 顶部尖角左侧
            QPoint(arrow_tip_x, mid_y),  # 箭头尖端
            QPoint(right_x, mid_y + thickness * 2),  # 底部尖角左侧
            QPoint(right_x, mid_y + thickness),  # 主干下方
            QPoint(left_x, mid_y + thickness)  # 左下角
        ])

        # 设置画刷为箭头颜色
        painter.setBrush(QBrush(self.brush_color))

        # 绘制箭头
        painter.drawPolygon(arrow_polygon)

    def _connect_signals(self):
        qconfig.themeChanged.connect(self.themeChanged)
