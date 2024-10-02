from pathlib import Path

import cv2
import numpy as np

from .styled_image_worker import StyledImageWorker


def get_gray_histogram(img):
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


def get_gray_cumulative_prop(gray):
    """
    获取累积分布直方图
    :param gray: 灰度直方图
    :return: 累积分布
    """
    cum_gray = np.cumsum(gray)
    return cum_gray


def match_histograms(src, ref):
    """
    匹配源图像和参考图像的直方图
    :param src: 源图像灰度图
    :param ref: 参考图像灰度图
    :return: 匹配后的图像
    """
    src_hist = get_gray_histogram(src)
    ref_hist = get_gray_histogram(ref)
    src_cdf = get_gray_cumulative_prop(src_hist)
    ref_cdf = get_gray_cumulative_prop(ref_hist)

    # 创建映射表
    mapping = np.zeros(256, dtype=int)
    for i in range(256):
        diff = np.abs(ref_cdf - src_cdf[i])
        mapping[i] = np.argmin(diff)

    # 应用映射
    matched = mapping[src]
    return matched


class HistogramMatcher(StyledImageWorker):
    def __init__(self, temp_dir: str = None):
        super().__init__(temp_dir=temp_dir)
        self.file_name_prefix = 'matched_image'

    def run(self, file_path2: str, file_path3: str, *args, **kwargs):
        """
        运行彩色图像直方图匹配并更新进度条
        :param file_path2: 原图路径
        :param file_path3: 参考图路径
        """
        # 加载图片
        img_pix1 = self.load_img_pix(file_path2)
        img_pix2 = self.load_img_pix(file_path3)

        # 分离 R、G、B 通道
        channels1 = self.separate_rgb_channels(img_pix1)
        channels2 = self.separate_rgb_channels(img_pix2)

        # 对每个通道进行直方图匹配
        matched_channels = self.histogram_matching_for_each_channel(channels1, channels2)

        # 合并匹配后的通道
        matched_img = self.merge_matched_channels(matched_channels)

        # 显示结果
        self.save_image(matched_img)

    @StyledImageWorker.step(1)
    def load_img_pix(self, file_path: str) -> np.ndarray:
        """
        获取图片的彩色像素值并更新进度条

        :param file_path: 图片路径
        :return: 读取的图像
        """
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

    @StyledImageWorker.step(3)
    def separate_rgb_channels(self, img_pix):
        return cv2.split(img_pix)

    @StyledImageWorker.step(4)
    def histogram_matching_for_each_channel(self, channels1, channels2):
        matched_channels = []
        for ch1, ch2 in zip(channels1, channels2):
            matched_channel = match_histograms(ch1, ch2)
            matched_channels.append(matched_channel)
        return matched_channels

    @StyledImageWorker.step(5)
    def merge_matched_channels(self, matched_channels):
        return cv2.merge(matched_channels)

    @StyledImageWorker.step(7)
    def save_image(self, matched_img):
        """保存匹配后的图像到指定文件夹，使用时间戳命名"""
        assert matched_img is not None, "没有可保存的图片"
        file_path = self.get_file_path()
        cv2.imwrite(file_path, matched_img)  # 保存图像
