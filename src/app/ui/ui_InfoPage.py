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

from qfluentwidgets import (BodyLabel, ElevatedCardWidget, HyperlinkLabel, ImageLabel,
    ScrollArea, SimpleCardWidget, StrongBodyLabel)

class Ui_InfoPage(object):
    def setupUi(self, InfoPage):
        if not InfoPage.objectName():
            InfoPage.setObjectName(u"InfoPage")
        InfoPage.resize(1100, 700)
        InfoPage.setWindowTitle(u"InfoPage")
        InfoPage.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -144, 1065, 826))
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
        self.verticalLayout_3.setSpacing(11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_3)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_5 = BodyLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_5.setFont(font)

        self.verticalLayout_8.addWidget(self.label_5)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_7 = BodyLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.label_8 = BodyLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(12)
        self.label_8.setFont(font1)
        self.label_8.setText(u"1.0.0")

        self.horizontalLayout_6.addWidget(self.label_8)


        self.verticalLayout_8.addWidget(self.frame_4)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.label_9 = BodyLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)
        self.label_9.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_9)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_6)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_13 = BodyLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_13)

        self.label_14 = BodyLabel(self.frame_7)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setFont(font1)

        self.horizontalLayout_8.addWidget(self.label_14)


        self.verticalLayout_9.addWidget(self.frame_7)

        self.label = BodyLabel(self.frame_6)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.verticalLayout_9.addWidget(self.label)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_15 = BodyLabel(self.frame_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_15)

        self.label_16 = BodyLabel(self.frame_8)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setFont(font1)
        self.label_16.setText(u"GNU General Public License v3.0 (GPL-3.0)")

        self.horizontalLayout_9.addWidget(self.label_16)


        self.verticalLayout_9.addWidget(self.frame_8)


        self.verticalLayout_3.addWidget(self.frame_6)

        self.frame_9 = QFrame(self.frame)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_10 = BodyLabel(self.frame_9)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_10)

        self.label_17 = BodyLabel(self.frame_9)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setFont(font1)

        self.horizontalLayout_10.addWidget(self.label_17)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_12 = BodyLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_12)

        self.support_button = HyperlinkLabel(self.frame_5)
        self.support_button.setObjectName(u"support_button")
        self.support_button.setFont(font1)
        self.support_button.setText(u"support@imagecolorviz.com")

        self.horizontalLayout_7.addWidget(self.support_button)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addWidget(self.frame_5)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = SimpleCardWidget(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.frame_10 = QFrame(self.frame_2)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_10)
        self.verticalLayout_10.setSpacing(11)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_11 = BodyLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.verticalLayout_10.addWidget(self.label_11)

        self.label_18 = BodyLabel(self.frame_10)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font1)

        self.verticalLayout_10.addWidget(self.label_18)


        self.verticalLayout_4.addWidget(self.frame_10)

        self.widget_2 = QWidget(self.frame_2)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.card_vtk = ElevatedCardWidget(self.widget_2)
        self.card_vtk.setObjectName(u"card_vtk")
        self.card_vtk.setMinimumSize(QSize(0, 270))
        self.card_vtk.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_vtk.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_vtk.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.card_vtk)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(30, 50, 30, 50)
        self.img_label_vtk = ImageLabel(self.card_vtk)
        self.img_label_vtk.setObjectName(u"img_label_vtk")
        self.img_label_vtk.setPixmap(QPixmap(u":/logo/vtk"))

        self.verticalLayout_7.addWidget(self.img_label_vtk, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_6 = StrongBodyLabel(self.card_vtk)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setText(u"VTK")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_6, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)


        self.gridLayout.addWidget(self.card_vtk, 0, 3, 1, 1)

        self.card_qfw = ElevatedCardWidget(self.widget_2)
        self.card_qfw.setObjectName(u"card_qfw")
        self.card_qfw.setMinimumSize(QSize(0, 270))
        self.card_qfw.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_qfw.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_qfw.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.card_qfw)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(30, 50, 30, 50)
        self.img_label_qfw = ImageLabel(self.card_qfw)
        self.img_label_qfw.setObjectName(u"img_label_qfw")
        self.img_label_qfw.setPixmap(QPixmap(u":/logo/qfluentwidgets"))

        self.verticalLayout_6.addWidget(self.img_label_qfw, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_3 = StrongBodyLabel(self.card_qfw)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText(u"QFluentWidgets")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)


        self.gridLayout.addWidget(self.card_qfw, 0, 1, 1, 1)

        self.card_pyqt = ElevatedCardWidget(self.widget_2)
        self.card_pyqt.setObjectName(u"card_pyqt")
        self.card_pyqt.setMinimumSize(QSize(0, 270))
        self.card_pyqt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_pyqt.setFrameShape(QFrame.Shape.StyledPanel)
        self.card_pyqt.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.card_pyqt)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(30, 50, 30, 50)
        self.img_label_pyqt = ImageLabel(self.card_pyqt)
        self.img_label_pyqt.setObjectName(u"img_label_pyqt")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.img_label_pyqt.sizePolicy().hasHeightForWidth())
        self.img_label_pyqt.setSizePolicy(sizePolicy2)
        self.img_label_pyqt.setPixmap(QPixmap(u":/logo/pyqt"))
        self.img_label_pyqt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.img_label_pyqt, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.label_4 = StrongBodyLabel(self.card_pyqt)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setText(u"PySide6")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignBottom)


        self.gridLayout.addWidget(self.card_pyqt, 0, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_4.addWidget(self.widget_2)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(InfoPage)

        QMetaObject.connectSlotsByName(InfoPage)
    # setupUi

    def retranslateUi(self, InfoPage):
        self.label_5.setText(QCoreApplication.translate("InfoPage", u"About ImageColorVisualization", None))
        self.label_7.setText(QCoreApplication.translate("InfoPage", u"Version:", None))
        self.label_9.setText(QCoreApplication.translate("InfoPage", u"ImageColorVisualization is a tool for visualizing colors in images, helping users analyze and display color distributions within images. Whether you are a designer, photographer, or data analyst, this tool allows you to understand the color composition of images visually, optimize designs, or conduct color-related research.", None))
        self.label_13.setText(QCoreApplication.translate("InfoPage", u"Development Team:", None))
        self.label_14.setText(QCoreApplication.translate("InfoPage", u"ImageColorVisualization Team", None))
        self.label.setText(QCoreApplication.translate("InfoPage", u"\u00a9 2024 ImageColorVisualization Project Group All Rights Reserved", None))
        self.label_15.setText(QCoreApplication.translate("InfoPage", u"License:", None))
        self.label_10.setText(QCoreApplication.translate("InfoPage", u"Special Thanks:", None))
        self.label_17.setText(QCoreApplication.translate("InfoPage", u"Thanks to all the programmers for their selfless contributions to the open-source community!", None))
        self.label_12.setText(QCoreApplication.translate("InfoPage", u"User Feedback and Support:", None))
        self.label_11.setText(QCoreApplication.translate("InfoPage", u"Third-Party Libraries Used", None))
        self.label_18.setText(QCoreApplication.translate("InfoPage", u"Thanks to the contributions of the following open-source projects:", None))
        pass
    # retranslateUi

