# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'conectar.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(559, 239)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(391, 164))
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u"background-color: #2b1b3d; color: #ffffff;")
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.txtPort = QLineEdit(Dialog)
        self.txtPort.setObjectName(u"txtPort")

        self.gridLayout.addWidget(self.txtPort, 0, 3, 1, 1)

        self.txtUser = QLineEdit(Dialog)
        self.txtUser.setObjectName(u"txtUser")
        self.txtUser.setInputMethodHints(Qt.InputMethodHint.ImhLowercaseOnly|Qt.InputMethodHint.ImhNoAutoUppercase)

        self.gridLayout.addWidget(self.txtUser, 1, 1, 1, 1)

        self.txtServer = QLineEdit(Dialog)
        self.txtServer.setObjectName(u"txtServer")

        self.gridLayout.addWidget(self.txtServer, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

        self.gridLayout.addWidget(self.buttonBox, 4, 3, 1, 1)

        self.txtPassword = QLineEdit(Dialog)
        self.txtPassword.setObjectName(u"txtPassword")

        self.gridLayout.addWidget(self.txtPassword, 4, 1, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        QWidget.setTabOrder(self.txtServer, self.txtPort)
        QWidget.setTabOrder(self.txtPort, self.txtUser)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Conectar", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Puerto", None))
        self.txtPort.setInputMask("")
        self.txtPort.setPlaceholderText(QCoreApplication.translate("Dialog", u"65535", None))
        self.txtUser.setPlaceholderText(QCoreApplication.translate("Dialog", u"anon", None))
        self.txtServer.setPlaceholderText(QCoreApplication.translate("Dialog", u"127.0.0.1", None))
        self.txtPassword.setPlaceholderText(QCoreApplication.translate("Dialog", u"agrega una contrase\u00f1a", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Servidor", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Usuario", None))
    # retranslateUi

