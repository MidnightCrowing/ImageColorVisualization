from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import (CustomColorSettingCard as QFluentCustomColorSettingCard,
                            ColorConfigItem,
                            FluentIconBase,
                            ColorDialog,
                            qconfig)


class CustomColorSettingCard(QFluentCustomColorSettingCard):
    def __init__(self, configItem: ColorConfigItem, icon: Union[str, QIcon, FluentIconBase], title: str,
                 content=None, parent=None, color_dialog_parent=None, enableAlpha=False):
        super().__init__(configItem, icon, title, content, parent, enableAlpha)
        self.color_dialog_parent = color_dialog_parent or self.window()

    # 覆盖父类方法以解决对话框失效问题
    def __showColorDialog(self):
        """ show color dialog """
        w = ColorDialog(
            qconfig.get(self.configItem), self.tr('Choose color'), self.color_dialog_parent, self.enableAlpha)
        w.colorChanged.connect(self.__onCustomColorChanged)
        w.show()
