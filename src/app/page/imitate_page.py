import os
import shutil
from enum import Enum, auto
from functools import partial
from typing import Callable, Optional

from PySide6.QtCore import QPoint, QThread, Qt, Signal, Slot
from PySide6.QtWidgets import QButtonGroup, QFileDialog
from qfluentwidgets import (Action, BodyLabel, FluentIcon, InfoBar, MessageBox, MessageBoxBase, PushButton, RadioButton,
                            RoundMenu, SubtitleLabel, ToolTipFilter, ToolTipPosition, isDarkTheme)

from src.styled_image import HistogramMatcher, StyTr
from src.utils.config import StyledImageEnum, cfg
from src.utils.reveal_file import reveal_file
from .base_page import BasePage
from ..common.icon import Icon
from ..ui.ui_ImitatePage import Ui_ImitatePage


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


def format_size(size_bytes: int):
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


class RunState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    STOPPING = auto()
    RERUN_AND_STOP = auto()
    RERUN_AND_STOPPING = auto()


class ImageGenerationWorker(QThread):
    """生成图片的工作线程"""
    stepUpdated = Signal(int)
    stopped = Signal()
    finished = Signal(object)

    def __init__(self, base_page: BasePage, temp_dir: str, step_bar: str):
        super().__init__()
        self.base_page = base_page
        self.temp_dir = temp_dir
        self.step_bar = step_bar
        self.target_img_path = None
        self.reference_img_path = None
        self.styled_selected = None
        self.matcher: Optional[HistogramMatcher] = None
        self.is_running: bool = False

    def run(self):
        self.is_running = True

        algorithm_method = self.get_algorithm_method()
        if algorithm_method:
            try:
                result = algorithm_method()
            except Exception as e:
                self.finished.emit(e)
            else:
                if self.is_running:
                    self.finished.emit(result)
        else:
            self.finished.emit(ValueError(f"The selected algorithm is not supported: {self.styled_selected}"))

    def get_algorithm_method(self) -> Callable[[], str]:
        """根据选中的算法返回对应的处理方法"""
        algorithm_map = {
            StyledImageEnum.HISTOGRAM_MATCHER.value: self._run_histogram_match,
            StyledImageEnum.STY_TR.value: self._run_sty_tr,
        }
        return algorithm_map.get(self.styled_selected)

    def _run_histogram_match(self) -> str:
        self.matcher = HistogramMatcher(temp_dir=self.temp_dir)
        self.matcher.setStep.connect(self.stepUpdated)
        self.matcher.stopped.connect(self.stopped)

        self.matcher.script(self.target_img_path, self.reference_img_path)
        styled_img_path = self.matcher.get_save_temp_path()
        return styled_img_path

    def _run_sty_tr(self) -> str:
        self.sty_tr = StyTr(temp_dir=self.temp_dir)
        self.sty_tr.setStep.connect(self.stepUpdated)
        self.sty_tr.stopped.connect(self.stopped)

        self.sty_tr.script(self.target_img_path, self.reference_img_path)
        styled_img_path = self.sty_tr.get_save_temp_path()
        return styled_img_path

    def set_image_paths(self, target_img_path: str, reference_img_path: str):
        self.target_img_path = target_img_path
        self.reference_img_path = reference_img_path

    def set_styled_selected(self, styled_selected: str):
        self.styled_selected = styled_selected

    def stop(self):
        self.is_running = False
        self.matcher.stop()


class SelectStyledImageBox(MessageBoxBase):
    def __init__(self, parent=None, styled_selected: str = StyledImageEnum.HISTOGRAM_MATCHER.value):
        super().__init__(parent)

        # 初始化选中的算法
        self.styled_selected = styled_selected  # 初始值

        self.titleLabel = SubtitleLabel(self.tr('Edit Run Configuration'), self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        label = BodyLabel(text=self.tr('Please select the algorithm to use:'))
        # noinspection PyUnresolvedReferences
        self.viewLayout.addWidget(label, 0, Qt.AlignLeft)

        self.button_group = QButtonGroup(self)
        for idx, enum_item in enumerate(StyledImageEnum):
            button = RadioButton(text=self.tr(enum_item.value))
            self.button_group.addButton(button, idx + 1)  # 按钮ID从1开始
            button.setChecked(enum_item.value == self.styled_selected)  # 默认选中第一个

            # noinspection PyUnresolvedReferences
            self.viewLayout.addWidget(button, 0, Qt.AlignLeft)

        self.widget.setMinimumWidth(350)

        # 连接信号
        self.button_group.buttonToggled.connect(self.on_button_toggled)

    def on_button_toggled(self, _):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            button_text = selected_button.text()
            self.styled_selected = button_text


class ImageGenerationPage(BasePage, Ui_ImitatePage):
    """图片生成页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.styled_selected = StyledImageEnum.HISTOGRAM_MATCHER.value

        self.temp_dir = r"temp"
        self.reference_img_path: Optional[str] = None
        self.target_img_path: Optional[str] = None
        self.styled_img_path: Optional[str] = None
        self.run_state: RunState = RunState.STOPPED
        self.image_generation_worker = ImageGenerationWorker(self, self.temp_dir, self.step_bar)

        self.set_run_state(RunState.STOPPED)

    def set_styled_selected(self, styled_selected: str):
        self.styled_selected = styled_selected

    def set_run_state(self, state: RunState):
        """设置运行状态"""
        self.run_state = state
        match state:
            case RunState.STOPPED | RunState.RERUN_AND_STOP:
                self.start_btn.setStopState()
                self.stop_btn.setStopState()
            case RunState.RUNNING:
                self.start_btn.setRunState()
                self.stop_btn.setRunState()
                self.styled_img_label.removeImage()
                self.styled_img_label.hideIcon()
            case RunState.STOPPING | RunState.RERUN_AND_STOPPING:
                self.start_btn.setStoppingState()
                self.stop_btn.setStoppingState()
        self.styled_btn.setDisabled(self.styled_img_label.isNull())

    @Slot()
    def on_start_btn_clicked(self):
        """处理开始按钮的点击事件"""
        match self.run_state:
            case RunState.STOPPED | RunState.RERUN_AND_STOP:
                self.generate_image()
            case RunState.RUNNING:
                self.generate_image_again()

    @Slot()
    def on_stop_btn_clicked(self):
        """处理停止按钮的点击事件"""
        match self.run_state:
            case RunState.RUNNING:
                self.reset_generate_status()
            case RunState.STOPPING:
                self.terminate_image_generation_worker()

    def generate_image(self):
        """生成风格化图像"""
        if self.check_generate_image():
            self.start_image_generation_task()

    def generate_image_again(self):
        """重新生成风格化图像"""
        self.set_run_state(RunState.RERUN_AND_STOPPING)
        self.reset_generate_status(rerun=True)

    def reset_generate_status(self, rerun: bool = False):
        """重置生成状态"""
        if rerun:
            self.set_run_state(RunState.RERUN_AND_STOPPING)
        else:
            self.set_run_state(RunState.STOPPING)

        self.image_generation_worker.stop()

    def terminate_image_generation_worker(self):
        """终止图片生成工作线程"""
        self.image_generation_worker.terminate()
        self.handle_image_generation_stopped()

    def check_image_isnull(self) -> bool:
        """检查是否选择了参考图像和目标图像"""
        return not (self.reference_img_label.image.isNull() or self.target_img_label.image.isNull())

    def check_generate_image(self) -> bool:
        """检查是否可以生成图像"""
        if not self.check_image_isnull():
            # noinspection PyUnresolvedReferences
            self.show_info_bar(
                InfoBar.error,
                title=self.tr('Error'),
                content=self.tr("Please select the reference image and target image first"),
                orient=Qt.Horizontal,
            )
            return False

        return self.check_temp_folder()

    def check_temp_folder(self) -> bool:
        """检查临时文件夹是否存在，不存在则创建一个"""
        if not os.path.exists(self.temp_dir):
            return self.create_temp_folder()
        else:
            return True

    def create_temp_folder(self) -> bool:
        """创建临时文件夹"""
        try:
            os.makedirs(self.temp_dir)
        except PermissionError:
            self.show_permission_dialog(require_admin_restart=True)
            return False
        else:
            return True

    def start_image_generation_task(self):
        """开始图片生成任务"""
        self.set_run_state(RunState.RUNNING)

        self.image_generation_worker.set_image_paths(self.target_img_path, self.reference_img_path)
        self.image_generation_worker.set_styled_selected(self.styled_selected)
        self.image_generation_worker.start()

    def handle_image_generation_stopped(self):
        """处理图片生成停止"""
        self.step_bar.setCurrentStep(0)

        assert self.run_state == RunState.STOPPING or self.run_state == RunState.RERUN_AND_STOPPING
        if self.run_state == RunState.STOPPING:
            self.set_run_state(RunState.STOPPED)
        elif self.run_state == RunState.RERUN_AND_STOPPING:
            self.set_run_state(RunState.RERUN_AND_STOP)

        if self.is_rerun_generating_image():
            self.generate_image()

    def handle_image_generation_finished(self, result):
        """处理图片生成完成"""
        if isinstance(result, Exception):
            # noinspection PyUnresolvedReferences
            self.show_info_bar(
                InfoBar.error,
                title=self.tr('Error'),
                content=f"{result}",
                orient=Qt.Horizontal,
            )
        else:
            self.styled_img_label.setImage(result)
            self.styled_img_label.scaledToHeight(170)
            self.styled_img_path = result

        self.set_run_state(RunState.STOPPED)

    def is_generating_image(self) -> bool:
        """检查是否正在生成图像"""
        return self.run_state == RunState.RUNNING

    def is_rerun_generating_image(self) -> bool:
        """检查是否需要重新生成图像"""
        return self.run_state == RunState.RERUN_AND_STOP


class ImitatePage(ImageGenerationPage):
    """模仿页面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.styled_img_label.hideIcon()
        self._set_styles()
        self._initialize_step_bar()
        self._set_tool_buttons()
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

        # 设置tooltip
        buttons = (
            (self.more_btn, 'More'),
            (self.folder_btn, 'Open temp folder'),
            (self.broom_btn, 'Clean temp files'),
            (self.reference_btn, 'Select Image'),
            (self.target_btn, 'Select Image'),
            (self.styled_btn, 'Save Image')
        )
        for button, tooltip in buttons:
            button.setToolTip(self.tr(tooltip))
            button.installEventFilter(ToolTipFilter(button, 300, ToolTipPosition.BOTTOM))

    def _connect_signals(self):
        """连接信号和槽"""
        self.more_btn.clicked.connect(self.create_more_menu)
        self.folder_btn.clicked.connect(self.open_temp_folder)
        self.broom_btn.clicked.connect(self.clear_temp_folder)
        self.reference_btn.clicked.connect(partial(self._select_image, 'reference'))
        self.target_btn.clicked.connect(partial(self._select_image, 'target'))
        self.styled_btn.clicked.connect(self.save_styled_image)
        self.image_generation_worker.stepUpdated.connect(self.step_bar.setCurrentStep)
        self.image_generation_worker.stopped.connect(self.handle_image_generation_stopped)
        self.image_generation_worker.finished.connect(self.handle_image_generation_finished)

    def _select_image(self, img_type):
        """选择图片并更新显示"""
        img_label = getattr(self, f"{img_type}_img_label")
        img_path_attr = f"{img_type}_img_path"

        def select_task():
            file_path = self._open_file_dialog()
            if file_path:
                cfg.set(cfg.pm_image_import, os.path.dirname(file_path))
                setattr(self, img_path_attr, file_path)
                img_label.setImage(file_path)
                img_label.scaledToHeight(170)
                self.step_bar.setCurrentStep(0)

        if self.is_generating_image():
            self.confirm_image_change(select_task)
        else:
            select_task()

    def save_styled_image(self):
        """保存生成的风格化图片"""
        file_path = self._save_file_dialog()
        if file_path:
            cfg.set(cfg.pm_image_export, os.path.dirname(file_path))

            try:
                shutil.copy(self.styled_img_path, file_path)
            except FileNotFoundError:
                self.show_info_bar(
                    InfoBar.error,
                    title=self.tr('Save failed'),
                    content=self.tr(
                        "File saving failed, please check whether the file path is correct. Or maybe the cache file has been deleted."),
                )
            except PermissionError:
                self.show_permission_dialog()
            else:
                w = self.show_info_bar(
                    InfoBar.success,
                    title=self.tr('Saved successfully'),
                    content=self.tr('File saved to:') + str(file_path),
                    show=False
                )
                btn = PushButton(text=self.tr('Open Directory'))
                btn.clicked.connect(lambda: reveal_file(file_path))
                w.addWidget(btn)
                w.show()
                if self.step_bar.getCurrentStep() == 7:
                    self.step_bar.setCurrentStep(8, animate=False)

    def _open_file_dialog(self) -> str:
        """打开文件选择对话框"""
        return QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), cfg.pm_image_import.value,
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )[0]

    def _save_file_dialog(self) -> str:
        """打开保存文件对话框"""
        directory = os.path.join(cfg.pm_image_export.value, "Styled Image")
        return QFileDialog.getSaveFileName(
            self, self.tr("Save Image File"), directory,
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )[0]

    def confirm_image_change(self, call_func: Callable):
        """确认是否更换图片"""
        m = MessageBox(self.tr("Change Picture Warning"),
                       self.tr(
                           "Replacing the image will cause the loaded image data to become invalid. You may need to re-execute the generation steps. Are you sure you want to continue?"),
                       self.window())
        m.setClosableOnMaskClicked(True)
        m.yesButton.clicked.connect(call_func)
        m.show()

    def create_more_menu(self):
        """创建"更多"菜单"""
        action = Action(text=self.tr('Modify running configuration...'))
        action.triggered.connect(self.show_config_box)
        menu = RoundMenu(parent=self)
        menu.addAction(action)
        pos = self.more_btn.mapToGlobal(QPoint(-menu.width() + 65, self.more_btn.height()))
        menu.exec(pos, ani=True)

    def show_config_box(self):
        """显示配置对话框"""
        m = SelectStyledImageBox(self.window(), self.styled_selected)
        m.yesButton.clicked.connect(lambda: self.set_styled_selected(m.styled_selected))
        m.show()

    def open_temp_folder(self):
        """打开临时文件夹"""
        if self.check_temp_folder():
            os.startfile(self.temp_dir)

    def clear_temp_folder(self):
        """清理临时文件夹"""

        def clear_task():
            if not os.path.exists(self.temp_dir):
                self.show_info_bar(
                    InfoBar.info,
                    title=self.tr("Clean temp files"),
                    content=self.tr("No cache folders, no need to clean")
                )
                return

            deleted_size = delete_files_except_whitelist(self.temp_dir, self.styled_img_path)
            if deleted_size == 0 and self.styled_img_path is None:
                self.show_info_bar(
                    InfoBar.info,
                    title=self.tr("Clean temp files"),
                    content=self.tr("No cache files, no need to clean")
                )
            else:
                self.show_info_bar(
                    InfoBar.success,
                    title=self.tr("Clean temp files"),
                    content=self.tr("Cleaning cache files successfully, total size of deleted files: ")
                            + format_size(deleted_size)
                )

        m = MessageBox(self.tr("Clean temp files"),
                       self.tr("This will delete all cached files. Are you sure you want to do this?"), self.window())
        m.setClosableOnMaskClicked(True)
        m.yesSignal.connect(clear_task)
        m.show()
