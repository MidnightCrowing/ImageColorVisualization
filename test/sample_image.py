from PIL import Image

from src.utils.getpixel import sample_image_colors

if __name__ == "__main__":
    image_path = r'./assets/test image.jpg'  # 替换为你的图片路径
    sampling_density = 100000  # 你想要的采样点数量

    image = Image.open(image_path)
    for color in sample_image_colors(image, sampling_density, color_space='RGB'):
        print(color)
    for color in sample_image_colors(image, sampling_density, color_space='HSL'):
        print(color)
