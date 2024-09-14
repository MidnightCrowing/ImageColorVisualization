from typing import Optional, List

from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPalette
from PySide6.QtWidgets import QWidget
from qfluentwidgets import themeColor, isDarkTheme, Theme, qconfig
from qfluentwidgets.common.icon import toQIcon, FluentIcon


class StepProgressBar(QWidget):
    """步骤进度条组件，显示多个步骤的进度和状态"""

    def __init__(self, steps=None, current_step: int = 0, line_width: int = 5, font_size=12, parent=None):
        """
        初始化步骤进度条

        :param steps: 步骤名称列表
        :param current_step: 当前激活的步骤索引
        :param line_width: 连接线宽度
        :param font_size: 字体大小
        :param parent: 父级窗口
        """
        super().__init__(parent)
        self.steps = steps or []  # 步骤名称列表
        self._current_step = current_step  # 当前步骤索引
        self.line_width = line_width  # 连接线宽度
        self.font_size = font_size  # 字体大小
        self._progress = 0.0  # 用于控制线条动画进度的属性

        # 初始化颜色属性
        self.active_color: Optional[QColor] = None
        self.inactive_color: Optional[QColor] = None
        self.label_color: Optional[QColor] = None
        self.background_color: Optional[QColor] = None

        # 创建动画对象
        self.animation = QPropertyAnimation(self, b"progress")
        self.animation.setDuration(400)  # 动画持续时间（毫秒）
        self.animation.setEasingCurve(QEasingCurve.OutCirc)  # 动画效果

        self._initializeColors()
        self._configureBackground()
        self._connect_signals()

    @Property(float)
    def progress(self) -> float:
        """进度属性，用于动画"""
        return self._progress

    @progress.setter
    def progress(self, value: float):
        self._progress = value
        self.update()  # 更新UI以触发重绘

    @Property(int)
    def currentStep(self) -> int:
        """当前步骤属性"""
        return self._current_step

    @currentStep.setter
    def currentStep(self, step_index: int):
        """设置当前步骤并更新UI"""
        self._current_step = step_index
        self.update()

    def setSteps(self, steps: List[str]):
        """设置步骤名称列表"""
        self.steps = steps
        self.update()

    def setCurrentStep(self, step_index: int, animate: bool = True):
        """
        设置当前步骤并启动线条动画
        :param step_index: 目标步骤索引
        """
        if step_index == self._current_step:
            return  # 如果步骤未变化，不触发动画

        # 启动连接线的动画
        if step_index > 1 and animate:
            self.animation.setStartValue(self._progress)
            self.animation.setEndValue(step_index - self._current_step)
            self.animation.start()
            self.animation.finished.connect(lambda: self._onAnimationFinished(step_index))
        else:
            self._onAnimationFinished(step_index)

    def getCurrentStep(self) -> int:
        """获取当前步骤索引"""
        return self._current_step

    def _onAnimationFinished(self, step_index: int):
        """动画完成后重置进度并更新步骤"""
        self._progress = 0.0  # 重置进度
        self._current_step = step_index  # 更新当前步骤
        self.update()

    def _initializeColors(self):
        """初始化颜色主题"""
        self.active_color = themeColor()  # 使用主题色作为激活颜色
        if isDarkTheme():
            self.inactive_color = QColor("#272727")
            self.label_color = QColor("#FFFFFF")
        else:
            self.inactive_color = QColor("#E6E8EA")
            self.label_color = QColor("#000000")
        self.background_color = QColor("transparent")

    def _configureBackground(self):
        """配置背景颜色"""
        palette = self.palette()
        palette.setColor(QPalette.Window, self.background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)  # 自动填充背景

    def _connect_signals(self):
        """连接主题变化的信号"""
        qconfig.themeChanged.connect(self._onThemeChanged)
        qconfig.themeColorChanged.connect(self._onThemeColorChanged)

    def _onThemeChanged(self, theme: Theme):
        """处理主题变化"""
        if theme == Theme.DARK:
            self.inactive_color = QColor("#272727")
            self.label_color = QColor("#FFFFFF")
        else:
            self.inactive_color = QColor("#E6E8EA")
            self.label_color = QColor("#000000")
        self.update()

    def _onThemeColorChanged(self, theme_color: QColor):
        """处理主题颜色变化"""
        self.active_color = theme_color
        self.update()

    def paintEvent(self, event):
        """重写的绘制事件，用于绘制步骤进度条"""
        if not self.steps:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        step_width = self.width() / len(self.steps)  # 每个步骤的宽度
        indicator_height = self.height() / 3  # 圆形指示器的高度
        radius = min(step_width, indicator_height) / 2  # 圆的半径
        centerX = step_width / 2  # 起始 X 坐标
        centerY = indicator_height  # 圆形中心的 Y 坐标

        # 绘制连接线
        painter.setBrush(Qt.NoBrush)
        for i in range(len(self.steps) - 1):
            line_color = self.active_color if i < self._current_step else self.inactive_color
            painter.setPen(QPen(line_color, self.line_width, Qt.SolidLine, Qt.RoundCap))

            if i == self._current_step - 1:
                # 动画效果，控制线条长度
                line_end_x = centerX + step_width * self._progress
                painter.drawLine(centerX, int(centerY), line_end_x, int(centerY))
                # 剩余未激活部分
                line_color = self.inactive_color
                painter.setPen(QPen(line_color, self.line_width, Qt.SolidLine, Qt.RoundCap))
                painter.drawLine(line_end_x, int(centerY), centerX + step_width, int(centerY))
            else:
                painter.drawLine(centerX, int(centerY), centerX + step_width, int(centerY))

            centerX += step_width

        # 绘制步骤指示器
        centerX = step_width / 2
        font = QFont("Microsoft YaHei UI", self.font_size)
        painter.setFont(font)
        for i, step in enumerate(self.steps):
            if i < self._current_step:
                painter.setBrush(self.active_color)
            else:
                painter.setBrush(self.inactive_color)
            painter.setPen(Qt.NoPen)

            # 绘制圆形指示器
            painter.drawEllipse(QRectF(centerX - radius, centerY - radius, radius * 2, radius * 2))

            # 激活状态下显示图标，否则显示步骤编号
            if i < self._current_step:
                icon = toQIcon(FluentIcon.ACCEPT)
                icon.paint(painter, int(centerX - radius / 2), int(centerY - radius / 2), int(radius), int(radius))
            else:
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
