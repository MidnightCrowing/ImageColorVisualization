from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon, NavigationItemPosition

from .page import ComparePage, HomePage, ImitatePage, InfoPage, SettingPage
from .window import Window


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Color Visualization')
        self.resize(1100, 700)

        self.home_page = HomePage(self)
        self.addSubInterface(self.home_page, FluentIcon.HOME, '分析')
        self.compare_page = ComparePage(self)
        self.addSubInterface(self.compare_page, FluentIcon.ZOOM, '比较')
        self.imitate_page = ImitatePage(self)
        self.addSubInterface(self.imitate_page, FluentIcon.TRANSPARENT, '模仿')

        self.info_page = InfoPage(self)
        self.addSubInterface(self.info_page, FluentIcon.INFO, '关于', position=NavigationItemPosition.BOTTOM)
        self.setting_page = SettingPage(self)
        self.addSubInterface(self.setting_page, FluentIcon.SETTING, '设置', position=NavigationItemPosition.BOTTOM)

    def updateFrameless(self):
        """ update frameless window """
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
