# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImitatePage.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from ..components import (ImageLabelCard, RightArrow, StepProgressBar)
from qfluentwidgets import (BodyLabel, PrimaryPushButton, ScrollArea, ToolButton)

class Ui_ImitatePage(object):
    def setupUi(self, ImitatePage):
        if not ImitatePage.objectName():
            ImitatePage.setObjectName(u"ImitatePage")
        ImitatePage.resize(1100, 700)
        ImitatePage.setWindowTitle(u"ImitatePage")
        self.verticalLayout = QVBoxLayout(ImitatePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.scrollArea = ScrollArea(ImitatePage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea{background: transparent; border: none}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1083, 731))
        self.scrollAreaWidgetContents.setStyleSheet(u"QWidget{background: transparent}")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = PrimaryPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addWidget(self.widget)

        self.main_widget = QWidget(self.scrollAreaWidgetContents)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout_3 = QVBoxLayout(self.main_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.step_bar = StepProgressBar(self.main_widget)
        self.step_bar.setObjectName(u"step_bar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.step_bar.sizePolicy().hasHeightForWidth())
        self.step_bar.setSizePolicy(sizePolicy1)
        self.step_bar.setMinimumSize(QSize(900, 80))

        self.verticalLayout_3.addWidget(self.step_bar)

        self.widget_2 = QWidget(self.main_widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy3)
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.widget_6 = QWidget(self.widget_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.label = BodyLabel(self.widget_6)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.reference_tool_btn = ToolButton(self.widget_6)
        self.reference_tool_btn.setObjectName(u"reference_tool_btn")

        self.horizontalLayout_3.addWidget(self.reference_tool_btn)


        self.verticalLayout_4.addWidget(self.widget_6)

        self.widget_9 = QWidget(self.widget_3)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy4)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_7 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)

        self.reference_img_label = ImageLabelCard(self.widget_9)
        self.reference_img_label.setObjectName(u"reference_img_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.reference_img_label.sizePolicy().hasHeightForWidth())
        self.reference_img_label.setSizePolicy(sizePolicy5)
        self.reference_img_label.setMinimumSize(QSize(0, 170))

        self.horizontalLayout_6.addWidget(self.reference_img_label)

        self.horizontalSpacer_8 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addWidget(self.widget_9)

        self.verticalSpacer_2 = QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.widget_7 = QWidget(self.widget_3)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.label_2 = BodyLabel(self.widget_7)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.horizontalSpacer_5 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.target_tool_btn = ToolButton(self.widget_7)
        self.target_tool_btn.setObjectName(u"target_tool_btn")

        self.horizontalLayout_4.addWidget(self.target_tool_btn)


        self.verticalLayout_4.addWidget(self.widget_7)

        self.widget_10 = QWidget(self.widget_3)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy4.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy4)
        self.horizontalLayout_7 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_9 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.target_img_label = ImageLabelCard(self.widget_10)
        self.target_img_label.setObjectName(u"target_img_label")
        sizePolicy5.setHeightForWidth(self.target_img_label.sizePolicy().hasHeightForWidth())
        self.target_img_label.setSizePolicy(sizePolicy5)
        self.target_img_label.setMinimumSize(QSize(0, 170))

        self.horizontalLayout_7.addWidget(self.target_img_label)

        self.horizontalSpacer_10 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addWidget(self.widget_10)

        self.verticalSpacer_3 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.horizontalLayout_2.addWidget(self.widget_3)

        self.widget_8 = RightArrow(self.widget_2)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy3.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy3)
        self.widget_8.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.widget_8)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy3.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.label_4 = BodyLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.horizontalSpacer_6 = QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.style_tool_btn = ToolButton(self.widget_5)
        self.style_tool_btn.setObjectName(u"style_tool_btn")

        self.horizontalLayout_5.addWidget(self.style_tool_btn)


        self.verticalLayout_5.addWidget(self.widget_5)

        self.widget_11 = QWidget(self.widget_4)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy4.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy4)
        self.horizontalLayout_8 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_11 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_11)

        self.style_img_label = ImageLabelCard(self.widget_11)
        self.style_img_label.setObjectName(u"style_img_label")
        sizePolicy5.setHeightForWidth(self.style_img_label.sizePolicy().hasHeightForWidth())
        self.style_img_label.setSizePolicy(sizePolicy5)
        self.style_img_label.setMinimumSize(QSize(0, 170))

        self.horizontalLayout_8.addWidget(self.style_img_label)

        self.horizontalSpacer_12 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_12)


        self.verticalLayout_5.addWidget(self.widget_11)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)

        self.verticalSpacer_4 = QSpacerItem(20, 135, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.horizontalLayout_2.addWidget(self.widget_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addWidget(self.widget_2)


        self.verticalLayout_2.addWidget(self.main_widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(ImitatePage)

        QMetaObject.connectSlotsByName(ImitatePage)
    # setupUi

    def retranslateUi(self, ImitatePage):
        self.pushButton.setText(QCoreApplication.translate("ImitatePage", u"Gesture", None))
        self.label.setText(QCoreApplication.translate("ImitatePage", u"Reference Image", None))
        self.reference_tool_btn.setText(QCoreApplication.translate("ImitatePage", u"...", None))
        self.label_2.setText(QCoreApplication.translate("ImitatePage", u"Target Image", None))
        self.target_tool_btn.setText(QCoreApplication.translate("ImitatePage", u"...", None))
        self.label_4.setText(QCoreApplication.translate("ImitatePage", u"Styled Image", None))
        self.style_tool_btn.setText(QCoreApplication.translate("ImitatePage", u"...", None))
        pass
    # retranslateUi

