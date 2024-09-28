import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 字体列表
FONT_FAMILY = ["JetBrains Mono", "Consolas", "HarmonyOS Sans", "Arial", "DejaVu Sans"]


def generate_dominant_color_chart(colors, file_path: str, block_size=1.2, margin=0.2, text_size=12,
                                  frame_on=False) -> bool:
    num_colors = len(colors)

    # 设置图片的大小，包含色块大小和色块之间的间隔，并且预留一些边距
    fig, ax = plt.subplots(figsize=((block_size + margin) * num_colors, block_size + 1.2))

    # 尝试使用字体列表中的字体
    font_properties = None
    for font in FONT_FAMILY:
        try:
            font_properties = FontProperties(family=font)
            # 检查字体是否可用
            if font_properties.get_name() != font:
                continue
            break  # 找到合适的字体后退出循环
        except Exception:
            continue  # 继续尝试下一个字体

    # 如果没有找到合适的字体，则使用默认字体
    if font_properties is None:
        font_properties = FontProperties()

    # 绘制每个颜色块
    for idx, color in enumerate(colors):
        # 将RGB值映射到0-1之间
        normalized_color = [c / 255.0 for c in color]

        # 计算每个颜色块的左下角位置 (idx * (block_size + margin))
        rect = plt.Rectangle((idx * (block_size + margin), 0.5), block_size, block_size,
                             facecolor=normalized_color, edgecolor=None)  # 移除色块边框
        ax.add_patch(rect)

        # 转换颜色为十六进制格式并作为标签，颜色与色块一致
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        ax.text(idx * (block_size + margin) + block_size / 2, 0.4, hex_color,
                va='top', ha='center', fontsize=text_size, color=hex_color, fontproperties=font_properties)

    # 移除x轴和y轴
    ax.set_xticks([])
    ax.set_yticks([])

    # 调整显示范围，只显示绘制区域
    ax.set_xlim(-margin, num_colors * (block_size + margin))
    ax.set_ylim(0, block_size + 0.8)  # 增加ylim的范围，使得色块和文字更接近中心

    if frame_on:
        # 设置边框线为浅灰色
        ax.spines['top'].set_color('#D3D3D3')
        ax.spines['right'].set_color('#D3D3D3')
        ax.spines['left'].set_color('#D3D3D3')
        ax.spines['bottom'].set_color('#D3D3D3')

        ax.spines['top'].set_linewidth(1)
        ax.spines['right'].set_linewidth(1)
        ax.spines['left'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
    else:
        ax.set_frame_on(False)

    # 设置边距，使内容在画布中间更居中
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.2)

    # 保存并显示图片，设置 DPI 提高分辨率
    try:
        plt.savefig(file_path, bbox_inches='tight', dpi=300)
    except PermissionError:
        return False
    return True
