from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import RangeSettingCard, FluentIconBase, RangeConfigItem, RangeValidator


class DoubleRangeConfigItem(RangeConfigItem):
    """Configuration item for range values with scaling applied."""

    def __init__(
            self,
            group: str,
            name: str,
            default: float,
            validator: Union[RangeValidator] = None,
            scale: int = 2,
            serializer=None,
            restart: bool = False
    ):
        """
        Initialize ScaledRangeConfigItem with scaling factor.

        Parameters
        ----------
        group : str
            The configuration group name.
        name : str
            The configuration item name.
        default : float
            The default value of the configuration item.
        validator : RangeValidator, optional
            A validator that checks if values are within the specified range.
        scale : int, optional
            Number of decimal places to scale the value by, default is 2.
        serializer : optional
            Serializer used for saving and loading values.
        restart : bool, optional
            Whether a restart is required when the value changes.
        """
        self.scale = scale
        self.scaling_multiplier = 10 ** scale

        # Adjust the validator range according to the scaling multiplier
        if validator is not None:
            validator = RangeValidator(
                validator.min * self.scaling_multiplier,
                validator.max * self.scaling_multiplier
            )
        # Adjust the default value according to the scaling multiplier and initialize the base class
        super().__init__(group, name, default * self.scaling_multiplier, validator, serializer, restart)

    def __str__(self):
        return f'{self.__class__.__name__}[range={self.range}, value={self.value}, scale={self.scale}]'

    @property
    def doubleValue(self):
        return self.value / self.scaling_multiplier

class DoubleRangeSettingCard(RangeSettingCard):
    """Setting card for scaled range configuration items."""

    def __init__(
            self,
            configItem: DoubleRangeConfigItem,
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
        self._update_value_label(configItem.value)

    def _update_value_label(self, value: float):
        """Update the value label with the scaled value."""
        self.valueLabel.setNum(value / self.scaling_multiplier)

    def setValue(self, value: float):
        """Set a new value and update the display label."""
        super().setValue(value)
        self._update_value_label(value)
