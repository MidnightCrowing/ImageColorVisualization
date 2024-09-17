# ImageColorVisualization

## 打包

```shell
nuitka --standalone --enable-plugin=pyside6 --include-data-files=data/*=data/ --windows-console-mode=disable --output-dir=dist --windows-icon-from-ico=./resource/image/ImageColorVisualization.ico ./main.py
```
