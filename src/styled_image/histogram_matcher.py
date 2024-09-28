import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PySide6.QtCore import SignalInstance


class HistogramMatcher:
    def __init__(self, temp_dir: str = r"temp", step_signal: SignalInstance = None):
        """
        初始化直方图匹配类
        :param step_signal: 用于更新进度条的信号
        """
        self.temp_dir = temp_dir  # 临时文件夹路径
        self.step_signal: Optional[SignalInstance] = step_signal
        self.matched_img = None  # 用于保存匹配后的图像
        self.save_temp_path: Optional[str] = None  # 保存路径

    def load_img_pix(self, file_path: str, step_index: int) -> np.ndarray:
        """
        获取图片的彩色像素值并更新进度条

        :param file_path: 图片路径
        :param step_index: 进度条步骤索引
        :return: 读取的图像
        """
        if self.step_signal is not None:
            self.step_signal.emit(step_index)

        # 使用 pathlib 处理路径
        file_path = str(Path(file_path))

        try:
            # 读取图像文件为二进制数据
            with open(file_path, 'rb') as f:
                img_array = np.frombuffer(f.read(), np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 读取彩色图像

            if img is None:
                raise FileNotFoundError(f"无法读取图像: {file_path}")

            return img

        except Exception as e:
            raise FileNotFoundError(f"无法读取图像: {file_path}") from e

    def get_gray_histogram(self, img):
        """
        获取图像的灰度直方图
        :param img: 输入图像
        :return: 灰度直方图
        """
        gray = np.zeros(256)
        height, width = img.shape
        for h in range(height):
            for w in range(width):
                gray[img[h][w]] += 1
        gray /= (height * width)  # 归一化
        return gray

    def get_gray_cumulative_prop(self, gray):
        """
        获取累积分布直方图
        :param gray: 灰度直方图
        :return: 累积分布
        """
        cum_gray = np.cumsum(gray)
        return cum_gray

    def match_histograms(self, src, ref):
        """
        匹配源图像和参考图像的直方图
        :param src: 源图像灰度图
        :param ref: 参考图像灰度图
        :return: 匹配后的图像
        """
        src_hist = self.get_gray_histogram(src)
        ref_hist = self.get_gray_histogram(ref)
        src_cdf = self.get_gray_cumulative_prop(src_hist)
        ref_cdf = self.get_gray_cumulative_prop(ref_hist)

        # 创建映射表
        mapping = np.zeros(256, dtype=int)
        for i in range(256):
            diff = np.abs(ref_cdf - src_cdf[i])
            mapping[i] = np.argmin(diff)

        # 应用映射
        matched = mapping[src]
        return matched

    def run_histogram_match(self, file_path2: str, file_path3: str):
        """
        运行彩色图像直方图匹配并更新进度条
        :param file_path2: 原图路径
        :param file_path3: 参考图路径
        """
        # 加载图片
        img_pix1 = self.load_img_pix(file_path2, 1)  # Load Images
        img_pix2 = self.load_img_pix(file_path3, 1)  # Load Images

        # 分离 R、G、B 通道
        if self.step_signal is not None:
            self.step_signal.emit(3)  # Extract Reference Colors
        channels1 = cv2.split(img_pix1)
        channels2 = cv2.split(img_pix2)

        # 对每个通道进行直方图匹配
        if self.step_signal is not None:
            self.step_signal.emit(4)  # Style Transfer Calculation
        matched_channels = []
        for ch1, ch2 in zip(channels1, channels2):
            matched_channel = self.match_histograms(ch1, ch2)
            matched_channels.append(matched_channel)

        # 合并匹配后的通道
        if self.step_signal is not None:
            self.step_signal.emit(5)  # Color Mapping Adjustment
        self.matched_img = cv2.merge(matched_channels)

        # 显示结果
        if self.step_signal is not None:
            self.step_signal.emit(7)  # Display Result
        self.save_image()

    def save_image(self):
        """保存匹配后的图像到指定文件夹，使用时间戳命名"""
        assert self.matched_img is not None, "没有可保存的图片"

        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.temp_dir, f"matched_image_{timestamp}.jpg")

        # 保存图像
        cv2.imwrite(file_path, self.matched_img)

        self.save_temp_path = file_path

    def get_save_temp_path(self) -> str:
        return self.save_temp_path
