import base64
import json
from io import BytesIO

import requests
from PIL import Image

from src.utils.config import cfg


# 将图片文件转换为 Base64 字符串
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 将PIL图像转换为Base64字符串
def pil_image_to_base64(image: Image, format: str = "PNG") -> str:
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


# 将Base64字符串转换为PIL图像
def base64_to_pil_image(base64_str: str) -> Image:
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    return image


def send_requests(base64_image: str, image_width: int, image_height: int, scale_factor: int) -> str:
    # 设置URL
    url = f"http://{cfg.sd_ip.value}:{cfg.sd_port.value}/sdapi/v1/img2img"

    # 设置请求头
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # 设置请求体数据
    data = {
        "batch_size": 1,
        "steps": cfg.sd_steps.value,
        "sampler_name": cfg.sd_sampler_name.value.value,
        "width": image_width,
        "height": image_height,
        "denoising_strength": cfg.sd_denoising_strength.doubleValue,
        "tiling": True,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "init_images": [base64_image],  # 使用Base64编码的图片
        "send_images": True,
        "save_images": True,
        "alwayson_scripts": {
            "Tiled Diffusion": {
                "args": [
                    True,  # 是否使用 Tiled Diffusion
                    cfg.td_method.value.value,  # 方案
                    cfg.td_overwrite_size.value,  # 是否覆盖输入图像大小
                    cfg.td_keep_input_size.value,  # 是否保持输入图像的原始大小
                    cfg.td_image_width.value,  # 图像宽度
                    cfg.td_image_height.value,  # 图像高度
                    cfg.td_tile_width.value,  # 潜空间分块宽度（处理时分块的宽度）
                    cfg.td_tile_height.value,  # 潜空间分块高度（处理时分块的高度）
                    cfg.td_tile_overlap.value,  # 潜空间分块重叠（分块之间的重叠像素）
                    cfg.td_tile_batch_size.value,  # 潜空间分块单批数量（单次处理的分块数量）
                    cfg.td_upscaler_name.value.value,  # 放大算法
                    int(scale_factor),  # 放大倍数
                    cfg.td_noise_inverse.value,  # 是否使用噪声反转
                    cfg.td_noise_inverse_steps.value,  # 反转步数
                    cfg.td_noise_inverse_retouch.doubleValue,  # 修复程度
                    cfg.td_noise_inverse_renoise_strength.doubleValue,  # 重铺噪声强度
                    cfg.td_noise_inverse_renoise_kernel.value,  # 重铺噪声大小
                    cfg.td_control_tensor_cpu.value,  # 将ControlNet张量移至CPU（如果适用，将控制张量移至CPU）
                    cfg.td_enable_bbox_control.value,  # 是否启用边界框控制机制
                    cfg.td_draw_background.value,  # 是否绘制背景层
                    cfg.td_causal_layers.value,  # 是否启用因果层设置
                ]
            },
            "Tiled VAE": {
                "args": [
                    True,  # 是否使用 Tiled VAE
                    cfg.tv_encoder_tile_size.value,  # 编码器分块大小
                    cfg.tv_decoder_tile_size.value,  # 解码器分块大小
                    cfg.tv_vae_to_gpu.value,  # 将VAE移动到GPU (如果允许)
                    cfg.tv_fast_decoder.value,  # 使用快速解码器
                    cfg.tv_fast_encoder.value,  # 使用快速编码器
                    cfg.tv_color_fix.value,  # 颜色修复
                ]
            }
        }
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    try:
        generated_base64_image = response.json()['images'][0]
    except KeyError | IndexError:
        print(response.json())
        raise

    return generated_base64_image


def generate_image(image: Image, scale_factor: int) -> Image:
    image_width, image_height = image.size
    base64_image = pil_image_to_base64(image)
    generated_base64_image = send_requests(base64_image, image_width, image_height, scale_factor)
    return base64_to_pil_image(generated_base64_image)
