# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HomePage.ui'
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

from qfluentwidgets import (ImageLabel, PrimaryPushButton, StrongBodyLabel)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName(u"HomePage")
        HomePage.resize(806, 579)
        self.horizontalLayout = QHBoxLayout(HomePage)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(HomePage)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QSize(300, 16777215))
        self.widget.setSizeIncrement(QSize(0, 0))
        self.widget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = StrongBodyLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.pushButton_2 = PrimaryPushButton(self.widget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(100, 50))

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(120, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.image_preview = ImageLabel(self.widget_4)
        self.image_preview.setObjectName(u"image_preview")
        sizePolicy1.setHeightForWidth(self.image_preview.sizePolicy().hasHeightForWidth())
        self.image_preview.setSizePolicy(sizePolicy1)
        self.image_preview.setMinimumSize(QSize(0, 140))
        self.image_preview.setMaximumSize(QSize(16777215, 140))
        self.image_preview.setFrameShape(QFrame.Shape.NoFrame)
        self.image_preview.setFrameShadow(QFrame.Shadow.Plain)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.image_preview)

        self.horizontalSpacer_2 = QSpacerItem(120, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.vtk_widget = QVTKRenderWindowInteractor(HomePage)
        self.vtk_widget.setObjectName(u"vtk_widget")

        self.horizontalLayout.addWidget(self.vtk_widget)


        self.retranslateUi(HomePage)

        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        HomePage.setWindowTitle(QCoreApplication.translate("HomePage", u"Form", None))
        self.label.setText(QCoreApplication.translate("HomePage", u"\u56fe\u7247\u9884\u89c8", None))
        self.pushButton_2.setText(QCoreApplication.translate("HomePage", u"\u9009\u62e9...", None))
    # retranslateUi

