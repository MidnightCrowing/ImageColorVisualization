from src.image_color_analyzer import extract_dominant_colors

if __name__ == "__main__":
    image_path = r'images/test image.jpg'  # 替换为你的图片路径
    dominant_colors = extract_dominant_colors(image_path, k=5)
    print(dominant_colors)
