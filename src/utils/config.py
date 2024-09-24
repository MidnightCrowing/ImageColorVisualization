from enum import Enum
from typing import Optional

from PySide6.QtCore import QLocale
from qfluentwidgets import (OptionsConfigItem,
                            OptionsValidator,
                            QConfig,
                            ConfigSerializer,
                            ConfigItem,
                            RangeValidator,
                            BoolValidator,
                            RangeConfigItem,
                            qconfig,
                            ColorConfigItem,
                            Theme,
                            EnumSerializer)


class DoubleRangeConfigItem(RangeConfigItem):
    """Configuration item for range values with scaling applied."""

    def __init__(
            self,
            group: str,
            name: str,
            default: float,
            validator: Optional[RangeValidator] = None,
            scale: int = 2,
            serializer=None,
            restart: bool = False
    ):
        """
        Initialize ScaledRangeConfigItem with scaling factor.

        Parameters
        ----------
        group : str
            The configuration group name.
        name : str
            The configuration item name.
        default : float
            The default value of the configuration item.
        validator : RangeValidator, optional
            A validator that checks if values are within the specified range.
        scale : int, optional
            Number of decimal places to scale the value by, default is 2.
        serializer : optional
            Serializer used for saving and loading values.
        restart : bool, optional
            Whether a restart is required when the value changes.
        """
        self.scale = scale
        self.scaling_multiplier = 10 ** scale

        # Adjust the validator range according to the scaling multiplier
        if validator is not None:
            validator = RangeValidator(
                validator.min * self.scaling_multiplier,
                validator.max * self.scaling_multiplier
            )
        # Adjust the default value according to the scaling multiplier and initialize the base class
        super().__init__(group, name, default * self.scaling_multiplier, validator, serializer, restart)

    def __str__(self):
        return f'{self.__class__.__name__}[range={self.range}, value={self.value}, scale={self.scale}]'

    @property
    def doubleValue(self):
        return self.value / self.scaling_multiplier


# 语言
class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


# stable diffusion 采样器名称
class SamplerName(Enum):
    DPM_2M = "DPM++ 2M"
    DPM_SDE = "DPM++ SDE"
    DPM_2M_SDE = "DPM++ 2M SDE"
    DPM_2M_SDE_HEUN = "DPM++ 2M SDE Heun"
    DPM_2S_A = "DPM++ 2S a"
    DPM_3M_SDE = "DPM++ 3M SDE"
    EULER_A = "Euler a"
    EULER = "Euler"
    LMS = "LMS"
    HEUN = "Heun"
    DPM2 = "DPM2"
    DPM2_A = "DPM2 a"
    DPM_FAST = "DPM fast"
    DPM_ADAPTIVE = "DPM adaptive"
    RESTART = "Restart"
    DDIM = "DDIM"
    DDIM_CFG_PLUS_PLUS = "DDIM CFG++"
    PLMS = "PLMS"
    UNIPC = "UniPC"
    LCM = "LCM"


# tiled diffusion 方案
class TiledDiffusionMethod(Enum):
    MULTI_DIFFUSION = "MultiDiffusion"
    MIXTURE_OF_DIFFUSIONS = "Mixture of Diffusions"


# tiled diffusion 放大算法
class UpscalerName(Enum):
    NONE = "None"
    LANCZOS = "Lanczos"
    NEAREST = "Nearest"
    _4X_ANIME_SHARP = "4x AnimeSharp"
    BSRGAN = "BSRGAN"
    DAT_X2 = "DAT x2"
    DAT_X3 = "DAT x3"
    DAT_X4 = "DAT x4"
    ESRGAN_4X = "ESRGAN 4x"
    LDSR = "LDSR"
    R_ESRGAN_4X = "R-ESRGAN 4x+"
    R_ESRGAN_4X_ANIME6B = "R-ESRGAN 4x+ Anime6B"
    SCUNET = "ScuNet"
    SCUNET_PSNR = "ScuNet PSNR"
    SWINIR_4X = "SwinIR_4x"


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class SamplerNameSerializer(ConfigSerializer):
    def serialize(self, sampler_name: SamplerName) -> str:
        """ 将 SamplerName 枚举成员序列化为字符串 """
        return sampler_name.value

    def deserialize(self, value: str) -> SamplerName:
        """ 将字符串反序列化为 SamplerName 枚举成员 """
        # 尝试找到与字符串值匹配的 SamplerName 枚举成员
        for member in SamplerName:
            if member.value == value:
                return member
        # 如果没有匹配的，抛出异常或返回一个默认值
        raise ValueError(f"Unknown sampler name: {value}")


class TiledDiffusionMethodSerializer(ConfigSerializer):
    def serialize(self, method: TiledDiffusionMethod) -> str:
        """ 将 TiledDiffusionMethod 枚举成员序列化为字符串 """
        return method.value

    def deserialize(self, value: str) -> TiledDiffusionMethod:
        """ 将字符串反序列化为 TiledDiffusionMethod 枚举成员 """
        # 尝试找到与字符串值匹配的 SamplerName 枚举成员
        for member in TiledDiffusionMethod:
            if member.value == value:
                return member
        # 如果没有匹配的，抛出异常或返回一个默认值
        raise ValueError(f"Unknown method name: {value}")


class UpscalerNameSerializer(ConfigSerializer):
    def serialize(self, upscaler_name: UpscalerName) -> str:
        """ 将 UpscalerName 枚举成员序列化为字符串 """
        return upscaler_name.value

    def deserialize(self, value: str) -> UpscalerName:
        """ 将字符串反序列化为 UpscalerName 枚举成员 """
        # 尝试找到与字符串值匹配的 UpscalerName 枚举成员
        for member in UpscalerName:
            if member.value == value:
                return member
        # 如果没有匹配的，抛出异常或返回一个默认值
        raise ValueError(f"Unknown upscaler name: {value}")


class Config(QConfig):
    # region personalization
    themeMode = OptionsConfigItem(
        group="QFluentWidgets", name="ThemeMode", default=Theme.AUTO,
        validator=OptionsValidator(Theme), serializer=EnumSerializer(Theme))
    themeColor = ColorConfigItem(
        group="QFluentWidgets", name="ThemeColor", default='#ff6a81ff')
    dpiScale = OptionsConfigItem(
        group="MainWindow", name="DpiScale", default="Auto",
        validator=OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        group="MainWindow", name="Language", default=Language.AUTO,
        validator=OptionsValidator(Language), serializer=LanguageSerializer(), restart=True)
    frame_less_window = OptionsConfigItem(
        group="MainWindow", name="FrameLessWindow", default=False,
        validator=BoolValidator(), restart=True)
    # endregion

    # region color point cloud
    sampling_density = ConfigItem(
        group="ColorPointCloud", name="SamplingDensity", default=100000)
    sd_enable = OptionsConfigItem(
        group="ColorPointCloud", name="Enable", default=False,
        validator=BoolValidator())
    # endregion

    # region stable diffusion
    sd_ip = ConfigItem(
        group="StableDiffusion", name="IP", default="localhost")
    sd_port = ConfigItem(
        group="StableDiffusion", name="Port", default="7860")
    sd_sampler_name = OptionsConfigItem(
        group="StableDiffusion", name="SamplerName", default=SamplerName.DPM_2M,
        validator=OptionsValidator(SamplerName), serializer=SamplerNameSerializer())
    sd_denoising_strength = DoubleRangeConfigItem(
        group="StableDiffusion", name="DenoisingStrength", default=0.1,
        validator=RangeValidator(0, 1))
    sd_steps = ConfigItem(
        group="StableDiffusion", name="Steps", default=20)
    # endregion

    # region tiled diffusion
    td_method = OptionsConfigItem(
        group="TiledDiffusion", name="Method", default=TiledDiffusionMethod.MULTI_DIFFUSION,
        validator=OptionsValidator(TiledDiffusionMethod), serializer=TiledDiffusionMethodSerializer())
    td_overwrite_size = ConfigItem(
        group="TiledDiffusion", name="OverwriteSize", default=False,
        validator=BoolValidator())
    td_keep_input_size = ConfigItem(
        group="TiledDiffusion", name="KeepInputSize", default=True,
        validator=BoolValidator())
    td_image_width = ConfigItem(
        group="TiledDiffusion", name="ImageWidth", default=1024)
    td_image_height = ConfigItem(
        group="TiledDiffusion", name="ImageHeight", default=1024)
    td_tile_width = RangeConfigItem(
        group="TiledDiffusion", name="TileWidth", default=96,
        validator=RangeValidator(16, 256))
    td_tile_height = RangeConfigItem(
        group="TiledDiffusion", name="TileHeight", default=96,
        validator=RangeValidator(16, 256))
    td_tile_overlap = RangeConfigItem(
        group="TiledDiffusion", name="TileOverlap", default=48,
        validator=RangeValidator(0, 256))
    td_tile_batch_size = RangeConfigItem(
        group="TiledDiffusion", name="TileBatchSize", default=4,
        validator=RangeValidator(1, 8))
    td_upscaler_name = OptionsConfigItem(
        group="TiledDiffusion", name="UpscalerName", default=UpscalerName.NONE,
        validator=OptionsValidator(UpscalerName), serializer=UpscalerNameSerializer())
    td_noise_inverse = ConfigItem(
        group="TiledDiffusion", name="NoiseInverse", default=False,
        validator=BoolValidator())
    td_noise_inverse_steps = RangeConfigItem(
        group="TiledDiffusion", name="NoiseInverseSteps", default=10,
        validator=RangeValidator(1, 200))
    td_noise_inverse_retouch = DoubleRangeConfigItem(
        group="TiledDiffusion", name="NoiseInverseRetouch", default=1,
        validator=RangeValidator(1, 100), scale=1)
    td_noise_inverse_renoise_strength = DoubleRangeConfigItem(
        group="TiledDiffusion", name="NoiseInverseRenoiseStrength", default=1,
        validator=RangeValidator(0, 2))
    td_noise_inverse_renoise_kernel = RangeConfigItem(
        group="TiledDiffusion", name="NoiseInverseRenoiseKernel", default=64,
        validator=RangeValidator(2, 512))
    td_control_tensor_cpu = ConfigItem(
        group="TiledDiffusion", name="ControlTensorCPU", default=False,
        validator=BoolValidator())
    td_enable_bbox_control = ConfigItem(
        group="TiledDiffusion", name="EnableBboxControl", default=False,
        validator=BoolValidator())
    td_draw_background = ConfigItem(
        group="TiledDiffusion", name="DrawBackground", default=False,
        validator=BoolValidator())
    td_causal_layers = ConfigItem(
        group="TiledDiffusion", name="CausalLayers", default=False,
        validator=BoolValidator())
    # endregion

    # region tiled vae
    tv_encoder_tile_size = RangeConfigItem(
        group="TiledVAE", name="EncoderTileSize", default=512,
        validator=RangeValidator(256, 4096))
    tv_decoder_tile_size = RangeConfigItem(
        group="TiledVAE", name="DecoderTileSize", default=64,
        validator=RangeValidator(48, 512))
    tv_vae_to_gpu = ConfigItem(
        group="TiledVAE", name="VAEToGPU", default=True,
        validator=BoolValidator())
    tv_fast_decoder = ConfigItem(
        group="TiledVAE", name="FastDecoder", default=True,
        validator=BoolValidator())
    tv_fast_encoder = ConfigItem(
        group="TiledVAE", name="FastEncoder", default=True,
        validator=BoolValidator())
    tv_color_fix = ConfigItem(
        group="TiledVAE", name="ColorFix", default=False,
        validator=BoolValidator())
    # endregion


NAME = 'ImageColorVisualization'
VERSION = '1.0.1'
AUTHOR = 'MidnightCrowing'
APP_URL = 'https://github.com/MidnightCrowing/ImageColorVisualization'
SUPPORT_URL = 'https://github.com/MidnightCrowing/ImageColorVisualization/issues'

cfg = Config()
qconfig.load(r"data/config.json", cfg)
