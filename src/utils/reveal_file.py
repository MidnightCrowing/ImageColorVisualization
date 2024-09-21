import os
import subprocess


def reveal_file(file_path: str):
    # 打开目录并选中该文件
    subprocess.run(['explorer', '/select,', os.path.abspath(file_path)])
