from qfluentwidgets import (ComboBoxSettingCard, ExpandLayout, FluentIcon, MessageBox, OptionsSettingCard,
                            RangeSettingCard, SettingCardGroup, SwitchSettingCard)

from src.utils.config import SamplerName, TiledDiffusionMethod, UpscalerName, VTKInteractorStyle, VTKProjection, cfg
from .base_page import BasePage
from ..components import CustomColorSettingCard, DoubleRangeSettingCard, InputSettingCard, SpinBoxSettingCard
from ..ui.ui_SettingPage import Ui_SettingPage


class SettingPage(BasePage, Ui_SettingPage):
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
            parent=self.personal_group,
            color_dialog_parent=self.window(),
            enableAlpha=True
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
        self.languageCard = ComboBoxSettingCard(
            configItem=cfg.language,
            icon=FluentIcon.LANGUAGE,
            title=self.tr('Language'),
            content=self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personal_group
        )
        self.frame_less_window_card = SwitchSettingCard(
            configItem=cfg.frame_less_window,
            icon=FluentIcon.BACK_TO_WINDOW,
            title=self.tr("Frame less window"),
            content=self.tr("Experimental feature, prone to compatibility issues."),
            parent=self.personal_group
        )
        self.pm_enable_card = SwitchSettingCard(
            configItem=cfg.pm_enable,
            icon=FluentIcon.PASTE,
            title=self.tr("Path memory"),
            content=self.tr("Enable the path memory function to quickly open the last used path next time."),
            parent=self.personal_group
        )
        # endregion

        # region vtk components
        self.vtk_components_group = SettingCardGroup(
            self.tr('VTK components'), self.widget)
        self.vc_interactor_style_card = ComboBoxSettingCard(
            configItem=cfg.vc_interactor_style,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Interactor style"),
            texts=[self.tr(member.value) for member in VTKInteractorStyle],
            parent=self.vtk_components_group
        )
        self.vc_projection_card = ComboBoxSettingCard(
            configItem=cfg.vc_projection,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Projection method"),
            texts=[self.tr(member.value) for member in VTKProjection],
            parent=self.vtk_components_group
        )
        # endregion

        # region color point cloud
        self.color_point_cloud_group = SettingCardGroup(
            self.tr('Color point cloud'), self.widget)
        self.sampling_density_card = SpinBoxSettingCard(
            configItem=cfg.sampling_density,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Sampling density"),
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
            'Stable diffusion', self.widget)
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
            content=self.tr("Recommended 0.1~0.3"),
            parent=self.personal_group
        )
        self.sd_step_card = SpinBoxSettingCard(
            configItem=cfg.sd_steps,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Steps"),
            content=self.tr("Number of steps for generating the image"),
            parent=self.personal_group
        )
        # endregion

        # region tiled diffusion
        self.tiled_diffusion_group = SettingCardGroup(
            'Tiled diffusion', self.widget)
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
            content=self.tr("Overwrite input image size"),
            parent=self.tiled_diffusion_group
        )
        self.td_keep_input_size_card = SwitchSettingCard(
            configItem=cfg.td_keep_input_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Keep input size"),
            content=self.tr("Keep the original size of the input image"),
            parent=self.tiled_diffusion_group
        )
        self.td_image_width_card = SpinBoxSettingCard(
            configItem=cfg.td_image_width,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Image width"),
            parent=self.tiled_diffusion_group
        )
        self.td_image_height_card = SpinBoxSettingCard(
            configItem=cfg.td_image_height,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Image height"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_width_card = RangeSettingCard(
            configItem=cfg.td_tile_width,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile width"),
            content=self.tr("Latent space tile width (width of tiles during processing)"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_height_card = RangeSettingCard(
            configItem=cfg.td_tile_height,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile height"),
            content=self.tr("Latent space tile height (height of tiles during processing)"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_overlap_card = RangeSettingCard(
            configItem=cfg.td_tile_overlap,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile overlap"),
            content=self.tr("Latent space tile overlap (overlapping pixels between tiles)"),
            parent=self.tiled_diffusion_group
        )
        self.td_tile_batch_size_card = RangeSettingCard(
            configItem=cfg.td_tile_batch_size,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Tile batch size"),
            content=self.tr("Latent space tile batch size (number of tiles processed at once)"),
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
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_steps_card = RangeSettingCard(
            configItem=cfg.td_noise_inverse_steps,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise reverse steps"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_retouch_card = DoubleRangeSettingCard(
            configItem=cfg.td_noise_inverse_retouch,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse retouch"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_renoise_strength_card = DoubleRangeSettingCard(
            configItem=cfg.td_noise_inverse_renoise_strength,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse renoise strength"),
            parent=self.tiled_diffusion_group
        )
        self.td_noise_inverse_renoise_kernel_card = RangeSettingCard(
            configItem=cfg.td_noise_inverse_renoise_kernel,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Noise inverse renoise kernel"),
            parent=self.tiled_diffusion_group
        )
        self.td_td_control_tensor_cpu_card = SwitchSettingCard(
            configItem=cfg.td_control_tensor_cpu,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Control tensor CPU"),
            content=self.tr("Move ControlNet tensor to CPU (if applicable)"),
            parent=self.tiled_diffusion_group
        )
        self.td_enable_bbox_control_card = SwitchSettingCard(
            configItem=cfg.td_enable_bbox_control,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Enable bbox control"),
            parent=self.tiled_diffusion_group
        )
        self.td_draw_background_card = SwitchSettingCard(
            configItem=cfg.td_draw_background,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Draw background"),
            parent=self.tiled_diffusion_group
        )
        self.td_causal_layers_card = SwitchSettingCard(
            configItem=cfg.td_causal_layers,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Causal layers"),
            parent=self.tiled_diffusion_group
        )
        # endregion

        # region tiled vae
        self.tiled_vae_group = SettingCardGroup(
            'Tiled VAE', self.widget)
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
            content=self.tr("Move VAE to GPU (if allowed)"),
            parent=self.tiled_vae_group
        )
        self.tv_fast_decoder_card = SwitchSettingCard(
            configItem=cfg.tv_fast_decoder,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Fast decoder"),
            parent=self.tiled_vae_group
        )
        self.tv_fast_encoder_card = SwitchSettingCard(
            configItem=cfg.tv_fast_encoder,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Fast encoder"),
            parent=self.tiled_vae_group
        )
        self.tv_color_fix_card = SwitchSettingCard(
            configItem=cfg.tv_color_fix,
            icon=FluentIcon.ALIGNMENT,
            title=self.tr("Color fix"),
            parent=self.tiled_vae_group
        )
        # endregion

        self._init_layout()
        self._set_visible()
        self._init_set_single_step()
        self._connect_signals()

    def _init_layout(self):
        for card in [self.theme_card, self.theme_color_card, self.zoom_card, self.languageCard,
                     self.frame_less_window_card, self.pm_enable_card]:
            self.personal_group.addSettingCard(card)

        for card in [self.vc_interactor_style_card, self.vc_projection_card]:
            self.vtk_components_group.addSettingCard(card)

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

        for group in [self.personal_group, self.vtk_components_group, self.color_point_cloud_group,
                      self.stable_diffusion_group, self.tiled_diffusion_group, self.tiled_vae_group]:
            self.expand_layout.addWidget(group)

    def _set_visible(self):
        self.set_sd_card_visible(cfg.get(cfg.sd_enable))

    def _init_set_single_step(self):
        self.td_tile_width_card.slider.setSingleStep(16)
        self.td_tile_height_card.slider.setSingleStep(16)
        self.td_tile_overlap_card.slider.setSingleStep(4)

        self.tv_decoder_tile_size_card.slider.setSingleStep(16)

    def _connect_signals(self):
        cfg.themeMode.valueChanged.connect(self.show_dialog)
        cfg.themeColor.valueChanged.connect(self.show_dialog)
        cfg.dpiScale.valueChanged.connect(self.show_dialog)
        cfg.language.valueChanged.connect(self.show_dialog)
        cfg.frame_less_window.valueChanged.connect(self.show_dialog)
        cfg.pm_enable.valueChanged.connect(self.path_memory_enable_changed)
        cfg.sd_enable.valueChanged.connect(self.set_sd_card_visible)

    def show_dialog(self):
        m = MessageBox(self.tr("Update successful"),
                       self.tr("The configuration takes effect after restarting the software"),
                       self.window())
        m.yesButton.setText(self.tr("Restart now"))
        m.cancelButton.setText(self.tr("Restart later"))
        m.setClosableOnMaskClicked(True)
        m.yesSignal.connect(self.restart_now)
        m.show()

    @staticmethod
    def path_memory_enable_changed(value: bool):
        if not value:
            cfg.set(cfg.pm_image_import, "")
            cfg.set(cfg.pm_image_export, "")
            cfg.set(cfg.pm_resource_import, "")
            cfg.set(cfg.pm_resource_export, "")

    def set_sd_card_visible(self, value: bool):
        if value:
            self.stable_diffusion_group.setVisible(True)
            self.tiled_diffusion_group.setVisible(True)
            self.tiled_vae_group.setVisible(True)
        else:
            self.stable_diffusion_group.setVisible(False)
            self.tiled_diffusion_group.setVisible(False)
            self.tiled_vae_group.setVisible(False)
