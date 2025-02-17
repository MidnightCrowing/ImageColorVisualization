import colorsys
import random
from typing import Literal

import numpy as np
from PIL import Image


def load_image_pixels(image: Image) -> tuple[np.ndarray, int, int]:
    """
    加载图片并返回其像素数组

    :param image: PIL 图片
    :return: 像素数组, 图片宽度, 图片高度
    """
    # 将图片转换为 RGB 模式
    image = image.convert('RGB')
    width, height = image.size
    # 将图片数据转换为 NumPy 数组
    pixels = np.array(image)
    return pixels, width, height


def sample_indices(total_pixels, sampling_density):
    """
    生成采样点的索引

    :param total_pixels: 总像素数量
    :param sampling_density: 采样点的数量
    :return: 采样点的索引列表
    """
    assert isinstance(total_pixels, int) and total_pixels > 0
    assert isinstance(sampling_density, int) and sampling_density > 0
    if sampling_density > total_pixels:
        sampling_density = total_pixels
    print(f"总像素数量: {total_pixels}\t采样点数量: {sampling_density}")
    return random.sample(range(total_pixels), sampling_density)


def sample_image_colors(pil_image: Image, sampling_density: int, color_space: Literal['RGB', 'HSL'] = 'HSL'):
    """
    从图片中采样指定数量的颜色值

    :param pil_image: PIL 图片
    :param sampling_density: 采样点的数量
    :param color_space: 颜色空间 ('RGB' 或 'HSL')
    :yield: 颜色值
    """
    pixels, width, height = load_image_pixels(pil_image)
    total_pixels = width * height
    indices = sample_indices(total_pixels, sampling_density)

    for index in indices:
        x = index % width
        y = index // width
        r, g, b = tuple(pixels[y, x])

        if color_space == 'RGB':
            yield r, g, b
        elif color_space == 'HSL':
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            yield h * 360, s, l
        else:
            raise ValueError("Unsupported color space. Use 'RGB' or 'HSL'.")
