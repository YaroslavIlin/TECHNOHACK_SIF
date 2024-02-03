# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddPort.ui'
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
        Dialog.resize(742, 515)
        self.numwell = QLabel(Dialog)
        self.numwell.setObjectName(u"numwell")
        self.numwell.setGeometry(QRect(20, 20, 141, 20))
        self.cmb_numwell = QComboBox(Dialog)
        self.cmb_numwell.setObjectName(u"cmb_numwell")
        self.cmb_numwell.setGeometry(QRect(384, 26, 190, 28))
        self.scheme = QLabel(Dialog)
        self.scheme.setObjectName(u"scheme")
        self.scheme.setGeometry(QRect(20, 74, 140, 20))
        self.cmb_scheme = QComboBox(Dialog)
        self.cmb_scheme.setObjectName(u"cmb_scheme")
        self.cmb_scheme.setGeometry(QRect(383, 76, 191, 30))
        self.le_x = QLineEdit(Dialog)
        self.le_x.setObjectName(u"le_x")
        self.le_x.setGeometry(QRect(385, 129, 111, 28))
        self.nports = QLabel(Dialog)
        self.nports.setObjectName(u"nports")
        self.nports.setGeometry(QRect(20, 127, 140, 20))
        self.lenwing = QLabel(Dialog)
        self.lenwing.setObjectName(u"lenwing")
        self.lenwing.setGeometry(QRect(18, 204, 351, 51))
        self.le_lenwingleft = QLineEdit(Dialog)
        self.le_lenwingleft.setObjectName(u"le_lenwingleft")
        self.le_lenwingleft.setGeometry(QRect(384, 214, 113, 28))
        self.le_lenwingright = QLineEdit(Dialog)
        self.le_lenwingright.setObjectName(u"le_lenwingright")
        self.le_lenwingright.setGeometry(QRect(534, 214, 113, 28))
        self.param_Lleft = QLabel(Dialog)
        self.param_Lleft.setObjectName(u"param_Lleft")
        self.param_Lleft.setGeometry(QRect(386, 244, 111, 20))
        self.param_Lleft.setAlignment(Qt.AlignCenter)
        self.param_Lright = QLabel(Dialog)
        self.param_Lright.setObjectName(u"param_Lright")
        self.param_Lright.setGeometry(QRect(536, 244, 111, 20))
        self.param_Lright.setAlignment(Qt.AlignCenter)
        self.translatability = QLabel(Dialog)
        self.translatability.setObjectName(u"translatability")
        self.translatability.setGeometry(QRect(20, 284, 351, 51))
        self.le_translatability = QLineEdit(Dialog)
        self.le_translatability.setObjectName(u"le_translatability")
        self.le_translatability.setGeometry(QRect(384, 296, 113, 28))
        self.cracopening = QLabel(Dialog)
        self.cracopening.setObjectName(u"cracopening")
        self.cracopening.setGeometry(QRect(20, 364, 120, 20))
        self.le_crackfracture = QLineEdit(Dialog)
        self.le_crackfracture.setObjectName(u"le_crackfracture")
        self.le_crackfracture.setGeometry(QRect(381, 356, 113, 28))
        self.btn_access = QPushButton(Dialog)
        self.btn_access.setObjectName(u"btn_access")
        self.btn_access.setGeometry(QRect(440, 450, 106, 35))
        self.btn_decline = QPushButton(Dialog)
        self.btn_decline.setObjectName(u"btn_decline")
        self.btn_decline.setGeometry(QRect(560, 450, 106, 35))
        self.le_y = QLineEdit(Dialog)
        self.le_y.setObjectName(u"le_y")
        self.le_y.setGeometry(QRect(530, 130, 111, 28))
        self.param_x = QLabel(Dialog)
        self.param_x.setObjectName(u"param_x")
        self.param_x.setGeometry(QRect(385, 158, 111, 20))
        self.param_x.setAlignment(Qt.AlignCenter)
        self.param_y = QLabel(Dialog)
        self.param_y.setObjectName(u"param_y")
        self.param_y.setGeometry(QRect(530, 160, 111, 20))
        self.param_y.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.numwell.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u044b:", None))
        self.scheme.setText(QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f:", None))
        self.nports.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430 \u043f\u043e\u0440\u0442\u0430", None))
        self.lenwing.setText(QCoreApplication.translate("Dialog", u"\u0414\u043b\u0438\u043d\u0430 \u043a\u0440\u044b\u043b\u044c\u0435\u0432 \u0437\u0430\u043a\u0440\u0435\u043f\u043b\u0451\u043d\u043d\u043e\u0439 \u0442\u0440\u0435\u0449\u0438\u043d\u044b \u0413\u0420\u041f:", None))
        self.param_Lleft.setText(QCoreApplication.translate("Dialog", u"\u041b\u0435\u0432\u0430\u044f", None))
        self.param_Lright.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0430\u0432\u0430\u044f", None))
        self.translatability.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u043e\u043d\u0438\u0446\u0430\u0435\u043c\u043e\u0441\u0442\u044c \u043f\u0440\u043e\u043f\u043f\u0430\u043d\u0442\u043d\u043e\u0439 \u043f\u0430\u0447\u043a\u0438  kf, \u0414:", None))
        self.cracopening.setText(QCoreApplication.translate("Dialog", u"\u0420\u0430\u0441\u043a\u0440\u044b\u0442\u0438\u0435 w, \u043c\u043c:", None))
        self.btn_access.setText(QCoreApplication.translate("Dialog", u"\u041e\u043a", None))
        self.btn_decline.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.param_x.setText(QCoreApplication.translate("Dialog", u"x, \u043c", None))
        self.param_y.setText(QCoreApplication.translate("Dialog", u"y, \u043c", None))
    # retranslateUi

