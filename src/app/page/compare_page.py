from enum import Enum, auto
from functools import partial

from PySide6.QtWidgets import QWidget, QFileDialog, QButtonGroup
from qfluentwidgets import FluentIcon, ToggleToolButton
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.point_cloud import VTKManager, find_overlapped_cloud
from .base_page import BasePage
from ..components import ImageLabelCard
from ..ui.ui_ComparePage import Ui_ComparePage


class ToggleBtnGroupId(Enum):
    IMG = auto()
    POINT = auto()


class DisplayBtnGroupId(Enum):
    COLOR = auto()
    SOLID = auto()
    OVERLAP = auto()


class OverlapBtnGroupId(Enum):
    HIDE = auto()
    SHOW = auto()
    ONLY = auto()


class ComparePage(BasePage, Ui_ComparePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 设置按钮图标和初始状态
        self._setup_buttons()

        # 初始化 VTK 控件状态
        self._setup_vtk_widgets()

        # 初始化VTK管理器
        self._init_vtk_managers()

        self.point_color_1 = (255, 107, 158)
        self.point_color_2 = (144, 93, 255)
        self.point_color_compare = (0, 234, 255)

        self.cloud_actor_1 = self.vtk_manager_compare.add_null_cloud_actor()
        self.cloud_actor_2 = self.vtk_manager_compare.add_null_cloud_actor()
        self.cloud_compare_actor = self.vtk_manager_compare.add_null_cloud_actor()

        self.cloud_data_1 = []
        self.cloud_data_2 = []

        # 连接信号与槽函数
        self._connect_signal()

    def _setup_buttons(self):
        """设置按钮图标、初始状态，并将按钮加入按钮组"""
        # 创建按钮组，用于管理图片和点的切换按钮
        self.toggle_btn_group_1 = QButtonGroup(self)
        self.toggle_btn_group_2 = QButtonGroup(self)
        self.display_btn_group = QButtonGroup(self)
        self.overlap_btn_group = QButtonGroup(self)

        # 将按钮添加到各自的按钮组，并分配ID
        self.toggle_btn_group_1.addButton(self.toggle_btn_img_1, ToggleBtnGroupId.IMG.value)
        self.toggle_btn_group_1.addButton(self.toggle_btn_point_1, ToggleBtnGroupId.POINT.value)
        self.toggle_btn_group_2.addButton(self.toggle_btn_img_2, ToggleBtnGroupId.IMG.value)
        self.toggle_btn_group_2.addButton(self.toggle_btn_point_2, ToggleBtnGroupId.POINT.value)
        self.display_btn_group.addButton(self.disp_btn_color, DisplayBtnGroupId.COLOR.value)
        self.display_btn_group.addButton(self.disp_btn_solid, DisplayBtnGroupId.SOLID.value)
        self.overlap_btn_group.addButton(self.olap_btn_hide, OverlapBtnGroupId.HIDE.value)
        self.overlap_btn_group.addButton(self.olap_btn_show, OverlapBtnGroupId.SHOW.value)
        self.overlap_btn_group.addButton(self.olap_btn_only, OverlapBtnGroupId.ONLY.value)

        # 设置按钮组为互斥模式
        self.toggle_btn_group_1.setExclusive(True)
        self.toggle_btn_group_2.setExclusive(True)
        self.display_btn_group.setExclusive(True)

        # 设置各按钮图标
        self.toggle_btn_img_1.setIcon(FluentIcon.PHOTO)
        self.toggle_btn_img_2.setIcon(FluentIcon.PHOTO)
        self.toggle_btn_point_1.setIcon(FluentIcon.PALETTE)
        self.toggle_btn_point_2.setIcon(FluentIcon.PALETTE)

        # 设置按钮初始状态
        self.toggle_btn_img_1.setChecked(True)
        self.toggle_btn_img_2.setChecked(True)
        self.disp_btn_color.setChecked(True)
        self.olap_btn_show.setChecked(True)

    def _setup_vtk_widgets(self):
        # 初始化图片显示控件状态
        self.vtk_widget_1.setHidden(True)
        self.vtk_widget_2.setHidden(True)

    def _init_vtk_managers(self):
        """初始化 VTK 管理器"""
        self.vtk_manager_1 = self.vtk_widget_1.vtk_manager
        self.vtk_manager_2 = self.vtk_widget_2.vtk_manager
        self.vtk_manager_compare = self.vtk_widget_compare.vtk_manager

        # 同步两个 VTK 窗口的场景
        self.vtk_manager_1.sync_scene(self.vtk_manager_2)
        self.vtk_manager_2.sync_scene(self.vtk_manager_1)

    def _connect_signal(self):
        """连接按钮组和其他控件的信号与槽函数"""
        # 连接选择按钮到文件选择对话框和更新函数
        self.select_btn_1.clicked.connect(partial(self.select_btn_clicked, 1))
        self.select_btn_2.clicked.connect(partial(self.select_btn_clicked, 2))

        # 连接按钮组的切换信号
        self.toggle_btn_group_1.buttonToggled.connect(
            partial(self.on_group_btn_toggled, self.toggle_btn_group_1, self.img_widget_1, self.vtk_widget_1))
        self.toggle_btn_group_2.buttonToggled.connect(
            partial(self.on_group_btn_toggled, self.toggle_btn_group_2, self.img_widget_2, self.vtk_widget_2))

        self.disp_btn_color.clicked.connect(self.disp_changed_color)
        self.disp_btn_solid.clicked.connect(self.disp_changed_solid)
        self.olap_btn_hide.clicked.connect(self.olap_changed_hide)
        self.olap_btn_show.clicked.connect(self.olap_changed_show)
        self.olap_btn_only.clicked.connect(self.olap_changed_only)

    def select_btn_clicked(self, btn_id: int):
        file_path = self.open_file_dialog()
        if file_path is None:
            return

        img_label = getattr(self, f'img_label_{btn_id}')
        vtk_manager = getattr(self, f'vtk_manager_{btn_id}')
        cloud_actor_compare = getattr(self, f'cloud_actor_{btn_id}')

        cloud_actor = self.update_image(file_path, img_label, vtk_manager)
        cloud_actor_compare.set_vtk_polydata(cloud_actor.get_vtk_polydata(), copy=True)

        polydata_1 = self.cloud_actor_1.get_vtk_polydata()
        polydata_2 = self.cloud_actor_2.get_vtk_polydata()
        polydata_group = (polydata_1, polydata_2) if btn_id == 1 else (polydata_2, polydata_1)
        polydata = find_overlapped_cloud(*polydata_group)
        self.cloud_compare_actor.set_vtk_polydata(polydata)

    def open_file_dialog(self):
        """打开文件对话框，并使用选中的图片路径更新图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Image File"), "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        # 如果选择了文件，则加载并显示图片
        if file_path:
            return file_path

    @staticmethod
    def update_image(image_path: str, img_label_card: ImageLabelCard, vtk_manager: VTKManager):
        """更新图像标签和VTK管理器的显示内容"""
        img_label_card.setImage(image_path)
        img_label_card.scaledToHeight(170)
        cloud_actor = vtk_manager.set_image(image_path)
        return cloud_actor

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

    def disp_changed_color(self):
        self.cloud_actor_1.remove_mask_cloud_actor()
        self.cloud_actor_2.remove_mask_cloud_actor()
        self.cloud_compare_actor.remove_mask_cloud_actor()

        self.vtk_manager_compare.render()

    def disp_changed_solid(self):
        self.cloud_actor_1.set_mask_cloud_actor(self.point_color_1)
        self.cloud_actor_2.set_mask_cloud_actor(self.point_color_2)
        self.cloud_compare_actor.set_mask_cloud_actor(self.point_color_compare)

        self.vtk_manager_compare.render()

    def olap_changed_hide(self):
        self.cloud_actor_1.show()
        self.cloud_actor_2.show()
        self.cloud_compare_actor.hide()

        self.vtk_manager_compare.render()

    def olap_changed_show(self):
        self.cloud_actor_1.show()
        self.cloud_actor_2.show()
        self.cloud_compare_actor.show()

        self.vtk_manager_compare.render()

    def olap_changed_only(self):
        self.cloud_actor_1.hide()
        self.cloud_actor_2.hide()
        self.cloud_compare_actor.show()

        self.vtk_manager_compare.render()

    def close_vtk(self):
        """关闭 VTK 管理器"""
        self.vtk_manager_1.close()
        self.vtk_manager_2.close()
        self.vtk_manager_compare.close()

    def closeEvent(self, event):
        """重载窗口关闭事件，确保 VTK 资源释放"""
        self.close_vtk()
        event.accept()
