# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddWell.ui'
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
        Dialog.resize(383, 317)
        self.cmb_typegeo = QComboBox(Dialog)
        self.cmb_typegeo.setObjectName(u"cmb_typegeo")
        self.cmb_typegeo.setGeometry(QRect(200, 50, 171, 28))
        self.typegeo = QLabel(Dialog)
        self.typegeo.setObjectName(u"typegeo")
        self.typegeo.setGeometry(QRect(20, 50, 131, 20))
        self.cmb_typewell = QComboBox(Dialog)
        self.cmb_typewell.setObjectName(u"cmb_typewell")
        self.cmb_typewell.setGeometry(QRect(200, 90, 171, 28))
        self.typewell = QLabel(Dialog)
        self.typewell.setObjectName(u"typewell")
        self.typewell.setGeometry(QRect(20, 90, 131, 20))
        self.begin = QLabel(Dialog)
        self.begin.setObjectName(u"begin")
        self.begin.setGeometry(QRect(20, 130, 63, 20))
        self.namewell = QLabel(Dialog)
        self.namewell.setObjectName(u"namewell")
        self.namewell.setGeometry(QRect(20, 10, 131, 20))
        self.le_namewell = QLineEdit(Dialog)
        self.le_namewell.setObjectName(u"le_namewell")
        self.le_namewell.setGeometry(QRect(200, 10, 171, 28))
        self.le_xbegin = QLineEdit(Dialog)
        self.le_xbegin.setObjectName(u"le_xbegin")
        self.le_xbegin.setGeometry(QRect(200, 130, 81, 28))
        self.le_ybegin = QLineEdit(Dialog)
        self.le_ybegin.setObjectName(u"le_ybegin")
        self.le_ybegin.setGeometry(QRect(290, 130, 81, 28))
        self.le_yend = QLineEdit(Dialog)
        self.le_yend.setObjectName(u"le_yend")
        self.le_yend.setGeometry(QRect(290, 190, 81, 28))
        self.end = QLabel(Dialog)
        self.end.setObjectName(u"end")
        self.end.setGeometry(QRect(20, 190, 63, 20))
        self.le_xend = QLineEdit(Dialog)
        self.le_xend.setObjectName(u"le_xend")
        self.le_xend.setGeometry(QRect(200, 190, 81, 28))
        self.xbegin = QLabel(Dialog)
        self.xbegin.setObjectName(u"xbegin")
        self.xbegin.setGeometry(QRect(202, 160, 81, 20))
        self.xbegin.setLayoutDirection(Qt.LeftToRight)
        self.xbegin.setAlignment(Qt.AlignCenter)
        self.ybegin = QLabel(Dialog)
        self.ybegin.setObjectName(u"ybegin")
        self.ybegin.setGeometry(QRect(290, 160, 81, 20))
        self.ybegin.setLayoutDirection(Qt.LeftToRight)
        self.ybegin.setAlignment(Qt.AlignCenter)
        self.xend = QLabel(Dialog)
        self.xend.setObjectName(u"xend")
        self.xend.setGeometry(QRect(200, 220, 81, 20))
        self.xend.setLayoutDirection(Qt.LeftToRight)
        self.xend.setAlignment(Qt.AlignCenter)
        self.yend = QLabel(Dialog)
        self.yend.setObjectName(u"yend")
        self.yend.setGeometry(QRect(290, 220, 81, 20))
        self.yend.setLayoutDirection(Qt.LeftToRight)
        self.yend.setAlignment(Qt.AlignCenter)
        self.btn_accept = QPushButton(Dialog)
        self.btn_accept.setObjectName(u"btn_accept")
        self.btn_accept.setGeometry(QRect(180, 270, 83, 29))
        self.btn_decline = QPushButton(Dialog)
        self.btn_decline.setObjectName(u"btn_decline")
        self.btn_decline.setGeometry(QRect(280, 270, 83, 29))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.typegeo.setText(QCoreApplication.translate("Dialog", u"\u0422\u0438\u043f \u0433\u0435\u043e\u043c\u0435\u0442\u0440\u0438\u0438:", None))
        self.typewell.setText(QCoreApplication.translate("Dialog", u"\u0422\u0438\u043f \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u044b:", None))
        self.begin.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0447\u0430\u043b\u043e:", None))
        self.namewell.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u044b:", None))
        self.end.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043d\u0435\u0446:", None))
        self.xbegin.setText(QCoreApplication.translate("Dialog", u"x, \u043c", None))
        self.ybegin.setText(QCoreApplication.translate("Dialog", u"y, \u043c", None))
        self.xend.setText(QCoreApplication.translate("Dialog", u"x, \u043c", None))
        self.yend.setText(QCoreApplication.translate("Dialog", u"y, \u043c", None))
        self.btn_accept.setText(QCoreApplication.translate("Dialog", u"\u041e\u043a", None))
        self.btn_decline.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

