from __future__ import annotations

from typing import Optional, Dict

import numpy as np
from PIL import Image
from qfluentwidgets import Theme
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.utils.config import cfg
from src.utils.sd_pipeline import generate_image
from .color_point_cloud import ColorPointCloud, PointCloudActor, MaskPointColor, ColorList, calculate_point_coordinates
from .type import Point3D
from .vtk_scene import VTKScene


class VTKManager:
    def __init__(self, vtk_widget: QVTKRenderWindowInteractor):
        """
        初始化 VTKManager。

        :param vtk_widget: VTK 渲染窗口小部件。
        """
        self.ball_round = 10
        self.cloud_actors: Dict[PointCloudActor, Optional[Image]] = {}

        # 初始化 VTK 场景和颜色点云对象
        self.vtk_scene = VTKScene(vtk_widget, self.ball_round)
        self.color_point_cloud = self._init_color_point_cloud()

        # 设置主题和连接信号槽
        self.set_theme(cfg.themeMode.value)
        self._connect_signals()

    def _init_color_point_cloud(self) -> ColorPointCloud:
        """初始化颜色点云对象。"""
        sampling_density = cfg.sampling_density.value
        return ColorPointCloud(self.vtk_scene.renderer, self.ball_round, sampling_density)

    def _connect_signals(self):
        """连接信号和槽，处理配置变更。"""
        cfg.sampling_density.valueChanged.connect(self.update_sampling_density)
        cfg.sd_enable.valueChanged.connect(self.update_sd_enable)
        cfg.themeChanged.connect(self.set_theme)

    def set_image(self, image_path: str, mask_cloud_actor: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        设置图像，并根据配置处理图像和更新点云。
        一般用于在一个 VTK 窗口中只显示一个图像时使用。

        :param image_path: 图像文件路径。
        :param mask_cloud_actor: 点云颜色（可选）。
        """
        new_image = Image.open(image_path)
        processed_image = self._process_image(new_image)

        if self.cloud_actors:
            # 如果已有点云，则移除现有点云
            self.color_point_cloud.remove_all_point_cloud()

        # 添加新的点云
        cloud_actor = self.color_point_cloud.add_point_cloud(processed_image, mask_cloud_actor=mask_cloud_actor)
        self.cloud_actors[cloud_actor] = new_image

        return cloud_actor

    def add_image(self, image_path: str, mask_cloud_actor: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        添加图像，并根据配置处理图像和更新点云。

        :param image_path: 图像文件路径。
        :param mask_cloud_actor: 点云颜色（可选）。
        """
        new_image = Image.open(image_path)
        processed_image = self._process_image(new_image)

        # 添加新的点云
        cloud_actor = self.color_point_cloud.add_point_cloud(processed_image, mask_cloud_actor=mask_cloud_actor)
        self.cloud_actors[cloud_actor] = new_image

        return cloud_actor

    def set_clouds(self, color_list: ColorList,
                   mask_cloud_actor: Optional[MaskPointColor] = None):
        """
        设置自定义点云，并根据配置更新点云。
        一般用于在一个 VTK 窗口中只显示一个图像时使用。

        :param color_list: 点的颜色列表。
        :param mask_cloud_actor: 点云颜色（可选）。
        """

        if self.cloud_actors:
            # 如果已有点云，则移除现有点云
            self.color_point_cloud.remove_all_point_cloud()

        # 添加新的点云
        cloud_actor = self.color_point_cloud.add_point_cloud(color_list=color_list, mask_cloud_actor=mask_cloud_actor)
        self.cloud_actors[cloud_actor] = None

    def add_clouds(self, color_list: ColorList,
                   mask_cloud_actor: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        添加自定义点云，并根据配置更新点云。

        :param color_list: 点的颜色列表。
        :param mask_cloud_actor: 点云颜色（可选）。
        """
        # 添加新的点云
        cloud_actor = self.color_point_cloud.add_point_cloud(color_list=color_list, mask_cloud_actor=mask_cloud_actor)
        self.cloud_actors[cloud_actor] = None

        return cloud_actor

    def add_null_cloud_actor(self, mask_cloud_actor: Optional[MaskPointColor] = None) -> PointCloudActor:
        """
        添加空点云对象，可用于实现更底层功能。
        """
        cloud_actor = self.color_point_cloud.add_point_cloud(mask_cloud_actor=mask_cloud_actor)
        self.cloud_actors[cloud_actor] = None

        return cloud_actor

    def set_theme(self, value: Optional[Theme] = None):
        """
        设置主题，根据主题设置背景颜色。

        :param value: 主题值（可选）。
        """
        if value is None:
            value = cfg.themeMode.value
        self.vtk_scene.set_theme(value)

    def remove_mask_cloud_actor(self):
        """移除点云颜色数据。"""
        self.color_point_cloud.remove_all_point_cloud()

    @staticmethod
    def _process_image(image: Image) -> Image:
        """
        处理图像，根据采样密度调整图像大小或直接返回图像。

        :param image: 原始图像。
        :return: 处理后的图像。
        """
        if cfg.sd_enable.value:
            sampling_density = cfg.sampling_density.value
            width, height = image.size
            if width * height < sampling_density:
                scale_factor = np.sqrt(sampling_density / (width * height))
                print(f'缩放图像: {scale_factor}')
                return generate_image(image, scale_factor)
        return image

    def update_sampling_density(self, value: int):
        """
        更新采样密度，必要时调整图像并更新点云。

        :param value: 新的采样密度。
        """
        print(f'更新采样密度: {value}')
        if not self.cloud_actors:
            return

        if not cfg.sd_enable.value:
            self.color_point_cloud.set_sample_count(value)
        else:
            self.color_point_cloud.set_sample_count(value)
            self._update_image_and_point_cloud(value)

    @staticmethod
    def update_sd_enable(value: bool):
        """
        更新稳定扩散开关，必要时调整图像并更新点云。

        :param value: 稳定扩散开关状态。
        """
        print(f'更新稳定扩散开关: {value}')

    def _update_image_and_point_cloud(self, sampling_density: int):
        """
        根据采样密度更新图像和点云。

        :param sampling_density: 采样密度。
        """
        for cloud_actor, image in self.cloud_actors.items():
            if image is None:
                continue

            width, height = image.size
            if width * height < sampling_density:
                scale_factor = np.sqrt(sampling_density / (width * height))
                print(f'缩放图像: {scale_factor}')
                scaled_image = generate_image(image, scale_factor)
                cloud_actor.set_image(scaled_image)

    def calculate_point_coordinates(self, color: MaskPointColor) -> Point3D:
        """
        计算点的坐标。

        :param color: 点的颜色。
        :return: 点的坐标。
        """
        return calculate_point_coordinates(color, self.ball_round)

    def sync_scene(self, vtk_manager: VTKManager):
        """
        用于同步两个 VTK 窗口的场景，将传入的 VTK 管理器同步到自己场景中。

        :param vtk_manager: 另一个 VTK 管理器。
        """
        self.vtk_scene.sync_scene(vtk_manager.vtk_scene.renderer, vtk_manager.vtk_scene.interactor)

    def render(self):
        """更新渲染 VTK 场景。"""
        self.vtk_scene.render()

    def close(self):
        """关闭 VTK 渲染窗口。"""
        self.vtk_scene.renderWindow.Finalize()
