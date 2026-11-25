import sys
import socket
import time
import os
import html

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QPixmap, QTextCursor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox, QListWidgetItem,
    QListWidget, QPushButton, QLineEdit, QLabel
)

from principal_ui import Ui_Principal
from conectar_ui import Ui_Dialog
from crear_ui import Ui_CrearDialog


SERVER_HOST = "3.149.102.2"
#3.149.102.2
SERVER_PORT = 3091
#3091

class ThreadSocket(QThread):
    #las signal de pyside6 son canales especiales para comunicar a lo de qt con el hilo de red
    signal_message = Signal(str)
    signal_connected = Signal(bool)
    signal_authenticated = Signal(bool, str)
    signal_public_start = Signal()
    signal_public_message = Signal(str)
    signal_public_end = Signal()
    signal_private_list = Signal(object)
    signal_private_history = Signal(str)
    signal_private_live = Signal(str, str, str)
    signal_profile_pic = Signal(str)
    signal_group_list = Signal(object)
    signal_group_history = Signal(str)
    signal_group_live = Signal(str, str, str)
    signal_group_member_check = Signal(bool, str)
    signal_group_name_check = Signal(bool, str)
    signal_channel_list = Signal(object)
    signal_channel_history = Signal(str)
    signal_channel_join_check = Signal(str, str)

    def __init__(self, host, port, name, password):
        super().__init__()
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(5)

    def run(self):
        global connected
        try:
            self.server.connect((self.host, self.port))
            connected = True
            self.server.settimeout(None)
            welcome = self.server.recv(BUFFER_SIZE)
            if welcome:
                self.signal_message.emit(welcome.decode("utf-8"))
            self.server.sendall(bytes(f"--name{self.name}", 'utf-8'))
            time.sleep(0.1)
            self.server.sendall(bytes(f"--password{self.password}", 'utf-8'))
            authentication = self.server.recv(BUFFER_SIZE)
            authentication_text = authentication.decode("utf-8")
            self.signal_message.emit(authentication_text)
            if "<!!Autenticado!!>" not in authentication_text:
                self.signal_authenticated.emit(False, authentication_text)
                self.signal_connected.emit(False)
                return
            self.signal_authenticated.emit(True, authentication_text)
            self.signal_connected.emit(True)
            self.server.sendall(b"--getProfile")

            socket_buffer = ""
            while connected:
                message = self.server.recv(BUFFER_SIZE)
                if message:
                    socket_buffer += message.decode("utf-8")
                    while "\n" in socket_buffer:
                        line, socket_buffer = socket_buffer.split("\n", 1)
                        if line == "--publicStart--": #para marcar el inicio del historial
                            self.signal_public_start.emit()
                        elif line.startswith("--public--"):
                            parts = [part.strip() for part in line[len("--public--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                sender = "Tú" if parts[0] == self.name else parts[0]
                                self.signal_public_message.emit(f"<{sender}> {parts[1]}\n")
                        elif line == "--publicEnd--":#ps aquí acaba
                            self.signal_public_end.emit()
                        elif line.startswith("--privateChat--"):
                            parts = [part.strip() for part in line[len("--privateChat--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                self.signal_private_list.emit(parts)
                            elif len(parts) == 3:
                                self.signal_private_list.emit(parts)
                        elif line.startswith("--profile--"):
                            parts = [part.strip() for part in line[len("--profile--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_profile_pic.emit(parts[0])
                        elif line.startswith("--privateMessage--"):
                            parts = [part.strip() for part in line[len("--privateMessage--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                sender = "Tú" if parts[0] == self.name else parts[0]
                                self.signal_private_history.emit(f"<{sender}> {parts[1]}\n")
                            elif len(parts) == 3:
                                self.signal_private_live.emit(parts[0], parts[1], parts[2])
                        elif line.startswith("--group--"):
                            parts = [part.strip() for part in line[len("--group--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                self.signal_group_list.emit(parts)
                        elif line.startswith("--groupMessage--"):
                            parts = [part.strip() for part in line[len("--groupMessage--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                sender = "Tú" if parts[0] == self.name else parts[0]
                                self.signal_group_history.emit(f"<{sender}> {parts[1]}\n")
                            elif len(parts) == 3:
                                self.signal_group_live.emit(parts[0], parts[1], parts[2])
                        elif line.startswith("--groupMemberValid--"):
                            parts = [part.strip() for part in line[len("--groupMemberValid--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_group_member_check.emit(True, parts[0])
                        elif line.startswith("--groupMemberInvalid--"):
                            parts = [part.strip() for part in line[len("--groupMemberInvalid--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_group_member_check.emit(False, parts[0])
                        elif line.startswith("--groupNameExists--"):
                            parts = [part.strip() for part in line[len("--groupNameExists--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_group_name_check.emit(False, parts[0])
                        elif line.startswith("--groupNameAvailable--"):
                            parts = [part.strip() for part in line[len("--groupNameAvailable--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_group_name_check.emit(True, parts[0])
                        elif line.startswith("--channel--"):
                            parts = [part.strip() for part in line[len("--channel--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                self.signal_channel_list.emit(parts)
                        elif line.startswith("--channelMessage--"):
                            parts = [part.strip() for part in line[len("--channelMessage--"):].split("--") if part.strip()]
                            if len(parts) == 2:
                                sender = "Tú" if parts[0] == self.name else parts[0]
                                self.signal_channel_history.emit(f"<{sender}> {parts[1]}\n")
                        elif line.startswith("--channelJoined--"):
                            parts = [part.strip() for part in line[len("--channelJoined--"):].split("--") if part.strip()]
                            if len(parts) == 1:
                                self.signal_channel_join_check.emit("Joined", parts[0])
                        elif line.startswith(("--channelJoinAvailable--",
                                           "--channelJoinNotFound--",
                                           "--channelJoinOwner--",
                                           "--channelJoinSubscribed--",
                                           "--channelJoinInvalid--")):
                            prefix = line.split("--", 2)[1]
                            parts = [part.strip() for part in line[len("--" + prefix + "--"):].split("--") if part.strip()]
                            status = prefix.removeprefix("channelJoin")
                            if len(parts) == 1:
                                self.signal_channel_join_check.emit(status, parts[0])
                        else:
                            self.signal_message.emit(line + "\n")
                else:
                    self.signal_message.emit("<!!disconected!!>")
                    break

        except (OSError, socket.timeout) as error:
            self.signal_message.emit(f"<!!error: {error}!!>")
            self.signal_connected.emit(False)
        finally:
            connected = False
            try:
                self.server.close()
            except OSError:
                pass

    def stop(self):
        global connected
        connected = False
        try:
            self.server.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self.server.close()
        except OSError:
            pass
        self.wait()


class MainWindow(QMainWindow, Ui_Principal):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.actionConectar.triggered.connect(self.showDialog)
        self.actionSalir.triggered.connect(self.salir)
        self.coneccion = None
        self.btnSalir.clicked.connect(self.actionSalir.trigger)
        self.btnSend.clicked.connect(self.mensaje_saliente)
        self.setWindowTitle("Chat global - Desconectado")
        self.txtSend.returnPressed.connect(self.mensaje_saliente)
        self.title.setText("Chat global")
        self.create_chat.clicked.connect(self.createChat)
        self.create_group.clicked.connect(self.createGroup)
        self.create_channel.clicked.connect(self.createChannel)
        self.join_channel.clicked.connect(self.joinChannel)
        self.chatsReciente.itemClicked.connect(self.chatSeleccionado)
        self.listWidget.itemClicked.connect(self.groupSeleccionado)
        self.canales.itemClicked.connect(self.channelSeleccionado)
        self.searchButton.clicked.connect(self.refresh)
        self.searchButton.setText("↻")
        self.searchButton.setToolTip("Actualizar")
        if self.chatsReciente.count():
            self.chatsReciente.setCurrentRow(0)

        self.chatsReciente.clear()
        self.chatsReciente.addItem("Chat global")
        self.listWidget.clear()
        self.canales.clear()
        self.activeSelection = ("public", None)
        self.setHeaderInitial("P")
        QTimer.singleShot(0, lambda: self.txtSend.setFocus(Qt.OtherFocusReason))

    def chatSeleccionado(self, item):
        if item.text() == "Chat global":
            self.activeSelection = ("public", None)
            self.title.setText("Chat global")
            self.setHeaderInitial("P")
            if self.coneccion is not None:
                self.sendCommand(b"--retrievePublic")
        elif self.coneccion is not None:
            chat_id = item.data(Qt.ItemDataRole.UserRole)
            self.activeSelection = ("private", chat_id)
            self.title.setText(item.text())
            profile_pic = item.data(Qt.ItemDataRole.UserRole + 1)
            self.setHeaderImage(profile_pic)
            self.txtMsgs.clear()
            self.coneccion.server.sendall(f"--retrievePrivate--{chat_id}--".encode("utf-8"))

    def groupSeleccionado(self, item):
        if self.coneccion is not None:
            group_id = item.data(Qt.ItemDataRole.UserRole)
            self.activeSelection = ("group", group_id)
            self.title.setText(item.text())
            self.setHeaderInitial("G")
            self.txtMsgs.clear()
            self.coneccion.server.sendall(f"--retrieveGroup--{group_id}--".encode("utf-8"))
            

    def channelSeleccionado(self, item):
        if self.coneccion is not None:
            channel_id = item.data(Qt.ItemDataRole.UserRole)
            self.activeSelection = ("channel", channel_id)
            self.title.setText(item.text())
            self.setHeaderInitial("C")
            self.txtMsgs.clear()
            self.coneccion.server.sendall(f"--retrieveChannel--{channel_id}--".encode("utf-8"))
            

    def loadPrivateList(self, chat):
        for index in range(self.chatsReciente.count()):
            item = self.chatsReciente.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == chat[0]:
                item.setText(chat[1])
                if len(chat) == 3:
                    item.setData(Qt.ItemDataRole.UserRole + 1, chat[2])
                if self.activeSelection == ("private", chat[0]):
                    self.chatsReciente.setCurrentItem(item)
                return
        item = QListWidgetItem(chat[1])
        item.setData(Qt.ItemDataRole.UserRole, chat[0])
        if len(chat) == 3:
            item.setData(Qt.ItemDataRole.UserRole + 1, chat[2])
        self.chatsReciente.addItem(item)
        if self.activeSelection == ("private", chat[0]):
            self.chatsReciente.setCurrentItem(item)

    def refreshPrivateList(self):
        if self.coneccion is None:
            return
        self.chatsReciente.clear()
        self.chatsReciente.addItem("Chat global")
        if self.activeSelection[0] == "public":
            self.chatsReciente.setCurrentRow(0)
        self.coneccion.server.sendall(b"--retrievePrivate")

    def loadGroupList(self, group):
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == group[0]:
                item.setText(group[1])
                return
        item = QListWidgetItem(group[1])
        item.setData(Qt.ItemDataRole.UserRole, group[0])
        self.listWidget.addItem(item)

    def loadChannelList(self, channel):
        for index in range(self.canales.count()):
            item = self.canales.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == channel[0]:
                item.setText(channel[1])
                return
        item = QListWidgetItem(channel[1])
        item.setData(Qt.ItemDataRole.UserRole, channel[0])
        self.canales.addItem(item)

    def seleccionarChatGlobal(self):
        items = self.chatsReciente.findItems("Chat global", Qt.MatchExactly)
        if items:
            self.chatsReciente.setCurrentItem(items[0])
            self.chatSeleccionado(items[0])

    def sendCommand(self, command):
        if self.coneccion is None:
            return
        self.coneccion.server.sendall(command)
        time.sleep(0.25)

    def retrieveSideLists(self):
        if self.coneccion is None:
            return
        self.chatsReciente.clear()
        self.chatsReciente.addItem("Chat global")
        self.listWidget.clear()
        self.canales.clear()
        self.sendCommand(b"--retrievePrivate")
        #time.sleep(0.1) ya no pq congela la ventana ejej
        self.sendCommand(b"--retrieveGroup")
        self.sendCommand(b"--retrieveChannel")

    def refresh(self):
        if self.coneccion is None:
            return
        self.chatsReciente.clear()
        self.chatsReciente.addItem("Chat global")
        self.listWidget.clear()
        self.canales.clear()
        self.sendCommand(b"--retrievePrivate")
        self.sendCommand(b"--retrieveGroup")
        self.sendCommand(b"--retrieveChannel")
        selection, item_id = self.activeSelection
        if selection == "public":
            self.sendCommand(b"--retrievePublic")
        elif selection == "private":
            self.txtMsgs.clear()
            self.sendCommand(f"--retrievePrivate--{item_id}--".encode("utf-8"))
        elif selection == "group":
            self.txtMsgs.clear()
            self.sendCommand(f"--retrieveGroup--{item_id}--".encode("utf-8"))
        elif selection == "channel":
            self.txtMsgs.clear()
            self.sendCommand(f"--retrieveChannel--{item_id}--".encode("utf-8"))
        
    def mensaje_saliente(self):
        str = self.txtSend.text()
        if str != "" and connected:
            selection, item_id = self.activeSelection
            if selection == "private":
                message = f"--sendPrivate--{item_id}--{str}--"
            elif selection == "group":
                message = f"--sendGroup--{item_id}--{str}--"
            elif selection == "channel":
                message = f"--sendChannel--{item_id}--{str}--"
            else:
                message = str
            self.coneccion.server.sendall(message.encode("utf-8"))
            time.sleep(0.1)
            self.txtSend.clear()
            if selection == "public":
                self.mensage_entrante("<Tú> " + str + '\n')

    def createChat(self):
        if self.coneccion is None:
            self.mensage_entrante("<!!No conectado!!>\n")
            return

        dialog = CrearDialog(self, "Crear chat", "Usuario")
        if dialog.exec() == 1:
            user_2 = dialog.txtNombre.text().strip()
            if user_2 == self.coneccion.name:
                self.mensage_entrante("<!!Seleccione otro usuario!!>\n")
                return
            message = f"--chat--{self.coneccion.name}--{user_2}--"
            self.coneccion.server.sendall(message.encode("utf-8"))

    def createGroup(self):
        if self.coneccion is None:
            self.mensage_entrante("<!!No conectado!!>\n")
            return
        dialog = CrearDialog(self, "Crear grupo", "Nombre", group=True, connection=self.coneccion)
        if dialog.exec() == 1:
            name = dialog.txtNombre.text().strip()
            members = "--".join(dialog.members)
            message = f"--group--{name}--{members}--" if members else f"--group--{name}--"
            self.coneccion.server.sendall(message.encode("utf-8"))

    def createChannel(self):
        if self.coneccion is None:
            self.mensage_entrante("<!!No conectado!!>\n")
            return
        dialog = CrearDialog(self, "Crear canal", "Nombre del canal")
        if dialog.exec() == 1:
            name = dialog.txtNombre.text().strip()
            message = f"--channel--{name}--{self.coneccion.name}--"
            self.coneccion.server.sendall(message.encode("utf-8"))

    def joinChannel(self):
        if self.coneccion is None:
            self.mensage_entrante("<!!No conectado!!>\n")
            return
        dialog = CrearDialog(
            self,
            "Unir a canal",
            "Nombre del canal",
            join_channel=True,
            connection=self.coneccion,
        )
        dialog.exec()

    def salir(self):
        exit()

    def showDialog(self):
        dialog = MiDialogo(self)
        resp = dialog.exec()
        if resp == 1:
            self.coneccion = dialog.connection
            self.coneccion.signal_public_start.connect(self.txtMsgs.clear)
            self.coneccion.signal_public_message.connect(self.mensage_entrante)
            self.coneccion.signal_private_list.connect(self.loadPrivateList)
            self.coneccion.signal_private_history.connect(self.mensage_entrante)
            self.coneccion.signal_private_live.connect(self.privateMessageLive)
            self.coneccion.signal_profile_pic.connect(self.loadProfileImage)
            self.coneccion.signal_group_list.connect(self.loadGroupList)
            self.coneccion.signal_group_history.connect(self.mensage_entrante)
            self.coneccion.signal_group_live.connect(self.groupMessageLive)
            self.coneccion.signal_channel_list.connect(self.loadChannelList)
            self.coneccion.signal_channel_history.connect(self.mensage_entrante)
            self.setWindowTitle("Chat global - Conectado")
            self.perfilnombre.setText(self.coneccion.name)
            self.perfilAvatar.setText(self.coneccion.name[:1].upper())
            self.seleccionarChatGlobal()
            self.retrieveSideLists()
            QTimer.singleShot(0, lambda: self.txtSend.setFocus(Qt.OtherFocusReason))

    def mensage_entrante(self, mensaje):
        mensaje = mensaje.strip()
        if not mensaje:
            return

        sender = None
        content = mensaje
        if mensaje.startswith("<") and ">" in mensaje:
            sender, content = mensaje.split(">", 1)
            sender = sender[1:].strip()
            content = content.lstrip()

        cursor = self.txtMsgs.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if sender == "Tú":
            alignment = "right"
            background = "#86e750"
            text_color = "#000000"
        elif sender is None:
            alignment = "left"
            background = "#ffb536"
            text_color = "#000000"
        else:
            alignment = "left"
            background = "#0c71c6"
            text_color = "#ffffff"

        escaped_sender = html.escape(sender) if sender is not None else ""
        escaped_content = html.escape(content)
        sender_html = f'<div style="font-size:8pt;color:{text_color};">{escaped_sender}</div>' if sender else ""
        #POR QUÉ NO SE REDONDEAN
        bubble = (
            '<table width="70%" cellspacing="0" cellpadding="8" '
            f'style="background:{background};border-radius:5px;margin:6px 0;">'
            f'<tr><td style="color:{text_color}">{sender_html}'
            f'<div style="color:{text_color}">{escaped_content}</div></td></tr></table>'
        )
        cursor.insertHtml(
            f'<div align="{alignment}">{bubble}</div><p style="margin:2px 0;"></p>'
        )
        self.txtMsgs.verticalScrollBar().setValue(self.txtMsgs.verticalScrollBar().maximum())

    def privateMessageLive(self, chat_id, username, content):
        self.refreshPrivateList()
        selection, item_id = self.activeSelection
        if selection == "private" and str(item_id) == str(chat_id):
            sender = "Tú" if username == self.coneccion.name else username
            self.mensage_entrante(f"<{sender}> {content}\n")

    def groupMessageLive(self, group_id, username, content):
        selection, item_id = self.activeSelection
        if selection == "group" and str(item_id) == str(group_id):
            sender = "Tú" if username == self.coneccion.name else username
            self.mensage_entrante(f"<{sender}> {content}\n")

    def resolveProfilePath(self, route):
        if not route:
            return None
        if os.path.isabs(route):
            return route if os.path.isfile(route) else None
        local_path = os.path.join(os.path.dirname(__file__), route)
        return local_path if os.path.isfile(local_path) else None

    def setHeaderImage(self, route):
        path = self.resolveProfilePath(route)
        if path:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.avatar.setPixmap(
                    pixmap.scaled(
                        self.avatar.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                return
        self.setHeaderInitial("X")

    def setHeaderInitial(self, initial):
        self.avatar.clear()
        self.avatar.setText(initial)

    def loadProfileImage(self, route):
        path = self.resolveProfilePath(route)
        if path:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.perfilAvatar.clear()
                self.perfilAvatar.setPixmap(
                    pixmap.scaled(
                        self.perfilAvatar.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                return
        self.perfilAvatar.clear()
        self.perfilAvatar.setText(self.coneccion.name[:1].upper())

class CrearDialog(QDialog, Ui_CrearDialog):
    def __init__(self, parent=None, title="Crear", label="Nombre", group=False, connection=None, join_channel=False):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.labelTitulo.setText(label)
        self.txtNombre.setPlaceholderText(label)
        self.members = []
        self.connection = connection
        self.pending_member = None
        self.pending_group_name = None
        self.join_channel = join_channel
        self.pending_channel_name = None
        self.addMemberButton = None
        if group:
            self.memberInput = QLineEdit(self)
            self.memberInput.setPlaceholderText("Escribe un usuario")
            self.addMemberButton = QPushButton("Agregar miembro", self)
            self.membersList = QListWidget(self)
            self.gridLayout.removeWidget(self.buttonBox)
            self.gridLayout.addWidget(QLabel("Miembro", self), 1, 0, 1, 1)
            self.gridLayout.addWidget(self.memberInput, 1, 1, 1, 1)
            self.gridLayout.addWidget(self.addMemberButton, 2, 1, 1, 1)
            self.gridLayout.addWidget(self.membersList, 3, 0, 1, 2)
            self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
            self.addMemberButton.clicked.connect(self.requestMember)
            self.connection.signal_group_member_check.connect(self.memberCheckResult)
            self.connection.signal_group_name_check.connect(self.groupNameCheckResult)
        if join_channel: #el default es el de crear canal, con banderas activamos el de grupos o el de unirse
            self.connection.signal_channel_join_check.connect(self.channelJoinCheckResult)

    def accept(self):
        if not self.txtNombre.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El campo es obligatorio.")
            self.txtNombre.setFocus()
            return
        if self.join_channel:
            if self.pending_channel_name is not None:
                return
            self.pending_channel_name = self.txtNombre.text().strip()
            self.buttonBox.setEnabled(False)
            self.connection.server.sendall(
                f"--checkChannelJoin--{self.pending_channel_name}--".encode("utf-8")
            )
            return
        if self.pending_member is not None:
            QMessageBox.warning(self, "Validación pendiente", "Espera a que termine la validación del miembro.")
            return
        if not getattr(self, "addMemberButton", None) or not getattr(self, "membersList", None):
            super().accept()
            return
        if self.pending_group_name is not None:
            return
        self.pending_group_name = self.txtNombre.text().strip()
        self.buttonBox.setEnabled(False)
        self.connection.server.sendall(
            f"--checkGroupName--{self.pending_group_name}--".encode("utf-8")
        )

    def requestMember(self):
        username = self.memberInput.text().strip()
        if not username:
            QMessageBox.warning(self, "Campo requerido", "Escribe un usuario.")
            self.memberInput.setFocus()
            return
        if username.casefold() in {member.casefold() for member in self.members}:
            QMessageBox.warning(self, "Miembro repetido", "Ese usuario ya fue agregado.")
            return
        self.pending_member = username
        self.addMemberButton.setEnabled(False)
        self.connection.server.sendall(f"--validateGroupMember--{username}--".encode("utf-8"))

    def memberCheckResult(self, valid, username):
        if self.pending_member != username:
            return
        self.pending_member = None
        self.addMemberButton.setEnabled(True)
        if not valid:
            QMessageBox.warning(self, "Usuario no encontrado", f"No existe el usuario {username}.")
            return
        self.members.append(username)
        self.membersList.addItem(username)
        self.memberInput.clear()
        self.memberInput.setFocus()

    def channelJoinCheckResult(self, status, name):
        if self.pending_channel_name != name:
            return
        if status == "Available":
            self.connection.server.sendall(
                f"--joinChannel--{name}--".encode("utf-8")
            )
            return
        self.pending_channel_name = None
        self.buttonBox.setEnabled(True)
        if status == "Joined":
            QMessageBox.information(
                self,
                "Canal unido",
                f"Te uniste correctamente al canal {name}.",
            )
            super().accept()
            if hasattr(self.parent(), "retrieveSideLists"):
                self.parent().retrieveSideLists()
        elif status == "NotFound":
            QMessageBox.warning(
                self,
                "Canal no encontrado",
                "No existe un canal con ese nombre.",
            )
        elif status == "Owner":
            QMessageBox.warning(
                self,
                "Propietario del canal",
                "Ya eres el propietario de este canal.",
            )
        elif status == "Subscribed":
            QMessageBox.warning(
                self,
                "Ya unido",
                "Ya estas unido a este canal.",
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "No se pudo validar el canal.",
            )
        self.txtNombre.setFocus()
        self.txtNombre.selectAll()

    def groupNameCheckResult(self, available, name):
        if self.pending_group_name != name:
            return
        self.pending_group_name = None
        self.buttonBox.setEnabled(True)
        if not available:
            QMessageBox.warning(
                self,
                "Grupo existente",
                "Ya existe un grupo con ese nombre. Elige otro nombre.",
            )
            self.txtNombre.setFocus()
            self.txtNombre.selectAll()
            return
        super().accept()


class MiDialogo(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connection = None

        self.txtServer.setText(SERVER_HOST)
        self.txtPort.setText(str(SERVER_PORT))
        
        self.txtServer.setReadOnly(True)
        self.txtPort.setReadOnly(True)

    def accept(self):
        if not self.txtUser.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El usuario es obligatorio.")
            self.txtUser.setFocus()
            return

        if not self.txtPassword.text():
            QMessageBox.warning(self, "Campo requerido", "La contraseña es obligatoria.")
            self.txtPassword.setFocus()
            return

        host = self.txtServer.text()
        port = self.txtPort.text()
        user = self.txtUser.text()
        password = self.txtPassword.text()
        if not port.isnumeric():
            QMessageBox.warning(self, "Campo requerido", "El puerto debe ser numérico.")
            return

        connection = ThreadSocket(host, int(port), user, password)
        if hasattr(self.parent(), "mensage_entrante"):
            connection.signal_message.connect(self.parent().mensage_entrante)
        connection.signal_authenticated.connect(self.authentication_finished)
        connection.start()
        self.connection = connection

    def authentication_finished(self, authenticated, message):
        if authenticated:
            super().accept()
        else:
            message = message.strip().replace("<!!", "").replace("!!>", "")
            QMessageBox.warning(self, "No se pudo conectar", message)
            self.txtPassword.clear()
            self.txtPassword.setFocus()

if __name__ == "__main__":
    BUFFER_SIZE = 1024  # Usamos un número pequeño para tener una respuesta rápida
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    app = QApplication(sys.argv)
    window = MainWindow()
    dialog = MiDialogo(window)
    if dialog.exec() == 1:
        window.coneccion = dialog.connection
        window.coneccion.signal_public_start.connect(window.txtMsgs.clear)
        window.coneccion.signal_public_message.connect(window.mensage_entrante)
        window.coneccion.signal_private_list.connect(window.loadPrivateList)
        window.coneccion.signal_private_history.connect(window.mensage_entrante)
        window.coneccion.signal_private_live.connect(window.privateMessageLive)
        window.coneccion.signal_profile_pic.connect(window.loadProfileImage)
        window.coneccion.signal_group_list.connect(window.loadGroupList)
        window.coneccion.signal_group_history.connect(window.mensage_entrante)
        window.coneccion.signal_group_live.connect(window.groupMessageLive)
        window.coneccion.signal_channel_list.connect(window.loadChannelList)
        window.coneccion.signal_channel_history.connect(window.mensage_entrante)
        window.setWindowTitle("Chat global - Conectado")
        window.perfilnombre.setText(window.coneccion.name)
        window.perfilAvatar.setText(window.coneccion.name[:1].upper())
        window.seleccionarChatGlobal()
        window.retrieveSideLists()
    else:
        sys.exit(0)
    window.show()
    sys.exit(app.exec())
