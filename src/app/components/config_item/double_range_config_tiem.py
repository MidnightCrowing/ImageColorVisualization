from typing import Optional

from qfluentwidgets import RangeConfigItem, RangeValidator


class DoubleRangeConfigItem(RangeConfigItem):
    """Configuration item for range values with scaling applied."""

    def __init__(
            self,
            group: str,
            name: str,
            default: float,
            validator: Optional[RangeValidator] = None,
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
