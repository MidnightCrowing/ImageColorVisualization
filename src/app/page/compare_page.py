from enum import Enum, auto
from functools import partial
from typing import Callable, NoReturn

from PySide6.QtWidgets import QWidget, QFileDialog, QButtonGroup
from qfluentwidgets import ImageLabel, FluentIcon, ToggleToolButton
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.vtk.vtk_manager import VTKManager
from ..ui.ui_ComparePage import Ui_ComparePage


class ToggleBtnGroupId(Enum):
    """按钮组的ID枚举，用于区分不同的按钮类型"""
    IMG = auto()
    POINT = auto()


class ComparePage(QWidget, Ui_ComparePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 创建两个按钮组，用于管理图片和点的切换按钮
        self.toggle_btn_group_1 = QButtonGroup(self)
        self.toggle_btn_group_2 = QButtonGroup(self)

        # 设置按钮图标和初始状态
        self._setup_buttons()

        # 初始化VTK管理器
        self._init_vtk_managers()

        # 连接信号与槽函数
        self._connect_signal()

    def _setup_buttons(self):
        """设置按钮图标、初始状态，并将按钮加入按钮组"""
        # 将按钮添加到各自的按钮组，并分配ID
        self.toggle_btn_group_1.addButton(self.toggle_btn_img_1, ToggleBtnGroupId.IMG.value)
        self.toggle_btn_group_1.addButton(self.toggle_btn_point_1, ToggleBtnGroupId.POINT.value)
        self.toggle_btn_group_2.addButton(self.toggle_btn_img_2, ToggleBtnGroupId.IMG.value)
        self.toggle_btn_group_2.addButton(self.toggle_btn_point_2, ToggleBtnGroupId.POINT.value)

        # 设置按钮组为互斥模式
        self.toggle_btn_group_1.setExclusive(True)
        self.toggle_btn_group_2.setExclusive(True)

        # 设置各按钮图标
        self.toggle_btn_img_1.setIcon(FluentIcon.PHOTO)
        self.toggle_btn_img_2.setIcon(FluentIcon.PHOTO)
        self.toggle_btn_point_1.setIcon(FluentIcon.PALETTE)
        self.toggle_btn_point_2.setIcon(FluentIcon.PALETTE)

        # 设置按钮初始状态
        self.toggle_btn_img_1.setChecked(True)
        self.toggle_btn_img_2.setChecked(True)

        # 初始化图片显示控件状态
        self.vtk_widget_1.setHidden(True)
        self.vtk_widget_2.setHidden(True)

    def _init_vtk_managers(self):
        """初始化 VTK 管理器"""
        self.vtk_manager_1 = VTKManager(self.vtk_widget_1)
        self.vtk_manager_2 = VTKManager(self.vtk_widget_2)
        self.vtk_manager_compare = VTKManager(self.vtk_widget_compare)

    def _connect_signal(self):
        """连接按钮组和其他控件的信号与槽函数"""
        # 连接选择按钮到文件选择对话框和更新函数
        self.select_btn_1.clicked.connect(
            partial(self.open_file_dialog, self.update_image, self.img_label_1, self.vtk_manager_1))
        self.select_btn_2.clicked.connect(
            partial(self.open_file_dialog, self.update_image, self.img_label_2, self.vtk_manager_2))

        # 连接按钮组的切换信号
        self.toggle_btn_group_1.buttonToggled.connect(
            partial(self.on_group_btn_toggled, self.toggle_btn_group_1, self.img_widget_1, self.vtk_widget_1))
        self.toggle_btn_group_2.buttonToggled.connect(
            partial(self.on_group_btn_toggled, self.toggle_btn_group_2, self.img_widget_2, self.vtk_widget_2))

    def open_file_dialog(self,
                         update_func: Callable[[str, ImageLabel, VTKManager], NoReturn],
                         img_label: ImageLabel,
                         vtk_manager: VTKManager):
        """打开文件对话框，并使用选中的图片路径更新图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        # 如果选择了文件，则加载并显示图片
        if file_path:
            update_func(file_path, img_label, vtk_manager)

    @staticmethod
    def update_image(image_path: str, img_label: ImageLabel, vtk_manager: VTKManager):
        """更新图像标签和VTK管理器的显示内容"""
        img_label.setImage(image_path)
        img_label.scaledToHeight(140)
        vtk_manager.set_image(image_path)

    @staticmethod
    def on_group_btn_toggled(button_group: QButtonGroup,
                             img_widget: QWidget,
                             vtk_widget: QVTKRenderWindowInteractor,
                             button: ToggleToolButton,
                             checked: bool):
        """处理按钮组的切换逻辑"""
        if checked:
            # 判断是图片按钮还是点按钮，并显示相应的控件
            if button_group.id(button) == ToggleBtnGroupId.IMG.value:
                # 显示图片并隐藏 VTK
                vtk_widget.setVisible(False)
                img_widget.setVisible(True)
            else:
                # 显示 VTK 并隐藏图片
                img_widget.setVisible(False)
                vtk_widget.setVisible(True)

    def close_vtk(self):
        """关闭 VTK 管理器"""
        self.vtk_manager_1.close()
        self.vtk_manager_2.close()
        self.vtk_widget_compare.close()

    def closeEvent(self, event):
        """重载窗口关闭事件，确保 VTK 资源释放"""
        self.close_vtk()
        event.accept()
