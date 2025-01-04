from collections import OrderedDict

import torch
from PIL import Image
from torchvision import transforms
from torchvision.utils import save_image

from .sty_tr_2 import sty_tr, transformer
from .styled_image_worker import StyledImageWorker


def get_device():
    """获取设备（GPU或CPU）"""
    return torch.device("cuda:2" if torch.cuda.is_available() else "cpu")


def load_model_weights(model, model_path):
    """加载模型权重"""
    state_dict = torch.load(model_path, weights_only=True)
    new_state_dict = OrderedDict((k, v) for k, v in state_dict.items())
    model.load_state_dict(new_state_dict)
    return model


class StyTr(StyledImageWorker):
    def __init__(
            self,
            temp_dir: str = None,
            img_size=512,
            vgg_model: str = 'models/vgg_normalised.pth',
            decoder_model: str = 'models/decoder_iter_160000.pth',
            trans_model: str = 'models/transformer_iter_160000.pth',
            embedding_model: str = 'models/embedding_iter_160000.pth'
    ):
        super().__init__(temp_dir=temp_dir)
        self.file_name_prefix = 'sty_tr'
        self.img_size = img_size
        self.vgg_model = vgg_model
        self.decoder_model = decoder_model
        self.trans_model = trans_model
        self.embedding_model = embedding_model

    def run(self, content_path: str, style_path: str, *args, **kwargs):
        """
        运行彩色图像直方图匹配并更新进度条
        :param content_path: 原图路径
        :param style_path: 参考图路径
        """
        device = get_device()

        # 加载模型
        network = self.load_models(self.vgg_model, self.decoder_model, self.trans_model, self.embedding_model, device)

        # 加载图像
        content_tf = self.build_transform(resize=self.img_size, crop=True)
        style_tf = self.build_transform(resize=self.img_size, crop=True)

        content = content_tf(Image.open(content_path).convert("RGB")).unsqueeze(0).to(device)
        style = style_tf(Image.open(style_path).convert("RGB")).unsqueeze(0).to(device)

        self.setStep.emit(3)

        # 风格迁移
        with torch.no_grad():
            output = network(content, style)[0].cpu()

        self.setStep.emit(4)

        # 保存结果
        save_image(output, self.get_file_path())

        self.setStep.emit(7)

    @StyledImageWorker.step(1)
    def load_models(self, vgg_model, decoder_model, trans_model, embedding_model, device):
        """加载所有模型并设置到设备"""
        vgg = sty_tr.vgg
        vgg.load_state_dict(torch.load(vgg_model, weights_only=True))
        vgg = torch.nn.Sequential(*list(vgg.children())[:44]).to(device).eval()

        decoder = load_model_weights(sty_tr.decoder, decoder_model).to(device).eval()
        trans = load_model_weights(transformer.Transformer(), trans_model).to(device).eval()
        embedding = load_model_weights(sty_tr.PatchEmbed(), embedding_model).to(device).eval()

        return sty_tr.StyTrans(vgg, decoder, embedding, trans).to(device).eval()

    @StyledImageWorker.step(2)
    def build_transform(self, resize=None, crop=None):
        """构建图像预处理转换"""
        transform_list = []

        if resize != 0:
            transform_list.append(transforms.Resize(resize))
        if crop:
            transform_list.append(transforms.CenterCrop(resize))
        transform_list.append(transforms.ToTensor())
        transform = transforms.Compose(transform_list)
        return transform
