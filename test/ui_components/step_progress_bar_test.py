import os

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

from qfluentwidgets import isDarkTheme, PushButton
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from src.app.components import StepProgressBar
# noinspection PyUnresolvedReferences
import src.utils.config


class StepProgressBarTest(QWidget):
    def __init__(self, steps):
        super().__init__()

        self.step_bar = StepProgressBar(steps=steps, current_step=0, line_width=5, font_size=12)
        self.next_button = PushButton(text="Next Step")
        self.next_button.clicked.connect(self.goToNextStep)

        layout = QVBoxLayout(self)
        layout.addWidget(self.step_bar)
        layout.addWidget(self.next_button)

    def goToNextStep(self):
        current_step = self.step_bar.getCurrentStep()
        if current_step < len(self.step_bar.steps):
            if current_step == len(self.step_bar.steps) - 1:
                self.step_bar.setCurrentStep(current_step + 1, False)
                self.next_button.setText("Finish")
            else:
                self.step_bar.setCurrentStep(current_step + 1)
        else:
            self.step_bar.setCurrentStep(0)
            self.next_button.setText("Next Step")


if __name__ == "__main__":
    app = QApplication([])

    steps = [
        "加载图片", "图片预处理", "提取参考色彩", "风格迁移计算",
        "颜色映射调整", "生成结果", "结果展示", "清理与保存"
    ]

    progress_bar = StepProgressBarTest(steps)
    progress_bar.setWindowTitle("StepProgressBar")
    progress_bar.setStyleSheet(f"background-color: {'#202020' if isDarkTheme() else '#f0f4f9'}")
    progress_bar.resize(900, 150)
    progress_bar.show()

    app.exec()
