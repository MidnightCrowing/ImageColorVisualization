import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from src.app.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    translator = FluentTranslator()
    app.installTranslator(translator)

    trans = QTranslator()
    trans.load(':/i18n/locale/zh_CN.qm')
    app.installTranslator(trans)

    demo = MainWindow()
    demo.show()

    sys.exit(app.exec())
