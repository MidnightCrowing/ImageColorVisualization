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

from qfluentwidgets import (ImageLabel, PushButton, ScrollArea)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_ComparePage(object):
    def setupUi(self, ComparePage):
        if not ComparePage.objectName():
            ComparePage.setObjectName(u"ComparePage")
        ComparePage.resize(805, 548)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 787, 530))
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
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(88, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.select_btn_1 = PushButton(self.frame_3)
        self.select_btn_1.setObjectName(u"select_btn_1")

        self.verticalLayout_2.addWidget(self.select_btn_1)

        self.img_label_1 = ImageLabel(self.frame_3)
        self.img_label_1.setObjectName(u"img_label_1")
        self.img_label_1.setMinimumSize(QSize(0, 140))
        self.img_label_1.setMaximumSize(QSize(16777215, 140))

        self.verticalLayout_2.addWidget(self.img_label_1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.vtk_widget_1 = QVTKRenderWindowInteractor(self.frame_3)
        self.vtk_widget_1.setObjectName(u"vtk_widget_1")
        self.vtk_widget_1.setMinimumSize(QSize(200, 200))
        self.vtk_widget_1.setMaximumSize(QSize(200, 200))

        self.verticalLayout_2.addWidget(self.vtk_widget_1)

        self.horizontalLayout.addWidget(self.frame_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.select_btn_2 = PushButton(self.frame_4)
        self.select_btn_2.setObjectName(u"select_btn_2")

        self.verticalLayout_3.addWidget(self.select_btn_2)

        self.img_label_2 = ImageLabel(self.frame_4)
        self.img_label_2.setObjectName(u"img_label_2")
        self.img_label_2.setMinimumSize(QSize(0, 140))
        self.img_label_2.setMaximumSize(QSize(16777215, 140))

        self.verticalLayout_3.addWidget(self.img_label_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.vtk_widget_2 = QVTKRenderWindowInteractor(self.frame_4)
        self.vtk_widget_2.setObjectName(u"vtk_widget_2")
        self.vtk_widget_2.setMinimumSize(QSize(200, 200))
        self.vtk_widget_2.setMaximumSize(QSize(200, 200))

        self.verticalLayout_3.addWidget(self.vtk_widget_2)

        self.horizontalLayout.addWidget(self.frame_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.verticalLayout_4.addWidget(self.frame)

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

