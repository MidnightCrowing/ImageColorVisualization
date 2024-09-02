from qfluentwidgets import FluentIcon, NavigationItemPosition

from .page import ComparePage, HomePage, ImitatePage, InfoPage, SettingPage
from .window import Window


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Color Visualization')
        self.resize(1100, 700)

        self.compare_page = ComparePage(self)  # 疑似兼容性BUG，compare_page 需要在 home_page 之前创建
        self.home_page = HomePage(self)
        self.imitate_page = ImitatePage(self)
        self.info_page = InfoPage(self)
        self.setting_page = SettingPage(self)

        self._add_sub_interface()
        self._set_locale()

    def _add_sub_interface(self):
        self.addSubInterface(self.home_page, FluentIcon.HOME, self.tr('Analysis'))
        self.addSubInterface(self.compare_page, FluentIcon.ZOOM, self.tr('Comparison'))
        self.addSubInterface(self.imitate_page, FluentIcon.TRANSPARENT, self.tr('Imitation'))
        self.addSubInterface(self.info_page, FluentIcon.INFO, self.tr('About'),
                             position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.setting_page, FluentIcon.SETTING, self.tr('Settings'),
                             position=NavigationItemPosition.BOTTOM)

    def _set_locale(self):
        # self.setLocale(QLocale(QLocale.English))
        # FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
        # FluentTranslator(QLocale(QLocale.Chinese, QLocale.HongKong))
        pass

    def closeEvent(self, event):
        self._close_vkt()
        event.accept()

    def _close_vkt(self):
        self.home_page.close_vtk()
        self.compare_page.close_vtk()
