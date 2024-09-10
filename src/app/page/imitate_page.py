from PySide6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import isDarkTheme, FluentIcon

from ..ui.ui_ImitatePage import Ui_ImitatePage


class ImitatePage(QWidget, Ui_ImitatePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
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
        self.step_bar.setCurrentStep(3)

        # 设置工具栏按钮图标
        self.reference_tool_btn.setIcon(FluentIcon.LABEL)
        self.target_tool_btn.setIcon(FluentIcon.LABEL)
        self.style_tool_btn.setIcon(FluentIcon.SAVE)

        # 隐藏图标
        self.style_img_label.hideIcon()

        # 设置信号槽
        self._connect_signals()

    def _connect_signals(self):
        self.reference_tool_btn.clicked.connect(self.set_reference_img)
        self.target_tool_btn.clicked.connect(self.set_target_img)
        self.style_tool_btn.clicked.connect(self.save_style_img)
        # self.style_img_label.setImage(r"C:\Users\lenovo\Pictures\网络资源\都市.jpg")
        # self.style_img_label.scaledToHeight(140)

    def set_reference_img(self):
        file_path = self.open_file_dialog()
        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.reference_img_label.setImage(file_path)
            self.reference_img_label.scaledToHeight(170)

    def set_target_img(self):
        file_path = self.open_file_dialog()
        # 如果选择了文件，则加载并显示图片
        if file_path:
            self.target_img_label.setImage(file_path)
            self.target_img_label.scaledToHeight(170)

    def save_style_img(self):
        file_path = self.save_file_dialog()
        # 检查是否选择了文件路径
        if file_path:
            pass

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
