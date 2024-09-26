from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from qfluentwidgets import ConfigItem, FluentIconBase, SettingCard, SpinBox, qconfig


class SpinBoxSettingCard(SettingCard):
    """ Setting card with a spin box """

    valueChanged = Signal(int)

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
        self.spin = SpinBox(self)

        self.spin.setRange(0, 2147483647)  # max: 2^31 - 1
        self.spin.setValue(configItem.value)
        self.spin.setMinimumWidth(200)
        self.hBoxLayout.addWidget(self.spin, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        configItem.valueChanged.connect(self.setValue)
        self.spin.valueChanged.connect(self._onValueChanged)

    def _onValueChanged(self, value: int):
        """ spin box value changed slot """
        self.setValue(value)
        self.valueChanged.emit(value)

    def setValue(self, value):
        qconfig.set(self.configItem, value)
        self.spin.setValue(value)
