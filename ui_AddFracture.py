# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddFracture.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(541, 310)
        self.scheme = QLabel(Dialog)
        self.scheme.setObjectName(u"scheme")
        self.scheme.setGeometry(QRect(20, 22, 161, 20))
        self.cmb_scheme = QComboBox(Dialog)
        self.cmb_scheme.setObjectName(u"cmb_scheme")
        self.cmb_scheme.setGeometry(QRect(215, 18, 321, 28))
        self.numwell = QLabel(Dialog)
        self.numwell.setObjectName(u"numwell")
        self.numwell.setGeometry(QRect(20, 74, 150, 20))
        self.numport = QLabel(Dialog)
        self.numport.setObjectName(u"numport")
        self.numport.setGeometry(QRect(20, 125, 150, 20))
        self.cmb_numwell = QComboBox(Dialog)
        self.cmb_numwell.setObjectName(u"cmb_numwell")
        self.cmb_numwell.setGeometry(QRect(215, 70, 130, 28))
        self.cmb_numport = QComboBox(Dialog)
        self.cmb_numport.setObjectName(u"cmb_numport")
        self.cmb_numport.setGeometry(QRect(216, 120, 130, 28))
        self.lenS = QLabel(Dialog)
        self.lenS.setObjectName(u"lenS")
        self.lenS.setGeometry(QRect(20, 180, 185, 20))
        self.le_lenleft = QLineEdit(Dialog)
        self.le_lenleft.setObjectName(u"le_lenleft")
        self.le_lenleft.setGeometry(QRect(217, 178, 80, 28))
        self.le_lenright = QLineEdit(Dialog)
        self.le_lenright.setObjectName(u"le_lenright")
        self.le_lenright.setGeometry(QRect(310, 178, 80, 28))
        self.left = QLabel(Dialog)
        self.left.setObjectName(u"left")
        self.left.setGeometry(QRect(217, 208, 80, 20))
        self.left.setAlignment(Qt.AlignCenter)
        self.right = QLabel(Dialog)
        self.right.setObjectName(u"right")
        self.right.setGeometry(QRect(310, 207, 80, 20))
        self.right.setAlignment(Qt.AlignCenter)
        self.btn_accept = QPushButton(Dialog)
        self.btn_accept.setObjectName(u"btn_accept")
        self.btn_accept.setGeometry(QRect(270, 260, 106, 35))
        self.btn_decline = QPushButton(Dialog)
        self.btn_decline.setObjectName(u"btn_decline")
        self.btn_decline.setGeometry(QRect(400, 260, 106, 35))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.scheme.setText(QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f:", None))
        self.numwell.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u044b:", None))
        self.numport.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u043f\u043e\u0440\u0442\u0430:", None))
        self.lenS.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u043b\u0443\u0434\u043b\u0438\u043d\u044b \u043f\u0440\u0434\u0437\u0430\u0434\u0430\u043d\u043d\u043e\u0433\u043e \u043f\u0443\u0442\u0438:", None))
        self.left.setText(QCoreApplication.translate("Dialog", u"\u041b\u0435\u0432\u0430\u044f", None))
        self.right.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0430\u0432\u0430\u044f", None))
        self.btn_accept.setText(QCoreApplication.translate("Dialog", u"\u041e\u043a", None))
        self.btn_decline.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

