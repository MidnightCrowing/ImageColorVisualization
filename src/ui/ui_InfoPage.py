# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InfoPage.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, ElevatedCardWidget, ImageLabel, ScrollArea,
    SimpleCardWidget, StrongBodyLabel)
import resource_rc

class Ui_InfoPage(object):
    def setupUi(self, InfoPage):
        if not InfoPage.objectName():
            InfoPage.setObjectName(u"InfoPage")
        InfoPage.resize(805, 627)
        self.verticalLayout = QVBoxLayout(InfoPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = ScrollArea(InfoPage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea{background: transparent; border: none}")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 770, 928))
        self.scrollAreaWidgetContents.setStyleSheet(u"QWidget{background: transparent}")
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(540, 0))
        self.widget.setMaximumSize(QSize(1000, 16777215))
        self.widget.setStyleSheet(u"InfoLabel[type=\"error\"] {\n"
"    background-color: #FFCCCC;  /* Redish background for errors */\n"
"}\n"
"\n"
"InfoLabel[type=\"warning\"] {\n"
"    background-color: #FFFFCC;  /* Yellowish background for warnings */\n"
"}\n"
"\n"
"InfoLabel[type=\"information\"] {\n"
"    background-color: #CCE5FF;  /* Blueish background for information */\n"
"}\n"
"\n"
"InfoLabel[type=\"success\"] {\n"
"    background-color: #CCFFCC;  /* Greenish background for success */\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 15, 20, 15)
        self.info_frame = QFrame(self.widget)
        self.info_frame.setObjectName(u"info_frame")
        self.info_frame.setStyleSheet(u"#info_frame[type=\"dark_Info\"] {\n"
"    background-color: rgb(39, 39, 39);\n"
"    border: 1px solid rgb(29, 29, 29);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"#info_frame[type=\"dark_Success\"] {\n"
"    background-color: rgb(57, 61, 27);\n"
"    border: 1px solid rgb(29, 29, 29);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"#info_frame[type=\"dark_Warning\"] {\n"
"    background-color: rgb(67, 53, 25);\n"
"    border: 1px solid rgb(29, 29, 29);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"#info_frame[type=\"dark_Error\"] {\n"
"    background-color: rgb(68, 39, 38);\n"
"    border: 1px solid rgb(29, 29, 29);\n"
"    border-radius: 6px;\n"
"}")
        self.info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.info_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.info_frame)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(20, 20, 20, 20)
        self.info_icon = ImageLabel(self.info_frame)
        self.info_icon.setObjectName(u"info_icon")

        self.horizontalLayout_5.addWidget(self.info_icon)

        self.info_text = BodyLabel(self.info_frame)
        self.info_text.setObjectName(u"info_text")
        sizePolicy.setHeightForWidth(self.info_text.sizePolicy().hasHeightForWidth())
        self.info_text.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.info_text)


        self.verticalLayout_2.addWidget(self.info_frame)

        self.frame = SimpleCardWidget(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.label = BodyLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = SimpleCardWidget(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.label_2 = BodyLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.widget_2 = QWidget(self.frame_2)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.card_vtk = ElevatedCardWidget(self.widget_2)
        self.card_vtk.setObjectName(u"card_vtk")
        self.card_vtk.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_vtk.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_vtk.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.card_vtk)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(30, 50, 30, 50)
        self.widget_5 = QWidget(self.card_vtk)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(61, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.img_label_vtk = ImageLabel(self.widget_5)
        self.img_label_vtk.setObjectName(u"img_label_vtk")
        self.img_label_vtk.setPixmap(QPixmap(u":/logo/vtk"))

        self.horizontalLayout_4.addWidget(self.img_label_vtk)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout_7.addWidget(self.widget_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)

        self.label_6 = StrongBodyLabel(self.card_vtk)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_6)


        self.gridLayout.addWidget(self.card_vtk, 0, 3, 1, 1)

        self.card_qfw = ElevatedCardWidget(self.widget_2)
        self.card_qfw.setObjectName(u"card_qfw")
        self.card_qfw.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_qfw.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_qfw.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.card_qfw)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(30, 50, 30, 50)
        self.widget_4 = QWidget(self.card_qfw)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.img_label_qfw = ImageLabel(self.widget_4)
        self.img_label_qfw.setObjectName(u"img_label_qfw")
        self.img_label_qfw.setPixmap(QPixmap(u":/logo/qfluentwidgets"))

        self.horizontalLayout_3.addWidget(self.img_label_qfw)

        self.horizontalSpacer_4 = QSpacerItem(83, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addWidget(self.widget_4)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.label_3 = StrongBodyLabel(self.card_qfw)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_3)


        self.gridLayout.addWidget(self.card_qfw, 0, 1, 1, 1)

        self.card_pyqt = ElevatedCardWidget(self.widget_2)
        self.card_pyqt.setObjectName(u"card_pyqt")
        self.card_pyqt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_pyqt.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_pyqt.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.card_pyqt)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(30, 50, 30, 50)
        self.widget_3 = QWidget(self.card_pyqt)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.img_label_pyqt = ImageLabel(self.widget_3)
        self.img_label_pyqt.setObjectName(u"img_label_pyqt")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.img_label_pyqt.sizePolicy().hasHeightForWidth())
        self.img_label_pyqt.setSizePolicy(sizePolicy1)
        self.img_label_pyqt.setPixmap(QPixmap(u":/logo/pyqt"))
        self.img_label_pyqt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.img_label_pyqt)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addWidget(self.widget_3)

        self.verticalSpacer_2 = QSpacerItem(20, 69, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.label_4 = StrongBodyLabel(self.card_pyqt)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4)


        self.gridLayout.addWidget(self.card_pyqt, 0, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_4.addWidget(self.widget_2)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(InfoPage)

        QMetaObject.connectSlotsByName(InfoPage)
    # setupUi

    def retranslateUi(self, InfoPage):
        InfoPage.setWindowTitle(QCoreApplication.translate("InfoPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("InfoPage", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">\u5173\u4e8e ImageColorVisualization</span><span style=\" font-size:12pt;\"><br/></span><span style=\" font-size:12pt; font-weight:700;\">\u7248\u672c\uff1a</span><span style=\" font-size:12pt;\">1.0.0</span></p><p><span style=\" font-size:12pt;\">ImageColorVisualization \u662f\u4e00\u4e2a\u56fe\u50cf\u989c\u8272\u53ef\u89c6\u5316\u5de5\u5177\uff0c\u5e2e\u52a9\u7528\u6237\u5206\u6790\u548c\u5c55\u793a\u56fe\u50cf\u4e2d\u7684\u989c\u8272\u5206\u5e03\u3002\u65e0\u8bba\u662f\u8bbe\u8ba1\u5e08\u3001\u6444\u5f71\u5e08\u8fd8\u662f\u6570\u636e\u5206\u6790\u5e08\uff0c\u90fd\u53ef\u4ee5\u901a\u8fc7\u8fd9\u4e2a\u5de5\u5177\u76f4\u89c2\u5730\u7406\u89e3\u56fe\u50cf\u7684\u8272\u5f69\u7ec4\u6210\uff0c\u4f18\u5316\u8bbe\u8ba1\u6216\u8fdb\u884c\u8272\u5f69\u76f8\u5173\u7684\u7814\u7a76\u3002</span></p><p><span style=\" font-size:12pt; font-weight:700;\">\u5f00\u53d1\u56e2\u961f\uff1a</span><span style=\" font-size:12pt;\">ImageColorVisualization \u56e2\u961f"
                        "<br/>\u00a9 2024 ImageColorVisualization \u9879\u76ee\u7ec4 \u4fdd\u7559\u6240\u6709\u6743\u5229<br/></span><span style=\" font-size:12pt; font-weight:700;\">\u8bb8\u53ef\u8bc1\uff1a</span><span style=\" font-size:12pt;\">GNU General Public License v3.0 (GPL-3.0)</span></p><p><span style=\" font-size:12pt; font-weight:700;\">\u7279\u522b\u611f\u8c22\uff1a</span><span style=\" font-size:12pt;\">\u611f\u8c22\u5404\u4f4d\u7f16\u7a0b\u5de5\u4f5c\u8005\u5bf9\u5f00\u6e90\u793e\u533a\u7684\u65e0\u79c1\u5949\u732e\uff01</span></p><p><span style=\" font-size:12pt; font-weight:700;\">\u7528\u6237\u53cd\u9988\u548c\u652f\u6301\uff1a</span><a href=\"mailto:support@imagecolorviz.com\"><span style=\" font-size:12pt; text-decoration: underline; color:#cc5e29;\">support@imagecolorviz.com</span></a></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("InfoPage", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">\u4f7f\u7528\u7684\u7b2c\u4e09\u65b9\u5e93</span></p><p><span style=\" font-size:12pt;\">\u611f\u8c22\u4ee5\u4e0b\u5f00\u6e90\u9879\u76ee\u7684\u8d21\u732e\uff1a </span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("InfoPage", u"VTK", None))
        self.label_3.setText(QCoreApplication.translate("InfoPage", u"QFluentWidgets", None))
        self.label_4.setText(QCoreApplication.translate("InfoPage", u"PySide6", None))
    # retranslateUi

