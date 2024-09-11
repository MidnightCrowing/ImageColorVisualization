from PySide6.QtWidgets import QWidget

from .filled_tool_button import FilledToolButton
from ...common.icon import Icon


class StopFilledToolButton(FilledToolButton):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setIcon(Icon.STOP_DISABLED)

        self.stop_style = """
            StopFilledToolButton[type="running"] {
                background-color: #C94F4F;
                border: none;
                border-radius: 4px;
                margin: 0;
            }

            StopFilledToolButton[type="running"]:hover {
                background-color: #B54747;
                border: none;
            }

            StopFilledToolButton[type="running"]:pressed {
                background-color: #A94242;
                border: none;
            }
        """

        self.setStyleSheet(self.filled_style + self.stop_style)

    def setDisabledState(self):
        self.setIcon(Icon.STOP_DISABLED)
        self.setDisabled(True)

    def setRunState(self):
        super().setRunState()
        self.setIcon(Icon.STOP_STROKE)
        self.setDisabled(False)

    def setStoppingState(self):
        super().setStoppingState()
        self.setIcon(Icon.KILL_PROCESS)

    def setStopState(self):
        super().setStopState()
        self.setDisabledState()
