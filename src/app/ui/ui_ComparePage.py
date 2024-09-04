# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ComparePage.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ..components import ImageLabelCard
from qfluentwidgets import (PushButton, ScrollArea, ToggleToolButton)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_ComparePage(object):
    def setupUi(self, ComparePage):
        if not ComparePage.objectName():
            ComparePage.setObjectName(u"ComparePage")
        ComparePage.resize(1100, 700)
        ComparePage.setWindowTitle(u"ComparePage")
        ComparePage.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(ComparePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = ScrollArea(ComparePage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea{background: transparent; border: none}")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1065, 1204))
        self.scrollAreaWidgetContents.setStyleSheet(u"QWidget{background: transparent}")
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame = QFrame(self.widget_2)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(88, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QSize(400, 16777215))
        self.frame_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_4 = QWidget(self.frame_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.select_btn_1 = PushButton(self.widget_4)
        self.select_btn_1.setObjectName(u"select_btn_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.select_btn_1.sizePolicy().hasHeightForWidth())
        self.select_btn_1.setSizePolicy(sizePolicy1)
        self.select_btn_1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_5.addWidget(self.select_btn_1)

        self.line_2 = QFrame(self.widget_4)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMidLineWidth(1)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_5.addWidget(self.line_2)

        self.toggle_btn_img_1 = ToggleToolButton(self.widget_4)
        self.toggle_btn_img_1.setObjectName(u"toggle_btn_img_1")

        self.horizontalLayout_5.addWidget(self.toggle_btn_img_1)

        self.toggle_btn_point_1 = ToggleToolButton(self.widget_4)
        self.toggle_btn_point_1.setObjectName(u"toggle_btn_point_1")

        self.horizontalLayout_5.addWidget(self.toggle_btn_point_1)


        self.verticalLayout_2.addWidget(self.widget_4)

        self.img_widget_1 = QWidget(self.frame_3)
        self.img_widget_1.setObjectName(u"img_widget_1")
        sizePolicy.setHeightForWidth(self.img_widget_1.sizePolicy().hasHeightForWidth())
        self.img_widget_1.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.img_widget_1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.img_label_1 = ImageLabelCard(self.img_widget_1)
        self.img_label_1.setObjectName(u"img_label_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.img_label_1.sizePolicy().hasHeightForWidth())
        self.img_label_1.setSizePolicy(sizePolicy2)
        self.img_label_1.setMinimumSize(QSize(0, 140))
        self.img_label_1.setMaximumSize(QSize(16777215, 140))
        self.img_label_1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_3.addWidget(self.img_label_1)

        self.horizontalSpacer_5 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addWidget(self.img_widget_1)

        self.vtk_widget_1 = QVTKRenderWindowInteractor(self.frame_3)
        self.vtk_widget_1.setObjectName(u"vtk_widget_1")
        sizePolicy.setHeightForWidth(self.vtk_widget_1.sizePolicy().hasHeightForWidth())
        self.vtk_widget_1.setSizePolicy(sizePolicy)
        self.vtk_widget_1.setMinimumSize(QSize(200, 200))
        self.vtk_widget_1.setMaximumSize(QSize(400, 400))
        self.vtk_widget_1.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout_2.addWidget(self.vtk_widget_1)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addWidget(self.frame_3)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_12)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMaximumSize(QSize(400, 16777215))
        self.frame_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_5 = QWidget(self.frame_4)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.select_btn_2 = PushButton(self.widget_5)
        self.select_btn_2.setObjectName(u"select_btn_2")
        self.select_btn_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_6.addWidget(self.select_btn_2)

        self.line_3 = QFrame(self.widget_5)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMidLineWidth(1)
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_6.addWidget(self.line_3)

        self.toggle_btn_img_2 = ToggleToolButton(self.widget_5)
        self.toggle_btn_img_2.setObjectName(u"toggle_btn_img_2")

        self.horizontalLayout_6.addWidget(self.toggle_btn_img_2)

        self.toggle_btn_point_2 = ToggleToolButton(self.widget_5)
        self.toggle_btn_point_2.setObjectName(u"toggle_btn_point_2")

        self.horizontalLayout_6.addWidget(self.toggle_btn_point_2)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.img_widget_2 = QWidget(self.frame_4)
        self.img_widget_2.setObjectName(u"img_widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.img_widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_6 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.img_label_2 = ImageLabelCard(self.img_widget_2)
        self.img_label_2.setObjectName(u"img_label_2")
        sizePolicy2.setHeightForWidth(self.img_label_2.sizePolicy().hasHeightForWidth())
        self.img_label_2.setSizePolicy(sizePolicy2)
        self.img_label_2.setMinimumSize(QSize(0, 140))
        self.img_label_2.setMaximumSize(QSize(16777215, 140))
        self.img_label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_4.addWidget(self.img_label_2)

        self.horizontalSpacer_7 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addWidget(self.img_widget_2)

        self.vtk_widget_2 = QVTKRenderWindowInteractor(self.frame_4)
        self.vtk_widget_2.setObjectName(u"vtk_widget_2")
        sizePolicy.setHeightForWidth(self.vtk_widget_2.sizePolicy().hasHeightForWidth())
        self.vtk_widget_2.setSizePolicy(sizePolicy)
        self.vtk_widget_2.setMinimumSize(QSize(200, 200))
        self.vtk_widget_2.setMaximumSize(QSize(400, 400))
        self.vtk_widget_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout_3.addWidget(self.vtk_widget_2)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)


        self.horizontalLayout.addWidget(self.frame_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addWidget(self.frame)

        self.frame_2 = QFrame(self.widget_2)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_9 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.vtk_widget_compare = QVTKRenderWindowInteractor(self.frame_2)
        self.vtk_widget_compare.setObjectName(u"vtk_widget_compare")
        sizePolicy2.setHeightForWidth(self.vtk_widget_compare.sizePolicy().hasHeightForWidth())
        self.vtk_widget_compare.setSizePolicy(sizePolicy2)
        self.vtk_widget_compare.setMinimumSize(QSize(400, 700))
        self.vtk_widget_compare.setMaximumSize(QSize(1000, 16777215))

        self.horizontalLayout_7.addWidget(self.vtk_widget_compare)

        self.horizontalSpacer_8 = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(ComparePage)

        QMetaObject.connectSlotsByName(ComparePage)
    # setupUi

    def retranslateUi(self, ComparePage):
        self.select_btn_1.setText(QCoreApplication.translate("ComparePage", u"Select image", None))
        self.select_btn_2.setText(QCoreApplication.translate("ComparePage", u"Select image", None))
        pass
    # retranslateUi

