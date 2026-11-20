# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crear.ui'
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

class Ui_CrearDialog(object):
    def setupUi(self, CrearDialog):
        if not CrearDialog.objectName():
            CrearDialog.setObjectName(u"CrearDialog")
        CrearDialog.setWindowModality(Qt.WindowModality.WindowModal)
        CrearDialog.resize(559, 239)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CrearDialog.sizePolicy().hasHeightForWidth())
        CrearDialog.setSizePolicy(sizePolicy)
        CrearDialog.setMinimumSize(QSize(391, 164))
        CrearDialog.setStyleSheet(u"background-color: #2b1b3d; color: #ffffff;")
        CrearDialog.setModal(True)
        self.gridLayout = QGridLayout(CrearDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelTitulo = QLabel(CrearDialog)
        self.labelTitulo.setObjectName(u"labelTitulo")

        self.gridLayout.addWidget(self.labelTitulo, 0, 0, 1, 1)

        self.txtNombre = QLineEdit(CrearDialog)
        self.txtNombre.setObjectName(u"txtNombre")

        self.gridLayout.addWidget(self.txtNombre, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(CrearDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)


        self.retranslateUi(CrearDialog)
        self.buttonBox.accepted.connect(CrearDialog.accept)
        self.buttonBox.rejected.connect(CrearDialog.reject)

        QMetaObject.connectSlotsByName(CrearDialog)
    # setupUi

    def retranslateUi(self, CrearDialog):
        CrearDialog.setWindowTitle(QCoreApplication.translate("CrearDialog", u"Crear", None))
        self.labelTitulo.setText(QCoreApplication.translate("CrearDialog", u"Nombre", None))
        self.txtNombre.setPlaceholderText(QCoreApplication.translate("CrearDialog", u"Escribe el nombre", None))
    # retranslateUi

