from PySide6.QtWidgets import QWidget
from qfluentwidgets import (CustomColorSettingCard,
                            ExpandLayout,
                            FluentIcon,
                            OptionsSettingCard,
                            SettingCardGroup,
                            ComboBoxSettingCard,
                            SwitchSettingCard,
                            RangeSettingCard)

from src.utils.config import cfg, SamplerName, TiledDiffusionMethod, UpscalerName
from ..components.double_range_setting_card import DoubleRangeSettingCard
from ..components.input_setting_card import InputSettingCard
from ..components.spin_setting_card import SpinBoxSettingCard
from ..ui.ui_SettingPage import Ui_SettingPage


class SettingPage(QWidget, Ui_SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.expand_layout = ExpandLayout(self.widget)

        # region personalization
        self.personal_group = SettingCardGroup(
            self.tr('Personalization'), self.widget)
        self.theme_card = OptionsSettingCard(
            configItem=cfg.themeMode,
            icon=FluentIcon.BRUSH,
            title=self.tr('Application theme'),
            content=self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personal_group
        )
        self.theme_color_card = CustomColorSettingCard(
            configItem=cfg.themeColor,
            icon=FluentIcon.PALETTE,
            title=self.tr('Theme color'),
            content=self.tr('Change the theme color of you application'),
            parent=self.personal_group
        )
        self.zoom_card = OptionsSettingCard(
            configItem=cfg.dpiScale,
            icon=FluentIcon.ZOOM,
            title=self.tr("Interface zoom"),
            content=self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personal_group
        )
        # self.languageCard = ComboBoxSettingCard(
        #     cfg.language,
        #     FluentIcon.LANGUAGE,
        #     self.tr('Language'),
        #     self.tr('Set your preferred language for UI'),
        #     texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
        #     parent=self.personalGroup
        # )
        # endregion

        # region color point cloud
        self.color_point_cloud_group = SettingCardGroup(
            self.tr('Color point cloud'), self.widget)
        self.sampling_density_card = SpinBoxSettingCard(
            configItem=cfg.sampling_density,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Sampling density"),
            content=self.tr("采样密度"),
            parent=self.color_point_cloud_group
        )
        self.sd_enable_card = SwitchSettingCard(
            configItem=cfg.sd_enable,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Stable diffusion enable"),
            parent=self.color_point_cloud_group
        )
        # endregion

        # region stable diffusion
        self.stable_diffusion_group = SettingCardGroup(
            self.tr('Stable diffusion'), self.widget)
        self.sd_ip_card = InputSettingCard(
            configItem=cfg.sd_ip,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Stable diffusion IP"),
            parent=self.personal_group
        )
        self.sd_port_card = InputSettingCard(
            configItem=cfg.sd_port,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Stable diffusion Port"),
            parent=self.personal_group
        )
        self.sd_sampler_name_card = ComboBoxSettingCard(
            configItem=cfg.sd_sampler_name,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Sampler name"),
            texts=[member.value for member in SamplerName],
            parent=self.personal_group
        )
        self.sd_denoising_strength_card = DoubleRangeSettingCard(
            configItem=cfg.sd_denoising_strength,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Denoising strength"),
            content=self.tr("(描述性文字)建议0.1~0.3之间"),
            parent=self.personal_group
        )
        self.sd_step_card = SpinBoxSettingCard(
            configItem=cfg.sd_steps,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Steps"),
            content=self.tr("生成图像的步数"),
            parent=self.personal_group
        )
        # endregion

        # region tiled diffusion
        self.tiled_diffusion_group = SettingCardGroup(
            self.tr('Tiled diffusion'), self.widget)
        self.td_method_card = ComboBoxSettingCard(
            configItem=cfg.td_method,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Method"),
            texts=[method.value for method in TiledDiffusionMethod],
            parent=self.tiled_diffusion_group
        )
        self.td_overwrite_size_card = SwitchSettingCard(
            configItem=cfg.td_overwrite_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Overwrite size"),
            content=self.tr("是否覆盖输入图像大小"),
            parent=self.tiled_diffusion_group
        )
        self.td_keep_input_size_card = SwitchSettingCard(
            configItem=cfg.td_keep_input_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Keep input size"),
            content=self.tr("是否保持输入图像的原始大小"),
            parent=self.tiled_diffusion_group
        )
        self.td_image_width_card = SpinBoxSettingCard(
            configItem=cfg.td_image_width,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Image width"),
            content=self.tr("图像宽度"),
            parent=self.tiled_diffusion_group
        )
        self.td_image_height_card = SpinBoxSettingCard(
            configItem=cfg.td_image_height,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Image height"),
            content=self.tr("图像高度"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_width_card = RangeSettingCard(
            configItem=cfg.td_tile_width,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile width"),
            content=self.tr("潜空间分块宽度（处理时分块的宽度）"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_height_card = RangeSettingCard(
            configItem=cfg.td_tile_height,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile height"),
            content=self.tr("潜空间分块高度（处理时分块的高度）"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_overlap_card = RangeSettingCard(
            configItem=cfg.td_tile_overlap,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile overlap"),
            content=self.tr("潜空间分块重叠（分块之间的重叠像素）"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_batch_size_card = RangeSettingCard(
            configItem=cfg.td_tile_batch_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile batch size"),
            content=self.tr("潜空间分块单批数量（单次处理的分块数量）"),
            parent=self.tiled_diffusion_group
        )
        self.td_upscaler_name_card = ComboBoxSettingCard(
            configItem=cfg.td_upscaler_name,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Upscaler name"),
            texts=[upscaler_name.value for upscaler_name in UpscalerName],
            parent=self.tiled_diffusion_group
        )
        self.td_noise_reverse_card = SwitchSettingCard(
            configItem=cfg.td_noise_inverse,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise reverse"),
            content=self.tr("是否使用噪声反转"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_steps_card = RangeSettingCard(
            configItem=cfg.td_noise_inverse_steps,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise reverse steps"),
            content=self.tr("反转步数"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_retouch_card = DoubleRangeSettingCard(
            configItem=cfg.td_noise_inverse_retouch,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse retouch"),
            content=self.tr("修复程度"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_renoise_strength_card = DoubleRangeSettingCard(
            configItem=cfg.td_noise_inverse_renoise_strength,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse renoise strength"),
            content=self.tr("重铺噪声强度"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_renoise_kernel_card = RangeSettingCard(
            configItem=cfg.td_noise_inverse_renoise_kernel,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse renoise kernel"),
            content=self.tr("重铺噪声大小"),
            parent=self.tiled_diffusion_group
        )
        self.td_td_control_tensor_cpu_card = SwitchSettingCard(
            configItem=cfg.td_control_tensor_cpu,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Control tensor CPU"),
            content=self.tr("将ControlNet张量移至CPU（如果适用，将控制张量移至CPU）"),
            parent=self.tiled_diffusion_group
        )
        self.td_enable_bbox_control_card = SwitchSettingCard(
            configItem=cfg.td_enable_bbox_control,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Enable bbox control"),
            content=self.tr("是否启用边界框控制机制"),
            parent=self.tiled_diffusion_group
        )
        self.td_draw_background_card = SwitchSettingCard(
            configItem=cfg.td_draw_background,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Draw background"),
            content=self.tr("是否绘制背景层"),
            parent=self.tiled_diffusion_group
        )
        self.td_causal_layers_card = SwitchSettingCard(
            configItem=cfg.td_causal_layers,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Causal layers"),
            content=self.tr("是否启用因果层设置"),
            parent=self.tiled_diffusion_group
        )
        # endregion

        # region tiled vae
        self.tiled_vae_group = SettingCardGroup(
            self.tr('Tiled VAE'), self.widget)
        self.tv_encoder_tile_size_card = RangeSettingCard(
            configItem=cfg.tv_encoder_tile_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Encoder tile size"),
            parent=self.tiled_vae_group
        )
        self.tv_decoder_tile_size_card = RangeSettingCard(
            configItem=cfg.tv_decoder_tile_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Decoder tile size"),
            parent=self.tiled_vae_group
        )
        self.tv_vae_to_gpu_card = SwitchSettingCard(
            configItem=cfg.tv_vae_to_gpu,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("VAE to GPU"),
            content=self.tr("将VAE移动到GPU (如果允许)"),
            parent=self.tiled_vae_group
        )
        self.tv_fast_decoder_card = SwitchSettingCard(
            configItem=cfg.tv_fast_decoder,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Fast decoder"),
            content=self.tr("使用快速解码器"),
            parent=self.tiled_vae_group
        )
        self.tv_fast_encoder_card = SwitchSettingCard(
            configItem=cfg.tv_fast_encoder,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Fast encoder"),
            content=self.tr("使用快速编码器"),
            parent=self.tiled_vae_group
        )
        self.tv_color_fix_card = SwitchSettingCard(
            configItem=cfg.tv_color_fix,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Color fix"),
            parent=self.tiled_vae_group
        )
        # endregion

        self.__init_layout()
        self.__init_set_single_step()

    def __init_layout(self):
        for card in [self.theme_card, self.theme_color_card, self.zoom_card]:
            self.personal_group.addSettingCard(card)

        for card in [self.sampling_density_card, self.sd_enable_card]:
            self.color_point_cloud_group.addSettingCard(card)

        for card in [self.sd_ip_card, self.sd_port_card, self.sd_sampler_name_card, self.sd_denoising_strength_card,
                     self.sd_step_card]:
            self.stable_diffusion_group.addSettingCard(card)

        for card in [self.td_method_card, self.td_overwrite_size_card, self.td_keep_input_size_card,
                     self.td_image_width_card, self.td_image_height_card, self.td_tile_width_card,
                     self.td_tile_height_card, self.td_tile_overlap_card, self.td_tile_batch_size_card,
                     self.td_upscaler_name_card, self.td_noise_reverse_card, self.td_noise_inverse_steps_card,
                     self.td_noise_inverse_retouch_card, self.td_noise_inverse_renoise_strength_card,
                     self.td_noise_inverse_renoise_kernel_card, self.td_td_control_tensor_cpu_card,
                     self.td_enable_bbox_control_card, self.td_draw_background_card, self.td_causal_layers_card]:
            self.tiled_diffusion_group.addSettingCard(card)

        for card in [self.tv_encoder_tile_size_card, self.tv_decoder_tile_size_card, self.tv_vae_to_gpu_card,
                     self.tv_fast_decoder_card, self.tv_fast_encoder_card, self.tv_color_fix_card]:
            self.tiled_vae_group.addSettingCard(card)

        for group in [self.personal_group, self.color_point_cloud_group, self.stable_diffusion_group,
                      self.tiled_diffusion_group, self.tiled_vae_group]:
            self.expand_layout.addWidget(group)

    def __init_set_single_step(self):
        self.td_tile_width_card.slider.setSingleStep(16)
        self.td_tile_height_card.slider.setSingleStep(16)
        self.td_tile_overlap_card.slider.setSingleStep(4)

        self.tv_decoder_tile_size_card.slider.setSingleStep(16)
