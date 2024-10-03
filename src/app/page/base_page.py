import sys
from typing import Union

from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import InfoBar, InfoBarIcon, InfoBarPosition, MessageBox


class BasePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.info_bar_position = InfoBarPosition.TOP

    def show_info_bar(self,
                      bar_type: Union[InfoBar.info, InfoBar.success, InfoBar.warning, InfoBar.error],
                      title: str,
                      content: str,
                      orient: Union[Qt.Vertical, Qt.Horizontal] = Qt.Vertical,
                      is_closable: bool = True,
                      position: InfoBarPosition = None,
                      duration: int = 5000,
                      show: bool = True):
        icon = {
            InfoBar.info: InfoBarIcon.INFORMATION,
            InfoBar.success: InfoBarIcon.SUCCESS,
            InfoBar.warning: InfoBarIcon.WARNING,
            InfoBar.error: InfoBarIcon.ERROR,
        }[bar_type]
        w = InfoBar(
            icon=icon,
            title=title,
            content=content,
            orient=orient,
            isClosable=is_closable,
            position=position or self.info_bar_position,
            duration=duration,
            parent=self.window()
        )
        if show:
            w.show()
        return w

    def show_permission_dialog(self, require_admin_restart: bool = False):
        """
        显示权限不足的提示对话框

        :param require_admin_restart: 是否需要重启程序并使用管理员权限来解决权限问题
        """
        message_title = self.tr('Insufficient permissions')
        message_text = self.tr(
            'The current operation encountered a permissions issue. To continue, try restarting the program with administrator rights.')

        dialog = MessageBox(message_title, message_text, self.window())
        dialog.yesButton.setText(self.tr('Restart'))
        dialog.cancelButton.setText(self.tr('Remind me later'))

        if require_admin_restart:
            dialog.cancelButton.setVisible(False)

        dialog.yesSignal.connect(lambda: self.restart_now(need_admin_restart=True))

        dialog.show()

    def restart_now(self, need_admin_restart: bool = False):
        """ 重启应用程序 """
        # 判断是否为打包后的可执行文件
        if sys.argv[0].endswith(".exe"):
            # exe env
            # 获取打包后的可执行文件路径
            executable = sys.argv[0]
        else:
            # python env
            # 获取当前 Python 解释器的路径
            executable = sys.executable

        # 判断是否需要使用管理员权限重启
        if need_admin_restart:
            pass
            # TODO 使用管理员权限运行程序
            # error_dialog = QMessageBox()
            # error_dialog.setIcon(QMessageBox.Critical)  # 设置对话框为错误图标
            # error_dialog.setWindowTitle(self.tr("Error"))  # 设置对话框标题
            # error_dialog.setText(self.tr("Failed to start"))  # 设置主要提示文本
            # error_dialog.setInformativeText(
            #     self.tr("Please try again manually and make sure to run the program as administrator."))  # 设置详细信息
            # error_dialog.setStandardButtons(QMessageBox.Ok)  # 设置确认按钮
            # error_dialog.exec()  # 显示对话框
        else:
            # 使用 QProcess 重新启动当前的可执行文件
            QProcess.startDetached(executable, sys.argv)

        # 退出当前应用程序
        QApplication.quit()
