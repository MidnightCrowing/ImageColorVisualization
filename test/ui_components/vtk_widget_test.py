import os

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

from PySide6.QtWidgets import QApplication

from src.app.components import VTKWidget
# noinspection PyUnresolvedReferences
import src.utils.config
# noinspection PyUnresolvedReferences
from src.app.common import resource_rc

if __name__ == "__main__":
    app = QApplication([])
    widget = VTKWidget()
    widget.resize(800, 600)
    widget.setWindowTitle("VTKWidget")

    widget.saveScreenshot.connect(lambda path: print("保存截图:", path))
    widget.openSetting.connect(lambda: print("打开设置"))

    widget.show()
    app.exec()
