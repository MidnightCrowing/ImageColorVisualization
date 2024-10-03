from typing import Callable, Dict, List, Tuple

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, QTimer, Qt, Signal, SignalInstance
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget, themeColor


def getRGBA(color: QColor) -> Tuple[int, int, int, int]:
    return color.red(), color.green(), color.blue(), color.alpha()


class KeyAction:
    def __init__(self, key: str, content: str = None, triggered: Callable = None):
        """
        表示一个按键操作。

        :param key: 快捷键字符
        :param content: 操作描述
        :param triggered: 点击按钮时执行的回调函数
        """
        self.key = key
        self.content = content
        self.triggered = triggered


class KeyCard(CardWidget):
    highlight = Signal()

    def __init__(self, parent: QWidget = None, text: str = None):
        self.animation_value = 0
        self.is_highlighted = False
        super().__init__(parent)
        self.setMinimumHeight(30)

        self.label = BodyLabel()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setAlignment(Qt.AlignCenter)  # 设置对齐方式为居中
        self.layout.addWidget(self.label)

        if text:
            self.setText(text)

        self.highlight_animation = QPropertyAnimation(self, b"highlightValue")
        self.highlight_animation.setDuration(300)
        self.highlight_animation.setEasingCurve(QEasingCurve.OutExpo)
        self.highlight_animation.setEndValue(1)

        self.reset_animation = QPropertyAnimation(self, b"highlightValue")
        self.reset_animation.setDuration(700)
        self.reset_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.reset_animation.setEndValue(0)

        self.highlight.connect(self.toggleHighlight)

    def get_highlight_value(self):
        return self.animation_value

    def set_highlight_value(self, value):
        self.animation_value = value
        self.setBackgroundColor(self.calculateColor())
        self.update()

    highlightValue = Property(float, get_highlight_value, set_highlight_value)

    def setText(self, text: str):
        self.label.setText(text)
        if len(text) == 1:
            self.setMinimumWidth(30)

    def text(self) -> str:
        return self.label.text()

    def _normalBackgroundColor(self):
        return self.calculateColor() if self.is_highlighted else super()._normalBackgroundColor()

    def _hoverBackgroundColor(self):
        return self.calculateColor() if self.is_highlighted else super()._hoverBackgroundColor()

    def _pressedBackgroundColor(self):
        return self._hoverBackgroundColor()

    # 计算颜色渐变
    def calculateColor(self) -> QColor:
        base_color = super()._normalBackgroundColor()
        theme_color = themeColor()
        base_r, base_g, base_b, base_a = getRGBA(base_color)
        target_r, target_g, target_b, target_a = getRGBA(theme_color)
        r = (target_r - base_r) * self.animation_value + base_r
        g = (target_g - base_g) * self.animation_value + base_g
        b = (target_b - base_b) * self.animation_value + base_b
        a = (target_a - base_a) * self.animation_value + base_a
        return QColor(r, g, b, a)

    # 切换高亮状态并触发动画
    def toggleHighlight(self):
        self.is_highlighted = True
        self.highlight_animation.setStartValue(self.animation_value)
        self.highlight_animation.start()

        # 300毫秒后恢复背景颜色
        QTimer.singleShot(300, self.resetHighlight)

    # 恢复背景颜色
    def resetHighlight(self):
        self.reset_animation.setStartValue(self.animation_value)
        self.reset_animation.start()
        self.is_highlighted = False


class KeyPrompts(QWidget):
    keyPressed = Signal(str)

    def __init__(self, parent=None):
        """
        按键提示组件，包含一个垂直布局以添加按键操作。

        :param parent: 父窗口
        """
        super().__init__(parent)
        self.key_signals: Dict[str, SignalInstance] = {}

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.keyPressed.connect(self.emitKeySignal)

    def addKeyAction(self, action: KeyAction):
        """
        向组件中添加单个按键操作。

        :param action: KeyAction 对象
        """
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(2)

        # 创建KeyCard
        text = action.key
        action_card = KeyCard(text=text)
        self.key_signals[text] = action_card.highlight

        # 创建标签显示操作描述
        action_label = BodyLabel(text=': ' + action.content)

        # 将按钮和标签添加到布局中
        action_layout.addWidget(action_card)
        action_layout.addWidget(action_label)

        # 添加可伸缩的间隔项
        action_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将操作小部件添加到主布局中
        self.layout.addWidget(action_widget)

    def addKeyActions(self, actions: List[KeyAction]):
        """
        批量添加按键操作。

        :param actions: KeyAction 对象列表
        """
        for action in actions:
            self.addKeyAction(action)

    def addKeyActionGroup(self, actions: List[KeyAction], group_description: str = ''):
        """
        添加一组按键操作，并在旁边显示描述。

        :param actions: KeyAction 对象列表
        :param group_description: 组的描述信息 (可以为空)
        """
        if not actions:
            return  # 如果 actions 为空，则不做任何操作

        # 创建主容器和布局
        group_widget = QWidget()
        group_layout = QHBoxLayout(group_widget)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(2)

        # 创建按键组并填充按钮
        button_group_widget = self._createButtonGroup(actions)
        group_layout.addWidget(button_group_widget)

        # 如果有组描述，则添加描述
        if group_description:
            group_label = BodyLabel(text=': ' + group_description)
            group_layout.addWidget(group_label)

        # 添加可伸缩的间隔项
        group_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 将组小部件添加到主布局中
        self.layout.addWidget(group_widget)

    def _createButtonGroup(self, actions: List[KeyAction]) -> QWidget:
        """
        创建一个包含按键和分隔符的水平按钮组。

        :param actions: KeyAction 对象列表
        :return: QWidget 包含按键组
        """
        button_group_widget = QWidget()
        button_group_layout = QHBoxLayout(button_group_widget)
        button_group_layout.setContentsMargins(0, 0, 0, 0)
        button_group_layout.setSpacing(3)

        for idx, action in enumerate(actions):
            # 创建KeyCard
            text = action.key
            card = KeyCard(text=text)
            self.key_signals[text] = card.highlight
            button_group_layout.addWidget(card)

            # 为除最后一个按钮外添加分隔符
            if idx < len(actions) - 1:
                separator_label = BodyLabel(text='/')
                button_group_layout.addWidget(separator_label)

        return button_group_widget

    def emitKeySignal(self, key_value: str):
        try:
            signal = self.key_signals[key_value]
        except KeyError:
            pass
        else:
            signal.emit()
