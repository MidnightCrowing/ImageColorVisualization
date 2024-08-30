from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from qfluentwidgets import SettingCard, FluentIconBase, ConfigItem, SpinBox, qconfig, DoubleSpinBox


class DoubleSpinBoxSettingCard(SettingCard):

    valueChanged = Signal(int)

    def __init__(
            self,
            configItem: ConfigItem,
            icon: Union[str, QIcon, FluentIconBase],
            title,
            content=None,
            parent=None
    ):
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.spin = DoubleSpinBox(self)

        self.spin.setRange(0, 2147483647) # max: 2^31 - 1
        self.spin.setValue(configItem.value)
        self.spin.setMinimumWidth(200)
        self.hBoxLayout.addWidget(self.spin, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        configItem.valueChanged.connect(self.setValue)
        self.spin.valueChanged.connect(self.__onValueChanged)

    def __onValueChanged(self, value: int):
        """ spin box value changed slot """
        self.setValue(value)
        self.valueChanged.emit(value)

    def setValue(self, value):
        qconfig.set(self.configItem, value)
        self.spin.setValue(value)
