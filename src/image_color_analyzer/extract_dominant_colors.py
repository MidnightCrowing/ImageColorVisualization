from typing import List, Tuple

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def load_image(image_path: str) -> np.ndarray:
    """Load and store the image"""
    image = Image.open(image_path).convert('RGB')  # 直接转换为 RGB 格式
    return np.array(image)  # 转换为 NumPy 数组


def get_dominant_colors(image: np.ndarray, k: int) -> List[Tuple[int, int, int]]:
    """Use KMeans to find the dominant colors in the image"""
    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    return kmeans.cluster_centers_.astype(int)


def extract_dominant_colors(image_path: str, k: int = 5) -> List[Tuple[int, int, int]]:
    """使用KMeans聚类算法来提取图像中的主色调"""
    image = load_image(image_path)
    dominant_colors = get_dominant_colors(image, k)
    return dominant_colors
