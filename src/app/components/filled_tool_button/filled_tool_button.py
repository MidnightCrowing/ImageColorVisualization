from PySide6.QtWidgets import QWidget
from qfluentwidgets import ToolTipFilter, ToolTipPosition
from qfluentwidgets import TransparentToolButton


class FilledToolButton(TransparentToolButton):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.filled_style = self._getBaseStyleSheet()

        self._setStyleSheet()
        self.setStopState()
        self.installEventFilter(ToolTipFilter(self, 300, ToolTipPosition.BOTTOM))

    def _getBaseStyleSheet(self) -> str:
        return """
            FilledToolButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 5px 9px 6px 8px;
                margin: 0;
            }

            FilledToolButton:hover {
                background-color: rgba(255, 255, 255, 9);
                border: none;
            }

            FilledToolButton:pressed {
                background-color: rgba(255, 255, 255, 6);
                border: none;
            }

            FilledToolButton:disabled {
                background-color: transparent;
                border: none;
            }
        """

    def _setStyleSheet(self):
        self.setStyleSheet(self.filled_style)

    def setRunState(self):
        self.setProperty("type", "running")
        self.style().unpolish(self)  # 取消现有样式
        self.style().polish(self)  # 重新应用样式
        self.update()  # 刷新组件显示

    def setStoppingState(self):
        self.setProperty("type", "stopping")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def setStopState(self):
        self.setProperty("type", "stopped")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
