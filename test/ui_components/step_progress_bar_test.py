import os

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import isDarkTheme

from src.app.components import StepProgressBar
# noinspection PyUnresolvedReferences
import src.utils.config

if __name__ == "__main__":
    app = QApplication(sys.argv)

    steps = ["加载图片",
             "图片预处理",
             "提取参考色彩",
             "风格迁移计算",
             "颜色映射调整",
             "生成结果",
             "结果展示",
             "清理与保存"]

    progress_bar = StepProgressBar(current_step=3)
    progress_bar.setWindowTitle("步骤进度条")
    progress_bar.setStyleSheet(f"background-color: {"#202020" if isDarkTheme() else "#F0F0F0"}")
    progress_bar.setSteps(steps)
    progress_bar.resize(900, 80)
    progress_bar.show()

    sys.exit(app.exec())
