import os
import shutil
from typing import Optional, Callable

from PySide6.QtCore import Qt, QPoint, QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog, QButtonGroup
from qfluentwidgets import (MessageBoxBase,
                            SubtitleLabel,
                            isDarkTheme,
                            FluentIcon,
                            InfoBar,
                            InfoBarPosition,
                            MessageBox,
                            RoundMenu,
                            Action,
                            RadioButton,
                            BodyLabel)

from ..common.icon import Icon
from ..ui.ui_ImitatePage import Ui_ImitatePage
from ...styled_image import HistogramMatcher


def delete_files_except_whitelist(folder_path: str, white_path: str = None) -> int:
    """
    删除指定路径中不在白名单中的文件，并返回删除的文件总大小。

    :param folder_path: 要清理的文件夹路径
    :param white_path: 文件白名单路径，不删除这个文件
    :return: 删除的文件总大小（字节）
    """
    total_deleted_size = 0  # 初始化删除的文件总大小
    white_file = os.path.basename(white_path) if white_path is not None else None

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查是否是文件且不在白名单中
        if os.path.isfile(file_path) and filename != white_file:
            # 获取文件大小
            file_size = os.path.getsize(file_path)

            # 删除文件
            os.remove(file_path)

            # 累加删除的文件大小
            total_deleted_size += file_size

    return total_deleted_size


def format_size(size_bytes):
    """
    将字节大小转换为更易读的格式（带单位）。

    :param size_bytes: 文件大小（字节数）
    :return: 可读形式的文件大小（带单位的字符串）
    """
    if size_bytes == 0:
        return "0 B"

    # 定义单位及其对应的缩写
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = size_bytes
    unit_index = 0

    # 循环将字节转换为更大单位
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    # 格式化输出为两位小数
    return f"{size:.2f} {units[unit_index]}"


class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('编辑运行配置', self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        label = BodyLabel(text='请选择要使用的算法：')

        button1 = RadioButton(text='直方图匹配')
        button2 = RadioButton(text='Neural Style Transfer')
        button3 = RadioButton(text='VGG19')

        # 将单选按钮添加到互斥的按钮组
        buttonGroup = QButtonGroup(self)
        buttonGroup.addButton(button1)
        buttonGroup.addButton(button2)
        buttonGroup.addButton(button3)

        # 当前选中的按钮发生改变
        buttonGroup.buttonToggled.connect(lambda button: print(button.text()))

        button1.setChecked(True)  # 选中第一个按钮
        button2.setDisabled(True)
        button3.setDisabled(True)

        # 将按钮添加到垂直布局
        # noinspection PyUnresolvedReferences
        self.viewLayout.addWidget(label, 0, Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.viewLayout.addWidget(button1, 0, Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.viewLayout.addWidget(button2, 0, Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.viewLayout.addWidget(button3, 0, Qt.AlignLeft)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)


class GenerateImageWorker(QThread):
    setStep = Signal(int)
    finished = Signal(object)

    def __init__(self, temp_dir, step_bar):
        super().__init__()
        self.temp_dir = temp_dir
        self.step_bar = step_bar
        self.target_img_path = None
        self.reference_img_path = None

    def run(self):
        result = self._run_histogram_match()
        self.finished.emit(result)

    def _run_histogram_match(self) -> str:
        matcher = HistogramMatcher(temp_dir=self.temp_dir, step_signal=self.setStep)
        matcher.run_histogram_match(self.target_img_path, self.reference_img_path)
        styled_img_path = matcher.get_save_temp_path()
        return styled_img_path

    def set_image_paths(self, target_img_path: str, reference_img_path: str):
        self.target_img_path = target_img_path
        self.reference_img_path = reference_img_path


class ImitatePage(QWidget, Ui_ImitatePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 初始化属性
        self.temp_dir = r"temp"
        self.generating_image = False
        self.reference_img_path: Optional[str] = None
        self.target_img_path: Optional[str] = None
        self.styled_img_path: Optional[str] = None
        self.generate_image_worker = GenerateImageWorker(self.temp_dir, self.step_bar)

        # 设置界面样式
        self._set_styles()
        # 初始化步骤进度条
        self._initialize_step_bar()
        # 设置工具栏按钮图标
        self._set_tool_buttons()
        # 隐藏图标
        self.styled_img_label.hideIcon()
        # 连接信号和槽
        self._connect_signals()

    def _set_styles(self):
        """设置界面样式"""
        bg_color = "#202020" if isDarkTheme() else "#f0f4f9"
        border_color = "#272727" if isDarkTheme() else "#E6E8EA"
        self.main_widget.setStyleSheet(
            f"""
            #main_widget {{
                background-color: {bg_color};
                border-left: 3px solid {border_color};
            }}
            """
        )

    def _initialize_step_bar(self):
        """初始化步骤进度条"""
        steps = [
            self.tr("Load Images"),
            self.tr("Image Preprocessing"),
            self.tr("Extract Reference Colors"),
            self.tr("Style Transfer Calculation"),
            self.tr("Color Mapping Adjustment"),
            self.tr("Generate Result"),
            self.tr("Display Result"),
            self.tr("Clean Up and Save")
        ]
        self.step_bar.setSteps(steps)

    def _set_tool_buttons(self):
        """设置工具栏按钮图标和状态"""
        icons = {
            self.stop_btn: Icon.STOP,
            self.more_btn: Icon.MORE_VERTICAL,
            self.folder_btn: FluentIcon.FOLDER,
            self.broom_btn: FluentIcon.BROOM,
            self.reference_btn: FluentIcon.LABEL,
            self.target_btn: FluentIcon.LABEL,
            self.styled_btn: FluentIcon.SAVE
        }
        for button, icon in icons.items():
            button.setIcon(icon)
        self.stop_btn.setDisabledState()
        self.update_styled_btn_state()

    def _connect_signals(self):
        """连接信号和槽"""
        self.start_btn.clicked.connect(self.generate_image)
        self.stop_btn.clicked.connect(self.reset_generate_status)
        self.more_btn.clicked.connect(self.create_more_menu)
        self.folder_btn.clicked.connect(self.open_temp_folder)
        self.broom_btn.clicked.connect(self.clear_temp_folder)
        self.reference_btn.clicked.connect(self.select_reference_image)
        self.target_btn.clicked.connect(self.select_target_image)
        self.styled_btn.clicked.connect(self.save_styled_image)
        self.generate_image_worker.setStep.connect(self.step_bar.setCurrentStep)
        self.generate_image_worker.finished.connect(self._generate_image_finished)

    def select_reference_image(self):
        """选择参考图片并更新显示"""

        def select_task():
            file_path = self._open_file_dialog()
            if file_path:
                self.reference_img_path = file_path
                self.reference_img_label.setImage(file_path)
                self.reference_img_label.scaledToHeight(170)
                self.step_bar.setCurrentStep(0)

        if self.generating_image:
            self._confirm_image_change(select_task)
        else:
            select_task()

    def select_target_image(self):
        """选择目标图片并更新显示"""

        def select_task():
            file_path = self._open_file_dialog()
            if file_path:
                self.target_img_path = file_path
                self.target_img_label.setImage(file_path)
                self.target_img_label.scaledToHeight(170)
                self.step_bar.setCurrentStep(0)

        if self.generating_image:
            self._confirm_image_change(select_task)
        else:
            select_task()

    def save_styled_image(self):
        """保存生成的风格化图片"""
        file_path = self._save_file_dialog()
        if file_path:
            try:
                shutil.copy(self.styled_img_path, file_path)
            except FileNotFoundError:
                # noinspection PyUnresolvedReferences
                InfoBar.warning(
                    title='保存失败',
                    content=f"文件保存失败，请检查文件路径是否正确。或可能缓存文件已被删除。",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            else:
                # noinspection PyUnresolvedReferences
                InfoBar.info(
                    title='保存成功',
                    content=f"文件已保存到: {file_path}",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                if self.step_bar.getCurrentStep() == 7:
                    self.step_bar.setCurrentStep(8, animate=False)

    def _open_file_dialog(self) -> str:
        """打开文件选择对话框"""
        return QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )[0]

    def _save_file_dialog(self) -> str:
        """打开保存文件对话框"""
        return QFileDialog.getSaveFileName(
            self, self.tr("Save Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )[0]

    def _confirm_image_change(self, call_func: Callable):
        """确认是否更换图片"""
        w = MessageBox(self.tr("更换图片警告"),
                       self.tr("更换图片会导致已加载的图像数据失效，可能需要重新执行生成步骤，确定要继续吗？"),
                       self.window())
        w.yesButton.clicked.connect(call_func)
        w.show()

    def reset_generate_status(self):
        """重置生成状态"""
        self.start_btn.setStopState()
        self.stop_btn.setStopState()
        self.step_bar.setCurrentStep(0)
        self.generating_image = False
        self.update_styled_btn_state()

    def check_generate_image(self) -> bool:
        """检查是否选择了参考图像和目标图像"""
        return not (self.reference_img_label.image.isNull() or self.target_img_label.image.isNull())

    def update_styled_btn_state(self):
        """更新风格化按钮状态"""
        self.styled_btn.setDisabled(self.styled_img_label.isNull())

    def warning_bar_show(self):
        """显示警告信息条"""
        # noinspection PyUnresolvedReferences
        InfoBar.warning(
            title='错误',
            content="请先选择参考图片和目标图片",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )

    def create_more_menu(self):
        """创建更多菜单"""
        pos = self.more_btn.mapToGlobal(QPoint(-10, self.more_btn.height()))
        action = Action(text=self.tr('修改运行配置...'))
        action.triggered.connect(self.show_config_box)
        menu = RoundMenu(parent=self)
        menu.addAction(action)
        menu.exec(pos, ani=True)

    def show_config_box(self):
        """显示配置对话框"""

        def update_run_config():
            print('...')

        w = CustomMessageBox(self.window())
        w.yesButton.clicked.connect(update_run_config)
        w.show()

    def open_temp_folder(self):
        """打开临时文件夹"""
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        os.startfile(self.temp_dir)

    def clear_temp_folder(self):
        """清理临时文件夹"""

        def show_info_bar(content):
            """显示信息条"""
            # noinspection PyUnresolvedReferences
            InfoBar.info(
                title=self.tr("清理缓存文件"),
                content=content,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )

        def clear_task():
            if not os.path.exists(self.temp_dir):
                show_info_bar("无缓存文件夹，无需清理")
                return

            deleted_size = delete_files_except_whitelist(self.temp_dir, self.styled_img_path)
            if deleted_size == 0 and self.styled_img_path is None:
                show_info_bar("无缓存文件，无需清理")
            else:
                show_info_bar(f"清理缓存文件成功，删除的文件总大小: {format_size(deleted_size)}")

        m = MessageBox(self.tr("清理缓存文件"), self.tr("这将会删除掉所有缓存文件，确定要这么做吗？"), self.window())
        m.yesSignal.connect(clear_task)
        m.show()

    def generate_image(self):
        """生成风格化图像"""
        if self._generate_image_started():
            self._generate_image_task()

    def _generate_image_started(self) -> bool:
        """生成风格化图像"""
        if not self.check_generate_image():
            self.warning_bar_show()
            return False

        self.start_btn.setRunState()
        self.stop_btn.setRunState()
        self.styled_img_label.removeImage()
        self.styled_img_label.hideIcon()
        self.generating_image = True
        return True

    def _generate_image_task(self):
        self.generate_image_worker.set_image_paths(self.target_img_path, self.reference_img_path)
        self.generate_image_worker.start()

    def _generate_image_finished(self, result):
        if isinstance(result, Exception):
            # Handle the exception (e.g., show an error message)
            # noinspection PyUnresolvedReferences
            InfoBar.warning(
                title='错误',
                content=f"{result}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
        else:
            self.styled_img_label.setImage(result)
            self.styled_img_label.scaledToHeight(170)
            self.update_styled_btn_state()
            self.styled_img_path = result

        self.start_btn.setStopState()
        self.stop_btn.setStopState()
        self.generating_image = False
