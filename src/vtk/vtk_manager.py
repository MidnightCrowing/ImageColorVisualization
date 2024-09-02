from typing import Optional

import numpy as np
from PIL import Image
from qfluentwidgets import qconfig, Theme
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.image_enlarge.sd_pipeline import generate_image
from src.utils.config import cfg
from .color_point_cloud import ColorPointCloud
from .vtk_scene import VTKScene


class VTKManager:
    def __init__(self, vtk_widget: QVTKRenderWindowInteractor):
        self.ball_round = 10
        self.image: Optional[Image] = None

        # 初始化 VTK 场景
        self.vtk_scene = VTKScene(vtk_widget, self.ball_round)
        self.color_point_cloud = self._init_color_point_cloud()

        # 设置主题
        self.set_theme(cfg.themeMode.value)

        # 连接信号和槽
        self._connect_signals()

    def _init_color_point_cloud(self) -> ColorPointCloud:
        """初始化颜色点云对象。"""
        sampling_density = cfg.sampling_density.value
        return ColorPointCloud(self.vtk_scene.renderer, self.ball_round, sampling_density)

    def _connect_signals(self):
        """连接信号和槽，处理配置变更。"""
        cfg.sampling_density.valueChanged.connect(self.update_sampling_density)
        cfg.sd_enable.valueChanged.connect(self.update_sd_enable)
        qconfig.themeChanged.connect(self.set_theme)

    def set_image(self, image_path: str):
        """设置图像，并根据配置处理图像和更新点云。"""
        image = Image.open(image_path)
        self.image = image
        processed_image = self._process_image(image)
        self.color_point_cloud.set_image(processed_image)

    def set_theme(self, value: Theme = None):
        """设置主题，根据主题设置背景颜色。"""
        if value is None:
            value = cfg.themeMode.value
        self.vtk_scene.set_theme(value)

    @staticmethod
    def _process_image(image: Image) -> Image:
        """处理图像，根据采样密度缩放或直接返回图像。"""
        if cfg.sd_enable.value:
            sampling_density = cfg.sampling_density.value
            width, height = image.size

            if width * height < sampling_density:
                scale_factor = np.sqrt(sampling_density / (width * height))
                print(f'缩放图像: {scale_factor}')
                return generate_image(image, scale_factor)

        return image

    def update_sampling_density(self, value: int):
        """更新采样密度，必要时调整图像并更新点云。"""
        print(f'更新采样密度: {value}')
        if not self.image:
            return

        if not cfg.sd_enable.value:
            self.color_point_cloud.set_sample_count(value)
        else:
            self.color_point_cloud.set_sample_count(value, update=False)
            self._update_image_and_point_cloud(value)

    @staticmethod
    def update_sd_enable(value: bool):
        """更新稳定扩散开关，必要时调整图像并更新点云。"""
        print(f'更新稳定扩散开关: {value}')

    def _update_image_and_point_cloud(self, sampling_density: int):
        """根据采样密度更新图像和点云。"""
        if not self.image:
            return

        width, height = self.image.size
        if width * height < sampling_density:
            scale_factor = np.sqrt(sampling_density / (width * height))
            print(f'缩放图像: {scale_factor}')
            scaled_image = generate_image(self.image, scale_factor)
            self.color_point_cloud.set_image(scaled_image, update=False)

        self.color_point_cloud.update_point_cloud()

    def close(self):
        self.vtk_scene.renderWindow.Finalize()
