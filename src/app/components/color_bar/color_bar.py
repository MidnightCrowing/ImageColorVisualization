from typing import Tuple, List

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, Property
from PySide6.QtGui import QColor, QMouseEvent, QPainter
from PySide6.QtWidgets import QWidget, QLabel


class ColorBar(QLabel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.colors = []  # 存储颜色列表
        self.color_rects = []  # 存储颜色块的矩形区域
        self.setMouseTracking(True)  # 开启鼠标追踪以捕捉悬停事件
        self.tooltip_text = None  # 当前工具提示文本
        self.tooltip_filter = None  # 工具提示过滤器
        self.hover_index = None  # 当前悬停的颜色块索引
        self.zoom_factor = 0.05  # 缩放比例

        # 初始化全局和局部动画
        easing_curve = QEasingCurve.OutCubic  # 平滑动画曲线
        self.global_zoom_level = 0  # 全局缩放动画级别
        self.global_animation = QPropertyAnimation(self, b"globalZoomValue")
        self.global_animation.setDuration(300)  # 动画持续时间
        self.global_animation.setEasingCurve(easing_curve)

        self.local_zoom_level = 0  # 局部缩放动画级别
        self.local_animation = QPropertyAnimation(self, b"localZoomValue")
        self.local_animation.setDuration(300)  # 动画持续时间
        self.local_animation.setEasingCurve(easing_curve)

    def setColors(self, colors: List[Tuple[int, int, int]]):
        """根据亮度对颜色进行排序并更新颜色列表"""
        self.colors = self.sort_colors_by_brightness(colors)
        self.update()

    def setZoomFactor(self, value: float):
        """设置缩放比例"""
        self.zoom_factor = value

    def zoomFactor(self) -> float:
        return self.zoom_factor

    def get_global_zoom_value(self):
        return self.global_zoom_level

    def set_global_zoom_value(self, value):
        self.global_zoom_level = value
        self.update()  # 每次修改缩放级别时重绘

    globalZoomValue = Property(float, get_global_zoom_value, set_global_zoom_value)

    def get_local_zoom_value(self):
        return self.local_zoom_level

    def set_local_zoom_value(self, value):
        self.local_zoom_level = value
        self.update()

    localZoomValue = Property(float, get_local_zoom_value, set_local_zoom_value)

    def sort_colors_by_brightness(self, colors):
        """按亮度对颜色进行排序"""

        def brightness(color):
            return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

        return sorted(colors, key=brightness, reverse=True)

    def paintEvent(self, event):
        """自定义绘制事件，用于绘制颜色块"""
        super().paintEvent(event)
        if not self.colors:
            return

        painter = QPainter(self)
        widget_width, widget_height = self.width(), self.height()
        num_colors = len(self.colors)

        # 计算每个颜色块的基础尺寸和全局缩放值
        base_size = min(widget_width // num_colors, widget_height)
        zoom_offset = int(base_size * self.global_zoom_level)

        # 调整后的宽高，防止颜色块溢出边界
        adjusted_width = widget_width - zoom_offset * 2
        adjusted_height = widget_height - zoom_offset * 2
        box_size = min(adjusted_width // num_colors, adjusted_height)

        # 计算颜色条的总宽度及其起始位置，使其居中显示
        total_width = box_size * num_colors
        start_x = (adjusted_width - total_width) // 2 + zoom_offset
        start_y = (adjusted_height - box_size) // 2 + zoom_offset

        self.color_rects = []  # 存储每个颜色块的矩形区域

        # 绘制颜色块
        for i, color in enumerate(self.colors):
            if i == self.hover_index:
                # 跳过悬停的颜色块，稍后绘制
                self.color_rects.append(None)
                continue

            x_pos = start_x + i * box_size
            rect = QRect(x_pos, start_y, box_size, box_size)
            self.color_rects.append(rect)
            painter.fillRect(rect, QColor(*color))

        # 绘制悬停的颜色块，添加局部缩放效果
        if self.hover_index is not None:
            hover_color = self.colors[self.hover_index]
            x_pos = start_x + self.hover_index * box_size
            local_zoom_offset = int(base_size * self.local_zoom_level)
            rect = QRect(x_pos - local_zoom_offset, start_y - local_zoom_offset,
                         box_size + local_zoom_offset * 2, box_size + local_zoom_offset * 2)
            self.color_rects[self.hover_index] = rect
            painter.fillRect(rect, QColor(*hover_color))

    def reset_tooltip(self):
        """当鼠标移出颜色块时，重置工具提示文本"""
        self.tooltip_text = None
        self.setToolTip('')  # 清除工具提示
        if self.tooltip_filter:
            self.tooltip_filter.hideToolTip()

    def mouseMoveEvent(self, event: QMouseEvent):
        """根据鼠标位置更新工具提示并启动动画"""
        mouse_pos = event.position().toPoint()
        tooltip_changed = False

        for i, rect in enumerate(self.color_rects):
            if rect and rect.contains(mouse_pos):
                color = self.colors[i]
                color_hex = '#%02x%02x%02x' % tuple(color)
                tooltip_text = f'Color: {color_hex}'
                if self.tooltip_text != tooltip_text:
                    # 鼠标进入新的颜色块
                    self.tooltip_text = tooltip_text
                    self.setToolTip(tooltip_text)
                    if self.tooltip_filter:
                        self.tooltip_filter.hideToolTip()
                        self.tooltip_filter.isEnter = True
                        self.tooltip_filter._tooltip = self.tooltip_filter._createToolTip()
                        self.tooltip_filter._tooltip.setDuration(-1)
                        self.tooltip_filter.showToolTip()
                    if self.local_animation.state() != QPropertyAnimation.Running:
                        self.local_animation.setStartValue(0)  # 从当前缩放开始动画
                        self.local_animation.setEndValue(self.zoom_factor)  # 设置最终缩放值
                        self.local_animation.start()
                tooltip_changed = True

                # 如果当前悬停的颜色块发生变化，更新索引并启动全局缩放动画
                if self.hover_index != i:
                    self.hover_index = i
                    self.global_animation.setStartValue(self.global_zoom_level)
                    self.global_animation.setEndValue(self.zoom_factor)
                    self.global_animation.start()
                break

        if not tooltip_changed:
            # 鼠标移出所有颜色块
            self.reset_tooltip()
            if self.hover_index is not None:
                # 重置局部和全局缩放动画
                self.local_animation.setStartValue(self.local_zoom_level)
                self.local_animation.setEndValue(0)
                self.local_animation.start()
                self.global_animation.setStartValue(self.global_zoom_level)
                self.global_animation.setEndValue(0)
                self.global_animation.start()
                self.hover_index = None
