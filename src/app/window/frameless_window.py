from PySide6.QtCore import Qt
from qfluentwidgets import MSFluentWindow


class MSFluentFramelessWindow(MSFluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def updateFrameless(self):
        # 覆盖父类WindowsFramelessWindowBase方法，修复vtk渲染器背景颜色问题

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
