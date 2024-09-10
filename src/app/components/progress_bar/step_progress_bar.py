from typing import Optional, List

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPalette
from PySide6.QtWidgets import QWidget
from qfluentwidgets import themeColor, isDarkTheme, Theme, qconfig
from qfluentwidgets.common.icon import toQIcon, FluentIcon


class StepProgressBar(QWidget):
    def __init__(self, steps=None, current_step: int = 0, line_width: int = 5, font_size=12, parent=None):
        """
        步骤进度条组件，用于显示多个步骤的进度

        :param steps: 步骤名称列表
        :param current_step: 当前激活的步骤索引
        :param line_width: 连接线宽度
        :param font_size: 字体大小
        :param parent: 父级窗口
        """
        super().__init__(parent)
        if steps is None:
            steps = []
        self.steps = steps  # 步骤名称列表
        self.current_step = current_step  # 当前激活的步骤索引
        self.line_width = line_width  # 连接线宽度
        self.font_size = font_size  # 字体大小
        self.active_color: Optional[QColor] = None  # 激活状态颜色
        self.inactive_color: Optional[QColor] = None  # 未激活状态颜色
        self.label_color: Optional[QColor] = None  # 标签颜色
        self.background_color: Optional[QColor] = None  # 背景颜色

        self.getThemeColor()
        self.paintBackground()
        self._connect_signals()

    def setSteps(self, steps: List[str]):
        self.steps = steps
        self.update()  # 重新绘制组件

    def getThemeColor(self):
        self.active_color = themeColor()
        if isDarkTheme():
            self.inactive_color = QColor("#272727")
            self.label_color = QColor("#FFFFFF")
        else:
            self.inactive_color = QColor("#E6E8EA")
            self.label_color = QColor("#000000")
        self.background_color = QColor("transparent")

    def themeChanged(self, theme: Theme):
        if theme == Theme.DARK:
            self.inactive_color = QColor("#202020")
            self.label_color = QColor("#FFFFFF")
        else:
            self.inactive_color = QColor("#E6E8EA")
            self.label_color = QColor("#000000")
        self.update()

    def themeColorChanged(self, theme_color: QColor):
        self.active_color = theme_color
        self.update()

    def setCurrentStep(self, step_index: int):
        """设置当前步骤并刷新界面"""
        self.current_step = step_index
        self.update()  # 重新绘制组件

    def paintEvent(self, event):
        """重写的绘制事件，用于绘制步骤进度条"""
        if len(self.steps) == 0:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        step_width = self.width() / len(self.steps)  # 每个步骤的宽度
        indicator_height = self.height() / 3  # 计算高度用于居中对齐
        radius = min(step_width, indicator_height) / 2  # 圆的半径
        centerX = step_width / 2  # 初始化 X 坐标
        centerY = indicator_height  # 初始化 Y 坐标

        # 绘制背景和连接线
        painter.setBrush(Qt.NoBrush)
        for i in range(len(self.steps) - 1):
            line_color = self.active_color if i < self.current_step - 1 else self.inactive_color
            painter.setPen(QPen(line_color, self.line_width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(centerX, int(centerY), centerX + step_width, int(centerY))
            centerX += step_width

        # 重置 X 坐标以绘制圆形指示器和编号
        centerX = step_width / 2
        font = QFont("Microsoft YaHei UI", self.font_size)
        painter.setFont(font)
        for i in range(len(self.steps)):
            # 设置指示器颜色
            if i < self.current_step:
                painter.setBrush(self.active_color)
            else:
                painter.setBrush(self.inactive_color)
            painter.setPen(Qt.NoPen)

            # 绘制指示器圆形
            painter.drawEllipse(QRectF(centerX - radius, centerY - radius, radius * 2, radius * 2))

            # 绘制步骤编号或图标
            if i < self.current_step:
                # 激活状态显示图标
                icon = toQIcon(FluentIcon.ACCEPT)
                icon.paint(painter, int(centerX - radius / 2), int(centerY - radius / 2), int(radius), int(radius))
            else:
                # 未激活状态显示编号
                painter.setPen(self.label_color)
                painter.drawText(QRectF(centerX - radius, centerY - radius, radius * 2, radius * 2),
                                 Qt.AlignCenter, str(i + 1))

            centerX += step_width

        # 绘制步骤标签
        painter.setPen(self.label_color)
        centerX = step_width / 2
        for step_name in self.steps:
            text_rect = QRectF(centerX - step_width / 2, centerY + radius + 5, step_width, indicator_height * 2)
            painter.drawText(text_rect, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, step_name)
            centerX += step_width

    def paintBackground(self):
        """绘制背景"""
        # 创建调色板并设置背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, self.background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 自动填充背景

    def _connect_signals(self):
        qconfig.themeChanged.connect(self.themeChanged)
        qconfig.themeColorChanged.connect(self.themeColorChanged)
