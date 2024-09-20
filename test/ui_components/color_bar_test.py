import os

print("当前工作目录:", os.getcwd())
os.chdir("../../")  # 修改工作目录到项目根目录
print("修改后工作目录:", os.getcwd())

import sys

import cv2
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from qfluentwidgets import ToolTipPosition, ToolTipFilter, isDarkTheme, PushButton
from sklearn.cluster import KMeans

from src.app.components import ColorBar
# noinspection PyUnresolvedReferences
import src.utils.config


class ColorBarTest(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        self.layout = QVBoxLayout(self)

        # Create and add the ColorBar widget
        self.color_bar = ColorBar(self)
        self.tooltip_filter = ToolTipFilter(self.color_bar, showDelay=-1, position=ToolTipPosition.TOP)
        self.color_bar.installEventFilter(self.tooltip_filter)
        self.color_bar.tooltip_filter = self.tooltip_filter
        self.layout.addWidget(self.color_bar)

        self.show_dominant_colors()

    def load_image(self):
        """Load and store the image"""
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image = image

    def show_dominant_colors(self):
        """Extract and display dominant colors in the ColorBar"""
        dominant_colors = [(112, 82, 89),
                           (17, 21, 66),
                           (43, 97, 160),
                           (228, 191, 126),
                           (16, 48, 115)]
        self.color_bar.setColors(dominant_colors)

    def get_dominant_colors(self, image, k=5):
        """Use KMeans to find the dominant colors in the image"""
        pixels = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int)


image_path = r'C:\Users\lenovo\Pictures\b_2feb4198a9d76db5ff777cdd1b4e9cb6.jpg'

if __name__ == "__main__":
    app = QApplication(sys.argv)

    color_bar = ColorBarTest()
    color_bar.setWindowTitle("ColorBar")
    color_bar.setStyleSheet(f"background-color: {'#202020' if isDarkTheme() else '#f0f4f9'}")
    color_bar.resize(900, 150)
    color_bar.show()

    sys.exit(app.exec())