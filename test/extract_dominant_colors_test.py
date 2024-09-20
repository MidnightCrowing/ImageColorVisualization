from src.utils.extract_dominant_colors import extract_dominant_colors

if __name__ == "__main__":
    image_path = r'./assets/test image.jpg'  # 替换为你的图片路径
    dominant_colors = extract_dominant_colors(image_path, k=5)
    print(dominant_colors)
