import os
from datetime import datetime
from enum import Enum, auto
from functools import wraps
from typing import Any, Dict, Optional, Tuple

from PySide6.QtCore import QObject, Signal


class StopWorker(Exception):
    """自定义异常，表示用户终止生成图片。"""
    pass


class RunState(Enum):
    RUNNING = auto()
    STOPPED = auto()


class StyledImageWorker(QObject):
    setStep = Signal(int)  # 当工作者进度更新时发射
    stopped = Signal()  # 当工作者停止时发射

    def __init__(self, temp_dir: str = None):
        super().__init__()
        self.temp_dir = temp_dir or r"temp"
        self.file_name_prefix = 'result'
        self.save_temp_path: Optional[str] = None
        self.run_state: RunState = RunState.RUNNING

    def stop(self):
        self.run_state = RunState.STOPPED

    def script(self, file_path2: str, file_path3: str, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        try:
            self.run(file_path2, file_path3, args, kwargs)
        except StopWorker:
            self.stopped.emit()

    def run(self, file_path2: str, file_path3: str, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def step(i: int):
        def decorator(func):
            @wraps(func)
            def wrapper(self: "StyledImageWorker", *args, **kwargs):
                if self.run_state == RunState.STOPPED:
                    raise StopWorker
                result = func(self, *args, **kwargs)
                self.setStep.emit(i)
                return result

            return wrapper

        return decorator

    def get_file_path(self):
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_temp_path = os.path.join(self.temp_dir, f"{self.file_name_prefix}_{timestamp}.jpg")
        return self.save_temp_path

    def get_save_temp_path(self) -> str:
        return self.save_temp_path
