import base64
import json

import requests


# 将图片文件转换为 Base64 字符串
def encode_image_to_base64(image_path):
    """
    将指定路径的图片转换为 Base64 编码字符串。

    :param image_path: 图片文件的路径
    :return: Base64 编码的字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 设置API请求的URL
url = "http://localhost:7860/sdapi/v1/img2img"  # API地址

# 将图片编码为 Base64
base64_image = encode_image_to_base64(r'./assets/test image.jpg')

# 设置请求头
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# 设置请求体数据
data = {
    "batch_size": 1,  # 一次处理的图像数量
    "steps": 20,  # 生成图像的步数
    "sampler_name": "DPM++ 2M",  # 采样器名称
    "width": 640 * 2,  # 输出图像的宽度
    "height": 448 * 2,  # 输出图像的高度
    "denoising_strength": 0.1,  # 去噪强度(建议0.1~0.3之间)
    "tiling": True,  # 是否启用平铺
    "do_not_save_samples": False,  # 是否不保存样本
    "do_not_save_grid": False,  # 是否不保存网格图像
    "init_images": [base64_image],  # 初始图像的 Base64 编码
    "send_images": True,  # 是否发送生成的图像
    "save_images": True,  # 是否保存生成的图像
    "alwayson_scripts": {
        "Tiled Diffusion": {  # Tiled Diffusion 的配置
            "args": [
                True,  # 是否使用 Tiled Diffusion
                "MultiDiffusion",  # 方案
                False,  # 是否覆盖输入图像大小
                True,  # 是否保持输入图像的原始大小
                1024,  # 图像宽度
                1024,  # 图像高度
                96,  # 潜空间分块宽度（处理时分块的宽度）
                96,  # 潜空间分块高度（处理时分块的高度）
                48,  # 潜空间分块重叠（分块之间的重叠像素）
                4,  # 潜空间分块单批数量（单次处理的分块数量）
                "R-ESRGAN 4x+",  # 放大算法
                2,  # 放大倍数
                False,  # 是否使用噪声反转
                10,  # 反转步数
                1,  # 修复程度
                1,  # 重铺噪声强度
                64,  # 重铺噪声大小
                False,  # 将ControlNet张量移至CPU（如果适用，将控制张量移至CPU）
                False,  # 是否启用边界框控制机制
                False,  # 是否绘制背景层
                False,  # 是否启用因果层设置
            ]
        },
        "Tiled VAE": {  # Tiled VAE 的配置
            "args": [
                True,  # 是否使用 Tiled VAE
                512,  # 编码器分块大小
                64,  # 解码器分块大小
                True,  # 将VAE移动到GPU (如果允许)
                True,  # 使用快速解码器
                True,  # 使用快速编码器
                False,  # 颜色修复
            ]
        }
    }
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 输出响应状态码和结果
print(response.status_code)  # 输出状态码
try:
    print(response.json())  # 输出响应内容
except json.JSONDecodeError:
    print("响应内容不是有效的JSON格式")
