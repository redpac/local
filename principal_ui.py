# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'principal.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Principal(object):
    def setupUi(self, Principal):
        if not Principal.objectName():
            Principal.setObjectName(u"Principal")
        Principal.resize(980, 650)
        Principal.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        Principal.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AddressBookNew))
        Principal.setWindowIcon(icon)
        Principal.setStyleSheet(u"QMainWindow { background: #949dff; }\n"
"QWidget#sidebar { background: #ffffff; border-right: 1px solid #dfe5e7; }\n"
"QWidget#header { background: #ffffff; border-bottom: 1px solid #dfe5e7; }\n"
"QLabel#title { color: #111b21; font-size: 18px; font-weight: 700; }\n"
"QLabel#sectionTitle { color: #54656f; font-size: 12px; font-weight: 700; }\n"
"QLineEdit { background: #f0f2f5; border: 0; border-radius: 8px; padding: 9px 12px; color: #111b21; }\n"
"QListWidget { border: 0; background: transparent; outline: 0; }\n"
"QListWidget::item { padding: 11px; border-bottom: 1px solid #f0f2f5; }\n"
"QListWidget::item:selected { background: #ebf5f2; color: #111b21; }\n"
"QLabel#avatar { background: #d9fdd3; color: #075e54; border-radius: 24px; font-size: 21px; font-weight: 700; }\n"
"QLabel#perfilAvatar { background: #00a884; color: white; border-radius: 19px; font-size: 16px; font-weight: 700; }\n"
"QLabel#emptyTitle { color: #41525d; font-size: 22px; font-weight: 600; }\n"
"QLabel#emptyText { color: #667781; font-size: "
                        "14px; }\n"
"")
        self.actionConectar = QAction(Principal)
        self.actionConectar.setObjectName(u"actionConectar")
        self.actionSalir = QAction(Principal)
        self.actionSalir.setObjectName(u"actionSalir")
        self.centralwidget = QWidget(Principal)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebarLayout = QVBoxLayout()
        self.sidebarLayout.setSpacing(12)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(16, 18, 16, 16)
        self.profileLayout = QHBoxLayout()
        self.profileLayout.setObjectName(u"profileLayout")
        self.profileLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.profileLayout.setContentsMargins(-1, 10, -1, 10)
        self.perfilAvatar = QLabel(self.centralwidget)
        self.perfilAvatar.setObjectName(u"perfilAvatar")
        self.perfilAvatar.setMinimumSize(QSize(45, 45))
        self.perfilAvatar.setMaximumSize(QSize(45, 45))
        self.perfilAvatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.profileLayout.addWidget(self.perfilAvatar)

        self.profileText = QVBoxLayout()
        self.profileText.setSpacing(1)
        self.profileText.setObjectName(u"profileText")
        self.perfilnombre = QLabel(self.centralwidget)
        self.perfilnombre.setObjectName(u"perfilnombre")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.perfilnombre.setFont(font)
        self.perfilnombre.setStyleSheet(u"font-weight: 700; color: #111b21;")

        self.profileText.addWidget(self.perfilnombre)

        self.profileStatus = QLabel(self.centralwidget)
        self.profileStatus.setObjectName(u"profileStatus")
        font1 = QFont()
        self.profileStatus.setFont(font1)
        self.profileStatus.setStyleSheet(u"color: #667781; font-size: 11px;")

        self.profileText.addWidget(self.profileStatus)


        self.profileLayout.addLayout(self.profileText)

        self.profileSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.profileLayout.addItem(self.profileSpacer)

        self.configuracionPerfil = QToolButton(self.centralwidget)
        self.configuracionPerfil.setObjectName(u"configuracionPerfil")
        self.configuracionPerfil.setStyleSheet(u"border: 0; color: #54656f; font-size: 20px;")

        self.profileLayout.addWidget(self.configuracionPerfil)


        self.sidebarLayout.addLayout(self.profileLayout)

        self.createButtonsLayout = QHBoxLayout()
        self.createButtonsLayout.setObjectName(u"createButtonsLayout")
        self.create_chat = QPushButton(self.centralwidget)
        self.create_chat.setObjectName(u"create_chat")

        self.createButtonsLayout.addWidget(self.create_chat)

        self.create_group = QPushButton(self.centralwidget)
        self.create_group.setObjectName(u"create_group")

        self.createButtonsLayout.addWidget(self.create_group)

        self.create_channel = QPushButton(self.centralwidget)
        self.create_channel.setObjectName(u"create_channel")

        self.createButtonsLayout.addWidget(self.create_channel)

        self.join_channel = QPushButton(self.centralwidget)
        self.join_channel.setObjectName(u"join_channel")

        self.createButtonsLayout.addWidget(self.join_channel)


        self.sidebarLayout.addLayout(self.createButtonsLayout)

        self.selecchatsreciente = QLabel(self.centralwidget)
        self.selecchatsreciente.setObjectName(u"selecchatsreciente")
        self.selecchatsreciente.setStyleSheet(u"QLabel#sectionTitle { }")

        self.sidebarLayout.addWidget(self.selecchatsreciente)

        self.chatsReciente = QListWidget(self.centralwidget)
        QListWidgetItem(self.chatsReciente)
        QListWidgetItem(self.chatsReciente)
        QListWidgetItem(self.chatsReciente)
        self.chatsReciente.setObjectName(u"chatsReciente")

        self.sidebarLayout.addWidget(self.chatsReciente)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.sidebarLayout.addWidget(self.label)

        self.listWidget = QListWidget(self.centralwidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.sidebarLayout.addWidget(self.listWidget)

        self.seleccanales = QLabel(self.centralwidget)
        self.seleccanales.setObjectName(u"seleccanales")
        self.seleccanales.setStyleSheet(u"QLabel#sectionTitle { }")

        self.sidebarLayout.addWidget(self.seleccanales)

        self.canales = QListWidget(self.centralwidget)
        QListWidgetItem(self.canales)
        QListWidgetItem(self.canales)
        QListWidgetItem(self.canales)
        self.canales.setObjectName(u"canales")
        self.canales.setMaximumSize(QSize(16777215, 120))

        self.sidebarLayout.addWidget(self.canales)


        self.rootLayout.addLayout(self.sidebarLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(10, 5, 24, 5)
        self.avatar = QLabel(self.centralwidget)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(48, 48))
        self.avatar.setMaximumSize(QSize(48, 48))
        self.avatar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.avatar)

        self.chatHeaderText = QVBoxLayout()
        self.chatHeaderText.setSpacing(0)
        self.chatHeaderText.setObjectName(u"chatHeaderText")
        self.chatHeaderText.setContentsMargins(50, 5, 10, 5)
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.chatHeaderText.addWidget(self.title)

        self.subtitle = QLabel(self.centralwidget)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setStyleSheet(u"color: #667781; font-size: 12px;")

        self.chatHeaderText.addWidget(self.subtitle)


        self.headerLayout.addLayout(self.chatHeaderText)

        self.searchButton = QToolButton(self.centralwidget)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setStyleSheet(u"border: 0; font-size: 22px; color: #54656f;")

        self.headerLayout.addWidget(self.searchButton)


        self.mainLayout.addLayout(self.headerLayout)

        self.txtMsgs = QPlainTextEdit(self.centralwidget)
        self.txtMsgs.setObjectName(u"txtMsgs")
        self.txtMsgs.setReadOnly(True)

        self.mainLayout.addWidget(self.txtMsgs)

        self.sendLayout = QHBoxLayout()
        self.sendLayout.setObjectName(u"sendLayout")
        self.sendLayout.setContentsMargins(16, 12, 16, 12)
        self.txtSend = QLineEdit(self.centralwidget)
        self.txtSend.setObjectName(u"txtSend")
        self.txtSend.setMaxLength(1023)

        self.sendLayout.addWidget(self.txtSend)

        self.btnSend = QPushButton(self.centralwidget)
        self.btnSend.setObjectName(u"btnSend")

        self.sendLayout.addWidget(self.btnSend)


        self.mainLayout.addLayout(self.sendLayout)


        self.rootLayout.addLayout(self.mainLayout)

        Principal.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Principal)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 980, 33))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        Principal.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menuArchivo.addAction(self.actionConectar)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionSalir)

        self.retranslateUi(Principal)

        QMetaObject.connectSlotsByName(Principal)
    # setupUi

    def retranslateUi(self, Principal):
        Principal.setWindowTitle(QCoreApplication.translate("Principal", u"Mensajes", None))
        self.actionConectar.setText(QCoreApplication.translate("Principal", u"Co&nectar", None))
#if QT_CONFIG(shortcut)
        self.actionConectar.setShortcut(QCoreApplication.translate("Principal", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionSalir.setText(QCoreApplication.translate("Principal", u"&Salir", None))
#if QT_CONFIG(shortcut)
        self.actionSalir.setShortcut(QCoreApplication.translate("Principal", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.perfilAvatar.setText(QCoreApplication.translate("Principal", u"P1", None))
        self.perfilnombre.setText(QCoreApplication.translate("Principal", u"p1", None))
        self.profileStatus.setText(QCoreApplication.translate("Principal", u"activo", None))
        self.configuracionPerfil.setText(QCoreApplication.translate("Principal", u"\u22ee", None))
        self.create_chat.setText(QCoreApplication.translate("Principal", u"Nuevo chat", None))
        self.create_group.setText(QCoreApplication.translate("Principal", u"Nuevo grupo", None))
        self.create_channel.setText(QCoreApplication.translate("Principal", u"Nuevo canal", None))
        self.join_channel.setText(QCoreApplication.translate("Principal", u"Unir a canal", None))
        self.selecchatsreciente.setText(QCoreApplication.translate("Principal", u"CHATS RECIENTES", None))

        __sortingEnabled = self.chatsReciente.isSortingEnabled()
        self.chatsReciente.setSortingEnabled(False)
        ___qlistwidgetitem = self.chatsReciente.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Principal", u"Chat global", None));
        ___qlistwidgetitem1 = self.chatsReciente.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Principal", u"p1", None));
        ___qlistwidgetitem2 = self.chatsReciente.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Principal", u"p2", None));
        self.chatsReciente.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("Principal", u"GRUPOS", None))

        __sortingEnabled1 = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.listWidget.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Principal", u"g1", None));
        ___qlistwidgetitem4 = self.listWidget.item(1)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Principal", u"g2", None));
        ___qlistwidgetitem5 = self.listWidget.item(2)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Principal", u"g3", None));
        ___qlistwidgetitem6 = self.listWidget.item(3)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Principal", u"g4", None));
        self.listWidget.setSortingEnabled(__sortingEnabled1)

        self.seleccanales.setText(QCoreApplication.translate("Principal", u"CANALES", None))

        __sortingEnabled2 = self.canales.isSortingEnabled()
        self.canales.setSortingEnabled(False)
        ___qlistwidgetitem7 = self.canales.item(0)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Principal", u"c1", None));
        ___qlistwidgetitem8 = self.canales.item(1)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("Principal", u"c2", None));
        ___qlistwidgetitem9 = self.canales.item(2)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("Principal", u"c3", None));
        self.canales.setSortingEnabled(__sortingEnabled2)

        self.avatar.setText(QCoreApplication.translate("Principal", u"P2", None))
        self.title.setText(QCoreApplication.translate("Principal", u"p2", None))
        self.subtitle.setText(QCoreApplication.translate("Principal", u"activo", None))
#if QT_CONFIG(tooltip)
        self.searchButton.setToolTip(QCoreApplication.translate("Principal", u"<html><head/><body><p align=\"justify\">Actualizar</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.searchButton.setText(QCoreApplication.translate("Principal", u"\u21bb", None))
        self.txtSend.setPlaceholderText(QCoreApplication.translate("Principal", u"Escribe un mensaje", None))
        self.btnSend.setText(QCoreApplication.translate("Principal", u"Enviar", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("Principal", u"&Archivo", None))
    # retranslateUi

