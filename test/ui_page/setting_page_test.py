import os

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

import sys

from PySide6.QtWidgets import QApplication

from src.app.page import SettingPage

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SettingPage()
    window.show()

    sys.exit(app.exec())
