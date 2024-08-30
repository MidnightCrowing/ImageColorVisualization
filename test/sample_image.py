import yaml

from src.utils.getpixel import sample_image_colors


def read_sampling_density(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

        return config.get('SAMPLING_DENSITY', None)


if __name__ == "__main__":
    image_path = r'./assets/test image.jpg'  # 替换为你的图片路径
    sampling_density = 100000  # 你想要的采样点数量

    for color in sample_image_colors(image_path, sampling_density, color_space='RGB'):
        print(color)
    for color in sample_image_colors(image_path, sampling_density, color_space='HSL'):
        print(color)
