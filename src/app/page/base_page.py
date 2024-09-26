from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarIcon, InfoBarPosition


class BasePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.info_bar_position = InfoBarPosition.TOP

    def show_info_bar(self,
                      bar_type: Union[InfoBar.info, InfoBar.success, InfoBar.warning, InfoBar.error],
                      title: str,
                      content: str,
                      orient: Union[Qt.Vertical, Qt.Horizontal] = Qt.Vertical,
                      is_closable: bool = True,
                      position: InfoBarPosition = None,
                      duration: int = 5000):
        icon = {
            InfoBar.info: InfoBarIcon.INFORMATION,
            InfoBar.success: InfoBarIcon.SUCCESS,
            InfoBar.warning: InfoBarIcon.WARNING,
            InfoBar.error: InfoBarIcon.ERROR,
        }[bar_type]
        w = InfoBar(
            icon=icon,
            title=title,
            content=content,
            orient=orient,
            isClosable=is_closable,
            position=position or self.info_bar_position,
            duration=duration,
            parent=self.window()
        )
        return w
