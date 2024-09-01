from src.utils.config import cfg
from .frame_window import MSFluentFrameWindow
from .frameless_window import MSFluentFramelessWindow

if cfg.frame_less_window.value:
    # Frameless window
    Window = MSFluentFramelessWindow
else:
    # Frame window
    Window = MSFluentFrameWindow
