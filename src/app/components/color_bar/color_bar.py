from typing import List, Tuple

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QColor, QMouseEvent, QPainter
from PySide6.QtWidgets import QLabel, QWidget
from qfluentwidgets import ToolTipFilter, ToolTipPosition


class ColorBar(QLabel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._colors = []  # 存储颜色列表
        self._color_rects = []  # 存储颜色块的矩形区域
        self.setMouseTracking(True)  # 开启鼠标追踪以捕捉悬停事件
        self.tooltip_text = None  # 当前工具提示文本
        self._hover_index = None  # 当前悬停的颜色块索引
        self._zoom_factor = 0.15  # 缩放比例
        self._tooltip_filter = ToolTipFilter(self, showDelay=-1, position=ToolTipPosition.TOP)  # 工具提示过滤器

        # 将工具提示过滤器安装到颜色条上
        self.installEventFilter(self._tooltip_filter)

        # 初始化全局和局部动画
        easing_curve = QEasingCurve.OutCubic  # 平滑动画曲线
        self._global_zoom_level = 0  # 全局缩放动画级别
        self._global_animation = QPropertyAnimation(self, b"globalZoomValue")
        self._global_animation.setDuration(300)  # 动画持续时间
        self._global_animation.setEasingCurve(easing_curve)

        self._local_zoom_level = 0  # 局部缩放动画级别
        self._local_animation = QPropertyAnimation(self, b"localZoomValue")
        self._local_animation.setDuration(300)  # 动画持续时间
        self._local_animation.setEasingCurve(easing_curve)

    def setColors(self, colors: List[Tuple[int, int, int]]):
        """根据亮度对颜色进行排序并更新颜色列表"""
        self._colors = self._sort_colors_by_brightness(colors)
        self.update()

    def colors(self) -> List[Tuple[int, int, int]]:
        """返回颜色列表"""
        return self._colors

    def removeColors(self):
        """重置颜色列表并更新组件"""
        self._colors = []  # 清空颜色列表
        self._color_rects = []  # 清空颜色块的矩形区域
        self._hover_index = None  # 重置悬停的颜色块索引
        self.update()  # 更新组件以重绘

    def setZoomFactor(self, value: float):
        """设置缩放比例"""
        self._zoom_factor = value

    def zoomFactor(self) -> float:
        return self._zoom_factor

    def _get_global_zoom_value(self):
        return self._global_zoom_level

    def _set_global_zoom_value(self, value):
        self._global_zoom_level = value
        self.update()  # 每次修改缩放级别时重绘

    globalZoomValue = Property(float, _get_global_zoom_value, _set_global_zoom_value)

    def _get_local_zoom_value(self):
        return self._local_zoom_level

    def _set_local_zoom_value(self, value):
        self._local_zoom_level = value
        self.update()

    localZoomValue = Property(float, _get_local_zoom_value, _set_local_zoom_value)

    def _sort_colors_by_brightness(self, colors):
        """按亮度对颜色进行排序"""

        def brightness(color):
            return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

        return sorted(colors, key=brightness, reverse=True)

    def paintEvent(self, event):
        """自定义绘制事件，用于绘制颜色块"""
        super().paintEvent(event)
        if not self._colors:
            return

        painter = QPainter(self)
        widget_width, widget_height = self.width(), self.height()
        num_colors = len(self._colors)

        # 计算每个颜色块的基础尺寸和全局缩放值
        base_size = min(widget_width // num_colors, widget_height)
        zoom_offset = int(base_size * self._global_zoom_level)

        # 调整后的宽高，防止颜色块溢出边界
        adjusted_width = widget_width - zoom_offset * 2
        adjusted_height = widget_height - zoom_offset * 2
        box_size = min(adjusted_width // num_colors, adjusted_height)

        # 计算颜色条的总宽度及其起始位置，使其居中显示
        total_width = box_size * num_colors
        start_x = (adjusted_width - total_width) // 2 + zoom_offset
        start_y = (adjusted_height - box_size) // 2 + zoom_offset

        self._color_rects = []  # 存储每个颜色块的矩形区域

        # 绘制颜色块
        for i, color in enumerate(self._colors):
            if i == self._hover_index:
                # 跳过悬停的颜色块，稍后绘制
                self._color_rects.append(None)
                continue

            x_pos = start_x + i * box_size
            rect = QRect(x_pos, start_y, box_size, box_size)
            self._color_rects.append(rect)
            painter.fillRect(rect, QColor(*color))

        # 绘制悬停的颜色块，添加局部缩放效果
        if self._hover_index is not None:
            hover_color = self._colors[self._hover_index]
            x_pos = start_x + self._hover_index * box_size
            local_zoom_offset = int(base_size * self._local_zoom_level)
            rect = QRect(x_pos - local_zoom_offset, start_y - local_zoom_offset,
                         box_size + local_zoom_offset * 2, box_size + local_zoom_offset * 2)
            self._color_rects[self._hover_index] = rect
            painter.fillRect(rect, QColor(*hover_color))

    def mouseMoveEvent(self, event: QMouseEvent):
        """根据鼠标位置更新工具提示并启动动画"""
        mouse_pos = event.position().toPoint()
        tooltip_changed = False

        for i, rect in enumerate(self._color_rects):
            if rect and rect.contains(mouse_pos):
                color = self._colors[i]
                color_hex = '#%02x%02x%02x' % tuple(color)
                tooltip_text = f'{self.tr('Color')}: {color_hex}'
                if self.tooltip_text != tooltip_text:
                    # 鼠标进入新的颜色块
                    self._set_tooltip(tooltip_text)
                    if self._local_animation.state() != QPropertyAnimation.Running:
                        self._local_animation.setStartValue(0)  # 从当前缩放开始动画
                        self._local_animation.setEndValue(self._zoom_factor)  # 设置最终缩放值
                        self._local_animation.start()
                tooltip_changed = True

                # 如果当前悬停的颜色块发生变化，更新索引并启动全局缩放动画
                if self._hover_index != i:
                    self._hover_index = i
                    self._global_animation.setStartValue(self._global_zoom_level)
                    self._global_animation.setEndValue(self._zoom_factor)
                    self._global_animation.start()
                break

        if not tooltip_changed:
            # 鼠标移出所有颜色块
            self._reset_tooltip()
            if self._hover_index is not None:
                # 重置局部和全局缩放动画
                self._local_animation.setStartValue(self._local_zoom_level)
                self._local_animation.setEndValue(0)
                self._local_animation.start()
                self._global_animation.setStartValue(self._global_zoom_level)
                self._global_animation.setEndValue(0)
                self._global_animation.start()
                self._hover_index = None

    def _set_tooltip(self, text: str):
        """设置工具提示文本"""
        self.tooltip_text = text
        self.setToolTip(text)
        if self._tooltip_filter:
            self._tooltip_filter.hideToolTip()
            self._tooltip_filter.isEnter = True
            self._tooltip_filter._tooltip = self._tooltip_filter._createToolTip()
            self._tooltip_filter._tooltip.setDuration(-1)
            self._tooltip_filter.showToolTip()

    def _reset_tooltip(self):
        """当鼠标移出颜色块时，重置工具提示文本"""
        self.tooltip_text = None
        self.setToolTip('')  # 清除工具提示
        if self._tooltip_filter:
            self._tooltip_filter.hideToolTip()
