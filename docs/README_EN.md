# ImageColorVisualization

[简体中文](../README.md) | English

![Interface](https://raw.githubusercontent.com/MidnightCrowing/ImageColorVisualization/main/docs/source/Interface.png)

## Introduction

ImageColorVisualization is a Python course project designed for visualizing the color distribution in images. Whether
you're a designer, photographer, or data analyst, this tool helps you analyze and display the color composition of an
image, offering insights to optimize designs or perform color-related research.

The project was inspired by Adobe Color CC and this [Bilibili video](https://www.bilibili.com/video/BV19T421671a).

## Install Dependencies

You can install the required dependencies using the following methods:

- Install dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

- Or manually install the dependencies using these commands:

    ```bash
    pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.org/simple/
    pip install vtk
    pip install opencv-python
    pip install requests
    pip install Pillow
    ```

## Running the Project

To start the program, run the following command in the root directory of the project:

```bash
python main.py
```

## Packaging the Project

To package the project using Nuitka, follow these steps:

1. Install Nuitka:

    ```bash
    pip install nuitka
    ```

2. Package the project:

    ```bash
    nuitka --standalone --enable-plugin=pyside6 --include-data-files=data/*=data/ --windows-console-mode=disable --output-dir=dist --windows-icon-from-ico=./resource/image/ImageColorVisualization.ico ./main.py
    ```

3. Create an installation package:

   This project uses Inno Setup to create an installer. Please ensure Inno Setup is installed, and that the Simplified
   Chinese and Traditional Chinese language packs are configured.

   In the root directory of the project, run the following command:

   ```bash
   cd Inno
   python setup.py
   ```

   This will generate a `setup.iss` file in the `Inno` directory. Open this file with Inno Setup and compile it to
   create the installer (the installer will be generated in the `dist` folder).

## Feedback

If you have any issues or suggestions, please visit
the [GitHub Issues](https://github.com/MidnightCrowing/ImageColorVisualization/issues) page of the project to submit
your feedback, and I will respond as soon as possible.

## License

This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html).

## Acknowledgments

- [QFluentWidgets](https://qfluentwidgets.com/en/pages/about) - A Fluent Design-style widget library based on C++
  Qt/PyQt/PySide.
- [VTK](https://vtk.org/)
- [IntelliJ Icon](https://intellij-icons.jetbrains.design/) - Providing some of the icon resources.

Thank you to the open-source community and all the developers who contributed to this project!
