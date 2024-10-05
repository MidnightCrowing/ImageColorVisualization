# ImageColorVisualization

简体中文 | [English](docs/README_EN.md)

![Interface](https://raw.githubusercontent.com/MidnightCrowing/ImageColorVisualization/main/docs/source/Interface_CN.png)

## 简介

ImageColorVisualization 是一个用于图像颜色可视化的 Python
课设项目，帮助用户分析并展示图像中的颜色分布。无论您是设计师、摄影师，还是数据分析师，您都可以通过该工具直观地了解图像的色彩组成，优化设计或进行色彩相关的研究。

项目的灵感来源于 Adobe Color CC 和 [Bilibili 视频](https://www.bilibili.com/video/BV19T421671a)。

## 安装依赖

您可以通过以下方式安装项目所需的依赖项：

- **选择 I（建议）**: 使用 conda 创建和激活环境：
    ```bash
    conda env create -f environment.yml
    conda activate ImageColorVisualization
    ```

- **选择 II**: 使用 `requirements.txt` 文件安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

- **选择 III**: 手动安装依赖：

  如果您希望逐个安装包，可以使用以下命令：
    ```bash
    pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.org/simple/
    pip install vtk
    pip install opencv-python
    pip install requests
    pip install Pillow
    pip install scikit-learn
    ```

## 运行项目

在项目根目录下运行以下命令启动程序：

```bash
python main.py
```

## 打包项目

使用 Nuitka 进行打包。请按照以下步骤操作：

1. 安装 Nuitka：

    ```bash
    pip install nuitka
    ```

2. 打包项目：

    ```bash
    nuitka --standalone --enable-plugin=pyside6 --windows-console-mode=attach --output-dir=dist --windows-icon-from-ico=./resource/image/ImageColorVisualization.ico ./main.py
    ```

3. 制作安装包：

   本项目使用 Inno Setup 制作安装包。请确保您已提前安装 Inno Setup，并配置简体中文和繁体中文语言包。

   在项目根目录下运行以下命令：

   ```bash
   cd Inno
   python setup.py
   ```

   这将自动处理Nuitka打包结果，并在 `Inno` 目录下生成一个 `setup.iss` 文件。使用 Inno Setup 打开该文件并编译，即可生成安装包（该安装包将会生成在
   `dist` 文件夹中）。

## 反馈

如果您有任何问题或建议，请访问 [本项目的 GitHub Issues](https://github.com/MidnightCrowing/ImageColorVisualization/issues)
页面提交反馈，我会尽快回复。

## 许可证

本项目使用 [GPL-3.0 许可证](https://www.gnu.org/licenses/gpl-3.0.html)。

## 鸣谢

- [QFluentWidgets](https://qfluentwidgets.com/zh/pages/about) - 一个基于 C++ Qt/PyQt/PySide 的 Fluent Design 风格组件库。
- [VTK](https://vtk.org/)
- [IntelliJ Icon](https://intellij-icons.jetbrains.design/) 和 [iconfont](https://www.iconfont.cn/) - 提供部分图标资源。

感谢开源社区以及所有为该项目做出贡献的开发者！
