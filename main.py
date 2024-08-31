import sys

from qfluentwidgets import qconfig

from src.utils.config import cfg


def load_config():
    """Load the configuration before importing MainWindow."""
    qconfig.load("data/config.json", cfg)


def main():
    from PySide6.QtWidgets import QApplication
    from src.app.main_window import MainWindow

    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    load_config()
    main()
