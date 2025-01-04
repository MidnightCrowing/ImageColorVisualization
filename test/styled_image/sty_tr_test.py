from src.styled_image import StyTr

matcher = StyTr(
    temp_dir=r"result",
    vgg_model=r'..\..\models\vgg_normalised.pth',
    decoder_model=r'..\..\models\decoder_iter_160000.pth',
    trans_model=r'..\..\models\transformer_iter_160000.pth',
    embedding_model=r'..\..\models\embedding_iter_160000.pth'
)
matcher.script(r"..\images\content.png", r"..\images\style.png")
