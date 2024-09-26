from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIconBase, RangeSettingCard


class DoubleRangeSettingCard(RangeSettingCard):
    """Setting card for scaled range configuration items."""

    def __init__(
            self,
            configItem,
            icon: Union[str, QIcon, FluentIconBase],
            title: str,
            content: str = None,
            parent=None
    ):
        """
        Initialize the setting card with a scaled range config item.

        Parameters
        ----------
        configItem : DoubleRangeConfigItem
            The configuration item this setting card represents.
        icon : Union[str, QIcon, FluentIconBase]
            The icon displayed on the card.
        title : str
            The title of the setting card.
        content : str, optional
            Additional content
        parent : optional
            Parent widget.
        """
        super().__init__(configItem, icon, title, content, parent)
        self.scaling_multiplier = configItem.scaling_multiplier
        self._updateLabelValue(configItem.value)

    def _updateLabelValue(self, value: float):
        """Update the value label with the scaled value."""
        self.valueLabel.setNum(value / self.scaling_multiplier)

    def setValue(self, value: float):
        """Set a new value and update the display label."""
        super().setValue(value)
        self._updateLabelValue(value)
