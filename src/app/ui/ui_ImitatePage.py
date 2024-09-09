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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

from ..components import StepProgressBar

class Ui_ImitatePage(object):
    def setupUi(self, ImitatePage):
        if not ImitatePage.objectName():
            ImitatePage.setObjectName(u"ImitatePage")
        ImitatePage.resize(1100, 700)
        ImitatePage.setWindowTitle(u"ImitatePage")
        self.verticalLayout = QVBoxLayout(ImitatePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = StepProgressBar(ImitatePage)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ImitatePage)

        QMetaObject.connectSlotsByName(ImitatePage)
    # setupUi

    def retranslateUi(self, ImitatePage):
        pass
    # retranslateUi

