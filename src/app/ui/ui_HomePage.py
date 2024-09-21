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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ..components import (ColorBar, ImageLabelCard)
from qfluentwidgets import (CaptionLabel, PrimaryPushButton, PushButton, StrongBodyLabel)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName(u"HomePage")
        HomePage.resize(1100, 700)
        HomePage.setWindowTitle(u"HomePage")
        HomePage.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.horizontalLayout = QHBoxLayout(HomePage)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(HomePage)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(300, 0))
        self.widget.setMaximumSize(QSize(350, 16777215))
        self.widget.setSizeIncrement(QSize(0, 0))
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
        self.instructions_label = StrongBodyLabel(self.widget_3)
        self.instructions_label.setObjectName(u"instructions_label")

        self.horizontalLayout_2.addWidget(self.instructions_label)

        self.select_file_button = PrimaryPushButton(self.widget_3)
        self.select_file_button.setObjectName(u"select_file_button")
        self.select_file_button.setMaximumSize(QSize(100, 50))

        self.horizontalLayout_2.addWidget(self.select_file_button)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.image_display_area = ImageLabelCard(self.widget_4)
        self.image_display_area.setObjectName(u"image_display_area")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.image_display_area.sizePolicy().hasHeightForWidth())
        self.image_display_area.setSizePolicy(sizePolicy2)
        self.image_display_area.setMinimumSize(QSize(0, 140))
        self.image_display_area.setMaximumSize(QSize(16777215, 140))
        self.image_display_area.setFrameShape(QFrame.Shape.NoFrame)
        self.image_display_area.setFrameShadow(QFrame.Shadow.Plain)
        self.image_display_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.image_display_area)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_3 = QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = CaptionLabel(self.widget_6)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.color_bar = ColorBar(self.widget_6)
        self.color_bar.setObjectName(u"color_bar")
        self.color_bar.setMinimumSize(QSize(0, 80))

        self.verticalLayout_3.addWidget(self.color_bar)


        self.verticalLayout.addWidget(self.widget_6)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = CaptionLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.widget_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.import_point_cloud_btn = PushButton(self.widget_5)
        self.import_point_cloud_btn.setObjectName(u"import_point_cloud_btn")

        self.gridLayout_2.addWidget(self.import_point_cloud_btn, 1, 0, 1, 1)

        self.export_point_cloud_btn = PushButton(self.widget_5)
        self.export_point_cloud_btn.setObjectName(u"export_point_cloud_btn")

        self.gridLayout_2.addWidget(self.export_point_cloud_btn, 1, 1, 1, 1)

        self.export_chart_btn = PushButton(self.widget_5)
        self.export_chart_btn.setObjectName(u"export_chart_btn")

        self.gridLayout_2.addWidget(self.export_chart_btn, 0, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.vtk_widget = QVTKRenderWindowInteractor(HomePage)
        self.vtk_widget.setObjectName(u"vtk_widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.vtk_widget.sizePolicy().hasHeightForWidth())
        self.vtk_widget.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.vtk_widget)


        self.retranslateUi(HomePage)
        self.select_file_button.clicked.connect(HomePage.open_file_dialog)

        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        self.instructions_label.setText(QCoreApplication.translate("HomePage", u"Please select a file:", None))
        self.select_file_button.setText(QCoreApplication.translate("HomePage", u"Browse...", None))
        self.label_2.setText(QCoreApplication.translate("HomePage", u"Dominant Colors", None))
        self.label.setText(QCoreApplication.translate("HomePage", u"Import/Export", None))
        self.import_point_cloud_btn.setText(QCoreApplication.translate("HomePage", u"Import Point Cloud", None))
        self.export_point_cloud_btn.setText(QCoreApplication.translate("HomePage", u"Export Point Cloud", None))
        self.export_chart_btn.setText(QCoreApplication.translate("HomePage", u"Export Chart", None))
        pass
    # retranslateUi

