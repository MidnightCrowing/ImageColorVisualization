from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from qfluentwidgets import ConfigItem, FluentIconBase, LineEdit, SettingCard, qconfig


class InputSettingCard(SettingCard):
    """ Setting card with a input box """

    valueChanged = Signal(str)

    def __init__(
            self,
            configItem: ConfigItem,
            icon: Union[str, QIcon, FluentIconBase],
            title,
            content=None,
            parent=None
    ):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.input = LineEdit(self)

        self.input.setText(str(configItem.value))
        self.input.setMinimumWidth(200)
        self.hBoxLayout.addWidget(self.input, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        configItem.valueChanged.connect(self.setValue)
        self.input.textChanged.connect(self._onValueChanged)

    def _onValueChanged(self, value: int):
        """ spin box value changed slot """
        self.setValue(value)
        self.valueChanged.emit(value)

    def setValue(self, value):
        qconfig.set(self.configItem, value)
        self.input.setText(str(value))
