from PySide6.QtWidgets import QWidget

from .filled_tool_button import FilledToolButton
from ...common.icon import Icon


class StartFilledToolButton(FilledToolButton):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.rerun = False

    def _setStyleSheet(self):
        self.start_style = """
            StartFilledToolButton[type="running"] {
                background-color: #57965C;
                border: none;
                border-radius: 4px;
                margin: 0;
            }

            StartFilledToolButton[type="running"]:hover {
                background-color: #4E8752;
                border: none;
            }

            StartFilledToolButton[type="running"]:pressed {
                background-color: #497E4D;
                border: none;
            }
        """
        self.setStyleSheet(self.filled_style + self.start_style)

    def setRunState(self):
        super().setRunState()
        self.setIcon(Icon.RERUN_STROKE)
        self.setToolTip(self.tr('Rerun'))

    def setStoppingState(self):
        super().setStoppingState()
        self.rerun = True
        self.setIcon(Icon.RERUN_DISABLED)
        self.setDisabled(True)
        self.setToolTip('')

    def setStopState(self):
        super().setStopState()
        self.rerun = False
        self.setIcon(Icon.RUN if not self.rerun else Icon.RERUN)
        self.setDisabled(False)
        self.setToolTip(self.tr('Run'))
