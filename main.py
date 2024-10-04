import os
import sys

from PySide6.QtCore import QTranslator, Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from src.app.main_window import MainWindow
from src.utils.config import cfg

if __name__ == "__main__":
    # enable dpi scale
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluent_translator = FluentTranslator(locale)  # PySide6-Fluent-Widgets 的翻译器
    app_translator = QTranslator()
    app_translator.load(f":/i18n/{locale.name()}")

    app.installTranslator(fluent_translator)
    app.installTranslator(app_translator)

    # create main window
    demo = MainWindow()
    demo.show()

    sys.exit(app.exec())
