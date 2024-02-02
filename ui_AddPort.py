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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(767, 515)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(380, 460, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.numwell = QLabel(Dialog)
        self.numwell.setObjectName(u"numwell")
        self.numwell.setGeometry(QRect(20, 20, 141, 20))
        self.cmb_numwell = QComboBox(Dialog)
        self.cmb_numwell.setObjectName(u"cmb_numwell")
        self.cmb_numwell.setGeometry(QRect(388, 26, 190, 28))
        self.scheme = QLabel(Dialog)
        self.scheme.setObjectName(u"scheme")
        self.scheme.setGeometry(QRect(20, 74, 140, 20))
        self.cmb_scheme = QComboBox(Dialog)
        self.cmb_scheme.setObjectName(u"cmb_scheme")
        self.cmb_scheme.setGeometry(QRect(388, 76, 190, 30))
        self.le_nports = QLineEdit(Dialog)
        self.le_nports.setObjectName(u"le_nports")
        self.le_nports.setGeometry(QRect(388, 130, 101, 28))
        self.nports = QLabel(Dialog)
        self.nports.setObjectName(u"nports")
        self.nports.setGeometry(QRect(20, 127, 140, 20))
        self.lenwing = QLabel(Dialog)
        self.lenwing.setObjectName(u"lenwing")
        self.lenwing.setGeometry(QRect(18, 180, 351, 51))
        self.le_lenwingleft = QLineEdit(Dialog)
        self.le_lenwingleft.setObjectName(u"le_lenwingleft")
        self.le_lenwingleft.setGeometry(QRect(384, 190, 113, 28))
        self.le_lenwingright = QLineEdit(Dialog)
        self.le_lenwingright.setObjectName(u"le_lenwingright")
        self.le_lenwingright.setGeometry(QRect(534, 190, 113, 28))
        self.para_Lleft = QLabel(Dialog)
        self.para_Lleft.setObjectName(u"para_Lleft")
        self.para_Lleft.setGeometry(QRect(386, 220, 111, 20))
        self.para_Lleft.setAlignment(Qt.AlignCenter)
        self.param_Lright = QLabel(Dialog)
        self.param_Lright.setObjectName(u"param_Lright")
        self.param_Lright.setGeometry(QRect(536, 220, 111, 20))
        self.param_Lright.setAlignment(Qt.AlignCenter)
        self.translatability = QLabel(Dialog)
        self.translatability.setObjectName(u"translatability")
        self.translatability.setGeometry(QRect(20, 260, 351, 51))
        self.le_translatability = QLineEdit(Dialog)
        self.le_translatability.setObjectName(u"le_translatability")
        self.le_translatability.setGeometry(QRect(384, 272, 113, 28))
        self.cracopening = QLabel(Dialog)
        self.cracopening.setObjectName(u"cracopening")
        self.cracopening.setGeometry(QRect(20, 340, 120, 20))
        self.le_crackopening = QLineEdit(Dialog)
        self.le_crackopening.setObjectName(u"le_crackopening")
        self.le_crackopening.setGeometry(QRect(381, 332, 113, 28))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.numwell.setText(QCoreApplication.translate("Dialog", u"\u041d\u043e\u043c\u0435\u0440 \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u044b:", None))
        self.scheme.setText(QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f:", None))
        self.nports.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0440\u0442\u043e\u0432", None))
        self.lenwing.setText(QCoreApplication.translate("Dialog", u"\u0414\u043b\u0438\u043d\u0430 \u043a\u0440\u044b\u043b\u044c\u0435\u0432 \u0437\u0430\u043a\u0440\u0435\u043f\u043b\u0451\u043d\u043d\u043e\u0439 \u0442\u0440\u0435\u0449\u0438\u043d\u044b \u0413\u0420\u041f:", None))
        self.para_Lleft.setText(QCoreApplication.translate("Dialog", u"\u041b\u0435\u0432\u0430\u044f", None))
        self.param_Lright.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0430\u0432\u0430\u044f", None))
        self.translatability.setText(QCoreApplication.translate("Dialog", u"\u041f\u0440\u043e\u043d\u0438\u0446\u0430\u0435\u043c\u043e\u0441\u0442\u044c \u043f\u0440\u043e\u043f\u043f\u0430\u043d\u0442\u043d\u043e\u0439 \u043f\u0430\u0447\u043a\u0438  kf, \u0414:", None))
        self.cracopening.setText(QCoreApplication.translate("Dialog", u"\u0420\u0430\u0441\u043a\u0440\u044b\u0442\u0438\u0435 w, \u043c\u043c:", None))
    # retranslateUi

