from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor


class Icon(FluentIconBase, Enum):
    COORDINATE_SYSTEM = "coordinateSystem"
    KILL_PROCESS = "killProcess"
    MORE_VERTICAL = "moreVertical"
    PAUSE = "pause"
    RERUN = "rerun"
    RERUN_DISABLED = "rerunDisabled"
    RERUN_STROKE = "rerunStroke"
    RUN = "run"
    SCREENSHOT = "screenshot"
    SELECT_IMAGE = "selectImage"
    STOP = "stop"
    STOP_DISABLED = "stopDisabled"
    STOP_STROKE = "stopStroke"

    def path(self, theme=Theme.AUTO):
        return f":/icon/{self.value}_{getIconColor(theme)}"
