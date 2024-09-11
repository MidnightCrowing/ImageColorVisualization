from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):
    KILL_PROCESS = "killProcess"
    MORE_VERTICAL = "moreVertical"
    PAUSE = "pause"
    RERUN = "rerun"
    RERUN_DISABLED = "rerunDisabled"
    RERUN_STROKE = "rerunStroke"
    RUN = "run"
    SELECT_IMAGE = "selectImage"
    STOP = "stop"
    STOP_DISABLED = "stopDisabled"
    STOP_STROKE = "stopStroke"

    def path(self, theme=Theme.AUTO):
        return f":/icon/{self.value}_{getIconColor(theme)}"
