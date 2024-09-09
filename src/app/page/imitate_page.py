from PySide6.QtWidgets import QWidget

from ..ui.ui_ImitatePage import Ui_ImitatePage


class ImitatePage(QWidget, Ui_ImitatePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # TODO: Imitate page
        self.widget.setFixedSize(900, 80)
        self.widget.setSteps(["加载图片",
             "图片预处理",
             "提取参考色彩",
             "风格迁移计算",
             "颜色映射调整",
             "生成结果",
             "结果展示",
             "清理与保存"])
        self.widget.setCurrentStep(3)
