from qfluentwidgets import MSFluentWindow as MSFluentFramelessWindow

from src.utils.config import cfg
from .frame_window import MSFluentFrameWindow

if cfg.frame_less_window.value:
    # Frameless window
    Window = MSFluentFramelessWindow
else:
    # Frame window
    Window = MSFluentFrameWindow
