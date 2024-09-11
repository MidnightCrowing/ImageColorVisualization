import gc
import os

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import (MessageBoxBase,
                            SubtitleLabel,
                            isDarkTheme,
                            FluentIcon,
                            InfoBar,
                            InfoBarPosition,
                            MessageBox,
                            RoundMenu,
                            Action)

from ..common.icon import Icon
from ..ui.ui_ImitatePage import Ui_ImitatePage


class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('标题', self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)


class ImitatePage(QWidget, Ui_ImitatePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.generating_image = False
        # TODO: Imitate page

        # 设置main_widget背景颜色
        widget_bg_color = "#202020" if isDarkTheme() else "#f0f4f9"
        widget_border_color = "#272727" if isDarkTheme() else "#E6E8EA"
        self.main_widget.setStyleSheet(
            f"""
            #main_widget {{
                background-color: {widget_bg_color};
                border-left: 3px solid {widget_border_color};
            }}
            """
        )

        # 设置步骤进度条
        self.step_bar.setSteps([self.tr("Load Images"),
                                self.tr("Image Preprocessing"),
                                self.tr("Extract Reference Colors"),
                                self.tr("Style Transfer Calculation"),
                                self.tr("Color Mapping Adjustment"),
                                self.tr("Generate Result"),
                                self.tr("Display Result"),
                                self.tr("Clean Up and Save")])

        # 设置工具栏按钮图标
        self.stop_btn.setIcon(Icon.STOP)
        self.more_btn.setIcon(Icon.MORE_VERTICAL)
        self.folder_btn.setIcon(FluentIcon.FOLDER)
        self.broom_btn.setIcon(FluentIcon.BROOM)
        self.reference_btn.setIcon(FluentIcon.LABEL)
        self.target_btn.setIcon(FluentIcon.LABEL)
        self.style_btn.setIcon(FluentIcon.SAVE)

        # 设置工具栏按钮状态
        self.stop_btn.setDisabledState()
        self.update_style_btn_state()

        # 隐藏图标
        self.style_img_label.hideIcon()

        # 设置信号槽
        self._connect_signals()

    def _connect_signals(self):
        self.start_btn.clicked.connect(self.generate_image)
        self.stop_btn.clicked.connect(self.user_reset_generate_status)
        self.more_btn.clicked.connect(lambda: self.create_more_menu(
            self.more_btn.mapToGlobal(QPoint(-10, self.more_btn.height()))))
        self.folder_btn.clicked.connect(self.open_temp_folder)
        self.broom_btn.clicked.connect(self.broom_temp)
        self.reference_btn.clicked.connect(self.set_reference_img)
        self.target_btn.clicked.connect(self.set_target_img)
        self.style_btn.clicked.connect(self.save_style_img)

    def set_reference_img(self):
        # 如果正在生成图片，则弹出警告框
        if self.generating_image:
            w = MessageBox(self.tr("更换图片警告"),
                           self.tr("更换图片会导致已加载的图像数据失效，可能需要重新执行生成步骤，确定要继续吗？"), self)
            if w.exec():
                # 确认
                self.user_reset_generate_status()
                pass
            else:
                # 取消
                return

        file_path = self.open_file_dialog()
        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.reference_img_label.setImage(file_path)
            self.reference_img_label.scaledToHeight(170)

    def set_target_img(self):
        # 如果正在生成图片，则弹出警告框
        if self.generating_image:
            w = MessageBox(self.tr("更换图片警告"),
                           self.tr("更换图片会导致已加载的图像数据失效，可能需要重新执行生成步骤，确定要继续吗？"), self)
            if w.exec():
                # 确认
                self.user_reset_generate_status()
                pass
            else:
                # 取消
                return

        file_path = self.open_file_dialog()
        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.target_img_label.setImage(file_path)
            self.target_img_label.scaledToHeight(170)

            self.step_bar.setCurrentStep(0)

    def save_style_img(self):
        file_path = self.save_file_dialog()
        # 检查是否选择了文件路径
        if file_path:
            self.target_img_label.image.save(file_path)
            if self.step_bar.getCurrentStep() == 7:
                self.step_bar.setCurrentStep(8)

    def open_file_dialog(self) -> str:
        # 打开文件选择对话框，设置文件类型为常见的图片格式
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        return file_path

    def save_file_dialog(self) -> str:
        # 打开保存文件对话框，支持 .ply 和 .vtk 格式
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Save Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        return file_path

    @staticmethod
    def generate_image_wrapper(method):
        def wrapper(self, *args, **kwargs):
            # 执行之前的操作
            if not self.check_generate_image():
                self.warning_bar_show()
                return
            # 设置按钮状态
            self.start_btn.setRunState()
            self.stop_btn.setRunState()
            #
            target_image = self.target_img_label.image
            self.style_img_label.removeImage()
            self.generating_image = True

            # 执行方法
            result = method(self, *args, **kwargs)

            # 执行之后的操作
            self.style_img_label.setImage(target_image)
            self.style_img_label.scaledToHeight(170)
            self.update_style_btn_state()
            # 设置按钮状态
            self.start_btn.setStopState()
            self.stop_btn.setStopState()
            #
            self.generating_image = False

            return result

        return wrapper

    @generate_image_wrapper
    def generate_image(self):
        for i in range(1, 8):
            self.step_bar.setCurrentStep(i)

    def user_reset_generate_status(self):
        """用户重置生成状态"""
        # 设置导航栏按钮状态
        self.start_btn.setStoppingState()
        self.stop_btn.setStoppingState()

        self.step_bar.setCurrentStep(0)
        self.generating_image = False
        self.update_style_btn_state()

        self.start_btn.setStopState()
        self.stop_btn.setStopState()

    def check_generate_image(self) -> bool:
        reference_image = self.reference_img_label.image
        target_image = self.target_img_label.image
        if target_image.isNull() or reference_image.isNull():
            return False
        return True

    def update_style_btn_state(self):
        if self.style_img_label.isNull():
            self.style_btn.setDisabled(True)
        else:
            self.style_btn.setDisabled(False)

    def warning_bar_show(self):
        InfoBar.warning(
            title='错误',
            content="请先选择参考图片和目标图片",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )

    def create_more_menu(self, pos):
        action = Action(text=self.tr('修改运行配置...'))
        action.triggered.connect(self.show_config_box)

        menu = RoundMenu(parent=self)
        menu.addAction(action)
        menu.exec(pos, ani=True)

    def show_config_box(self):
        w = CustomMessageBox(self)
        if w.exec():
            print("...")

    @staticmethod
    def open_temp_folder():
        if not os.path.exists("temp"):
            os.makedirs("temp")
        os.startfile(r"temp")

    def broom_temp(self):
        gc.collect()
        InfoBar.info(
            title='清理缓存文件',
            content="清理缓存文件成功",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
