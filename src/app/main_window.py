from PySide6.QtCore import QLocale
from qfluentwidgets import FluentIcon, NavigationItemPosition

from .page import ComparePage, HomePage, ImitatePage, InfoPage, SettingPage
from .window import Window


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Color Visualization')
        self.resize(1100, 700)

        self.home_page = HomePage(self)
        self.addSubInterface(self.home_page, FluentIcon.HOME, self.tr('Analysis'))
        self.compare_page = ComparePage(self)
        self.addSubInterface(self.compare_page, FluentIcon.ZOOM, self.tr('Comparison'))
        self.imitate_page = ImitatePage(self)
        self.addSubInterface(self.imitate_page, FluentIcon.TRANSPARENT, self.tr('Imitation'))

        self.info_page = InfoPage(self)
        self.addSubInterface(self.info_page, FluentIcon.INFO, self.tr('About'),
                             position=NavigationItemPosition.BOTTOM)
        self.setting_page = SettingPage(self)
        self.addSubInterface(self.setting_page, FluentIcon.SETTING, self.tr('Settings'),
                             position=NavigationItemPosition.BOTTOM)

        self._set_locale()

    def _set_locale(self):
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
