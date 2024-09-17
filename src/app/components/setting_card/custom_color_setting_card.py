import sys
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QButtonGroup, QPushButton, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (CustomColorSettingCard as QFluentCustomColorSettingCard,
                            ColorConfigItem,
                            FluentIconBase,
                            ColorDialog,
                            qconfig,
                            RadioButton)
from qframelesswindow.utils import getSystemAccentColor


class CustomColorSettingCard(QFluentCustomColorSettingCard):
    def __init__(self, configItem: ColorConfigItem, icon: Union[str, QIcon, FluentIconBase], title: str,
                 content=None, parent=None, color_dialog_parent=None, enableAlpha=False):
        super(QFluentCustomColorSettingCard, self).__init__(icon, title, content, parent=parent)
        self.enableAlpha = enableAlpha
        self.configItem = configItem
        self.defaultColor = QColor(configItem.defaultValue)
        self.customColor = QColor(qconfig.get(configItem))
        self.systemColor = getSystemAccentColor()

        self.choiceLabel = QLabel(self)

        self.radioWidget = QWidget(self.view)
        self.radioLayout = QVBoxLayout(self.radioWidget)
        self.defaultRadioButton = RadioButton(
            self.tr('Default color'), self.radioWidget)
        self.systemRadioButton = RadioButton(
            self.tr('System color'), self.radioWidget)
        self.customRadioButton = RadioButton(
            self.tr('Custom color'), self.radioWidget)
        self.buttonGroup = QButtonGroup(self)

        # 只能获取 Windows 和 macOS 的主题色
        if sys.platform not in ["win32", "darwin"]:
            self.systemRadioButton.setHidden(True)

        self.color_dialog_parent = color_dialog_parent or self.window()
        self.customColorWidget = QWidget(self.view)
        self.customColorLayout = QHBoxLayout(self.customColorWidget)
        self.customLabel = QLabel(
            self.tr('Custom color'), self.customColorWidget)
        self.chooseColorButton = QPushButton(
            self.tr('Choose color'), self.customColorWidget)

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()

        if self.customColor == self.defaultColor:
            self.defaultRadioButton.setChecked(True)
            self.chooseColorButton.setEnabled(False)
        elif self.customColor == self.systemColor:
            self.systemRadioButton.setChecked(True)
            self.chooseColorButton.setEnabled(False)
        else:
            self.customRadioButton.setChecked(True)
            self.chooseColorButton.setEnabled(True)

        self.choiceLabel.setText(self.buttonGroup.checkedButton().text())
        self.choiceLabel.adjustSize()

        self.chooseColorButton.setObjectName('chooseColorButton')

        self.buttonGroup.buttonClicked.connect(self.__onRadioButtonClicked)
        self.chooseColorButton.clicked.connect(self.__showColorDialog)

    def __initLayout(self):
        self.addWidget(self.choiceLabel)

        self.radioLayout.setSpacing(19)
        self.radioLayout.setAlignment(Qt.AlignTop)
        self.radioLayout.setContentsMargins(48, 18, 0, 18)
        self.buttonGroup.addButton(self.customRadioButton)
        self.buttonGroup.addButton(self.systemRadioButton)
        self.buttonGroup.addButton(self.defaultRadioButton)
        self.radioLayout.addWidget(self.defaultRadioButton)
        self.radioLayout.addWidget(self.systemRadioButton)
        self.radioLayout.addWidget(self.customRadioButton)
        self.radioLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.customColorLayout.setContentsMargins(48, 18, 44, 18)
        self.customColorLayout.addWidget(self.customLabel, 0, Qt.AlignLeft)
        self.customColorLayout.addWidget(self.chooseColorButton, 0, Qt.AlignRight)
        self.customColorLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.radioWidget)
        self.addGroupWidget(self.customColorWidget)

    def __onRadioButtonClicked(self, button: RadioButton):
        """ radio button clicked slot """
        if button.text() == self.choiceLabel.text():
            return

        self.choiceLabel.setText(button.text())
        self.choiceLabel.adjustSize()

        if button is self.defaultRadioButton:
            self.chooseColorButton.setDisabled(True)
            qconfig.set(self.configItem, self.defaultColor)
            if self.defaultColor != self.customColor:
                self.colorChanged.emit(self.defaultColor)
        elif button is self.systemRadioButton:
            self.chooseColorButton.setDisabled(True)
            qconfig.set(self.configItem, self.systemColor)
            if self.systemColor != self.customColor:
                self.colorChanged.emit(self.systemColor)
        else:
            self.chooseColorButton.setDisabled(False)
            qconfig.set(self.configItem, self.customColor)
            if self.defaultColor != self.customColor and self.systemColor != self.customColor:
                self.colorChanged.emit(self.customColor)

    # 覆盖父类方法以解决对话框失效问题
    def __showColorDialog(self):
        """ show color dialog """
        w = ColorDialog(
            qconfig.get(self.configItem), self.tr('Choose color'), self.color_dialog_parent, self.enableAlpha)
        w.colorChanged.connect(self.__onCustomColorChanged)
        w.show()
