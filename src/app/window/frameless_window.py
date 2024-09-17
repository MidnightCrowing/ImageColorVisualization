from PySide6.QtCore import Qt, QEvent
from qfluentwidgets import MSFluentWindow


class MSFluentFramelessWindow(MSFluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pre_maximized_size = None  # 记录最大化前的窗口大小
        self.is_restoring = False  # 标志用于恢复窗口状态

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            current_state = self.windowState()
            previous_state = event.oldState()

            if current_state & Qt.WindowMaximized:
                # 窗口当前处于最大化状态
                if self.pre_maximized_size is None:
                    # 记录最大化前的窗口大小
                    self.pre_maximized_size = self.size()

                if previous_state & Qt.WindowMinimized:
                    # 窗口从最小化状态恢复
                    self.is_restoring = True
                    self.adjustSize()  # 调整窗口大小
                    self.showMaximized()  # 恢复最大化

            elif previous_state & Qt.WindowMaximized:
                # 窗口从最大化状态恢复到普通状态
                if self.is_restoring:
                    # 恢复最大化状态时设置的标志
                    self.is_restoring = False
                else:
                    # 恢复到最大化前的大小
                    if self.pre_maximized_size is not None:
                        self.resize(self.pre_maximized_size)
                        self.pre_maximized_size = None  # 清除记录的大小

        super().changeEvent(event)

    def updateFrameless(self):
        # 覆盖父类WindowsFramelessWindowBase方法，修复vtk渲染器背景颜色问题

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self.windowEffect.addWindowAnimation(self.winId())
