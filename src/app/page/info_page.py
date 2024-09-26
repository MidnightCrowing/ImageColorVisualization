import webbrowser

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget

from src.utils.config import SUPPORT_URL, VERSION
from .base_page import BasePage
from ..ui.ui_InfoPage import Ui_InfoPage

PYQT_URL = "https://doc.qt.io/qtforpython-6/quickstart.html"
QFW_URL = "https://qfluentwidgets.com/zh/pages/about/"
VTK_URL = "https://examples.vtk.org/site/"


class InfoPage(BasePage, Ui_InfoPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.info_frame.setHidden(True)
        self.info_frame.setProperty('type', 'dark_Warning')
        self.info_icon.setImage(':/qfluentwidgets/images/info_bar/Warning_dark.svg')
        self.info_text.setText(QCoreApplication.translate("InfoPage",
                                                          u"",
                                                          None))

        self.version_label.setText(VERSION)
        self.support_button.setUrl(SUPPORT_URL)

        self.img_label_pyqt.scaledToHeight(60)
        self.img_label_qfw.scaledToHeight(60)
        self.img_label_vtk.scaledToHeight(60)

        self.card_pyqt.clicked.connect(lambda: webbrowser.open(PYQT_URL))
        self.card_qfw.clicked.connect(lambda: webbrowser.open(QFW_URL))
        self.card_vtk.clicked.connect(lambda: webbrowser.open(VTK_URL))
