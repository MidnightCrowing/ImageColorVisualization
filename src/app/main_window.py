from PySide6.QtCore import QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon, NavigationItemPosition, SplashScreen

# noinspection PyUnresolvedReferences
from .common import resource_rc
from .page import ComparePage, HomePage, ImitatePage, InfoPage, SettingPage
from .window import Window
from src.utils.config import cfg


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Color Visualization')
        # self.setWindowIcon(QIcon(':/logo/pyqt'))
        self.resize(1100, 700)

        # 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self._set_splash_screen()

        # 创建子界面
        self._create_sub_interface()

        # 设置语言
        self._set_locale()

        # 隐藏启动页面
        self.splashScreen.finish()

    def _set_splash_screen(self):
        if not cfg.frame_less_window.value:
            self.splashScreen.titleBar.setHidden(True)
        self.splashScreen.setIcon(self.windowIcon())
        self.splashScreen.setIconSize(QSize(102, 102))

        # 在创建其他子页面前先显示主界面
        self.show()

        # 使用事件循环，确保启动页面先显示
        loop = QEventLoop()
        QTimer.singleShot(1, loop.quit)  # 延迟1ms退出循环，让启动页面有时间显示
        loop.exec()

    def _create_sub_interface(self):
        self.compare_page = ComparePage(self)  # 疑似兼容性BUG，compare_page 需要在 home_page 之前创建
        self.home_page = HomePage(self)
        self.imitate_page = ImitatePage(self)
        self.info_page = InfoPage(self)
        self.setting_page = SettingPage(self)

        self.addSubInterface(self.home_page, FluentIcon.HOME, self.tr('Analysis'))
        self.addSubInterface(self.compare_page, FluentIcon.ZOOM, self.tr('Comparison'))
        self.addSubInterface(self.imitate_page, FluentIcon.TRANSPARENT, self.tr('Imitation'))
        self.addSubInterface(self.info_page, FluentIcon.INFO, self.tr('About'),
                             position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.setting_page, FluentIcon.SETTING, self.tr('Settings'),
                             position=NavigationItemPosition.BOTTOM)

    def _set_locale(self):
        # TODO: 语言设置
        # self.setLocale(QLocale(QLocale.English))
        # FluentTranslator(QLocale(QLocale.Chinese, QLocale.China))
        # FluentTranslator(QLocale(QLocale.Chinese, QLocale.HongKong))
        pass

    def closeEvent(self, event):
        self._close_vtk()
        event.accept()

    def _close_vtk(self):
        self.home_page.close_vtk()
        self.compare_page.close_vtk()
