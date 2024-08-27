from PySide6.QtWidgets import QWidget
from qfluentwidgets import (CustomColorSettingCard,
                            ExpandLayout,
                            FluentIcon,
                            OptionsConfigItem,
                            OptionsSettingCard,
                            OptionsValidator,
                            QConfig,
                            SettingCardGroup,
                            qconfig)

from ..ui.ui_SettingPage import Ui_SettingPage


class Config(QConfig):
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)


cfg = Config()
qconfig.load("../data/ui_config.json", cfg)


class SettingPage(QWidget, Ui_SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.expandLayout = ExpandLayout(self.widget)

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.widget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FluentIcon.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        # self.languageCard = ComboBoxSettingCard(
        #     cfg.language,
        #     FluentIcon.LANGUAGE,
        #     self.tr('Language'),
        #     self.tr('Set your preferred language for UI'),
        #     texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
        #     parent=self.personalGroup
        # )

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        # self.personalGroup.addSettingCard(self.languageCard)

        self.expandLayout.addWidget(self.personalGroup)
