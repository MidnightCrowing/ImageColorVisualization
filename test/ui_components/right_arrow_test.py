import os

from qfluentwidgets import isDarkTheme

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

from PySide6.QtWidgets import QApplication

from src.app.components import RightArrow
# noinspection PyUnresolvedReferences
import src.utils.config

if __name__ == "__main__":
    app = QApplication([])
    widget = RightArrow()
    widget.setWindowTitle("RightArrow")
    widget.setStyleSheet(f"background-color: {"#202020" if isDarkTheme() else "#f0f4f9"}")
    widget.show()
    app.exec()
