from typing import Callable, List

from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, PushButton


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


class KeyPrompts(QWidget):
    def __init__(self, parent=None):
        """
        按键提示组件，包含一个垂直布局以添加按键操作。

        :param parent: 父窗口
        """
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def addKeyAction(self, action: KeyAction):
        """
        向组件中添加单个按键操作。

        :param action: KeyAction 对象
        """
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(2)

        # 创建按钮并连接点击事件
        action_button = PushButton(text=action.key)
        action_button.clicked.connect(action.triggered)

        # 创建标签显示操作描述
        action_label = BodyLabel(text=': ' + action.content)

        # 将按钮和标签添加到布局中
        action_layout.addWidget(action_button)
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
            # 创建按键并绑定点击事件
            action_button = PushButton(text=action.key)
            action_button.clicked.connect(action.triggered)
            button_group_layout.addWidget(action_button)

            # 为除最后一个按钮外添加分隔符
            if idx < len(actions) - 1:
                separator_label = BodyLabel(text='/')
                button_group_layout.addWidget(separator_label)

        return button_group_widget
