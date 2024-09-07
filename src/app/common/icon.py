from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):
    SelectImage = "SelectImage"

    def path(self, theme=Theme.AUTO):
        return f":/icon/{self.value}_{getIconColor(theme)}"
