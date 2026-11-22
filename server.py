import socket
import threading
import re
from database import (
    check_connection,
    get_user_id,
    get_user_profile_pic,
    get_channel_by_name,
    join_channel,
    verify_password,
    create_user,
    create_channel,
    create_chat,
    create_group,
    group_exists,
    save_public,
    get_public_messages,
    get_recent_private_chats,
    get_private_history,
    get_private_participants,
    get_user_groups,
    get_group_history,
    get_group_recipients,
    get_user_channels,
    get_channel_owner,
    user_can_read_channel,
    get_channel_recipients,
    get_channel_history,
    save_private_message,
    save_group_message,
    save_channel_message,
)

SHUTDOWN_COMMAND = "en papulandia hay un papu"
SHUTDOWN_ANNOUNCEMENT = "Anuncio: el servidor se cerrará.\n"

def profile_route(profile_pic):
    if not profile_pic:
        return ""
    profile_pic = str(profile_pic).replace("\\", "/").lstrip("/")
    return profile_pic if profile_pic.startswith("src/") else f"src/{profile_pic}"

class Cliente:
    name = ""
    password = ""
    authenticated = False
    conn = None
    addr = None


def setName(connection, name: str):
    for client in list_of_clients:
        if client.conn == connection:
            client.name = name
            break


def getName(connection) -> str:
    for client in list_of_clients:
        if client.conn == connection:
            return client.name
    return ""


def setPassword(connection, password: str):
    for client in list_of_clients:
        if client.conn == connection:
            client.password = password
            break


def getPassword(connection) -> str:
    for client in list_of_clients:
        if client.conn == connection:
            return client.password
    return ""


def setAuthenticated(connection, authenticated):
    for client in list_of_clients:
        if client.conn == connection:
            client.authenticated = authenticated
            break


def remove(connection):
    for client in list_of_clients:
        if client.conn == connection:
            list_of_clients.remove(client)
            break


def broadcast(message, connection):
    for client in list_of_clients:
        if client.conn != connection:
            try:
                client.conn.send(bytes(message, 'utf-8'))
            except:
                client.conn.close()
                remove(client)

def clientthread(conn, addr):
    conn.send(bytes(f"Bienvenido {addr}\n", 'utf-8'))
    while True:
        #try:
            message = conn.recv(BUFFER_SIZE)
            if message:
                print(f"<{addr[0]}> {message}")
                msg = message.decode('utf-8')
                # Mensajes especiales (comandos)
                combined_retrieval_commands = re.split(
                    r'(?=--retrieve(?:Public|Private|Group|Channel))',
                    msg
                )
                filtered_commands = []
                for command in combined_retrieval_commands:
                    if command.startswith('--retrieve'):
                        filtered_commands.append(command)
                #pq los retrieve siguen llegando juntitos
                combined_retrieval_commands = filtered_commands
                if len(combined_retrieval_commands) > 1:
                    user_id = get_user_id(getName(conn))
                    for command in combined_retrieval_commands:
                        command = command.strip().removesuffix('--')
                        if command == '--retrievePublic':
                            conn.sendall(b"--publicStart--\n")
                            for username, content in get_public_messages():
                                conn.sendall(f"--public--{username}--{content}--\n".encode('utf-8'))
                            conn.sendall(b"--publicEnd--\n")
                        elif command == '--retrievePrivate':
                            for chat_id, username, profile_pic in get_recent_private_chats(user_id):
                                conn.sendall(f"--privateChat--{chat_id}--{username}--{profile_route(profile_pic)}--\n".encode('utf-8'))
                        elif command == '--retrieveGroup':
                            for group_id, name in get_user_groups(user_id):
                                conn.sendall(f"--group--{group_id}--{name}--\n".encode('utf-8'))
                        elif command == '--retrieveChannel':
                            for channel_id, name in get_user_channels(user_id):
                                conn.sendall(f"--channel--{channel_id}--{name}--\n".encode('utf-8'))
                    continue
                if msg == SHUTDOWN_COMMAND:
                    broadcast(SHUTDOWN_ANNOUNCEMENT, None)
                    shutdown_server()
                    return
                elif msg.startswith('--name'):
                    setName(conn, msg.removeprefix('--name'))
                elif msg.startswith('--password'):
                    setPassword(conn, msg.removeprefix('--password'))
                    name = getName(conn)
                    password = getPassword(conn)
                    user_id = get_user_id(name)
                    if user_id is None:
                        create_user(name, password)
                        setAuthenticated(conn, True)
                        conn.sendall(b"<!!Autenticado!!>\n")
                    elif verify_password(name, password):
                        setAuthenticated(conn, True)
                        conn.sendall(b"<!!Autenticado!!>\n")
                    else:
                        conn.sendall(b"<!!Clave incorrecta!!>\n")
                        conn.close()
                        remove(conn)
                        return
                elif msg.startswith('--chat'):
                    parts = [part.strip() for part in msg[len('--chat'):].split('--') if part.strip()]
                    if len(parts) != 2:
                        conn.sendall(b"<!!Formato de chat invalido!!>\n")
                        continue

                    user_1 = parts[0]
                    user_2 = parts[1]
                    user_1_id = get_user_id(user_1)
                    user_2_id = get_user_id(user_2)
                    if user_1_id is None or user_2_id is None:
                        conn.sendall(b"<!!Usuario no encontrado!!>\n")
                        continue

                    chat_id = create_chat(user_1_id, user_2_id)
                    if chat_id is None:
                        response = f"<!!Chat ya existe!!> {user_1} - {user_2}\n"
                    else:
                        response = f"<Chat creado> {user_1} - {user_2} (id {chat_id})\n"
                    conn.sendall(response.encode('utf-8'))
                elif msg.startswith('--group'):
                    parts = [part.strip() for part in msg[len('--group'):].split('--') if part.strip()]
                    if not parts:
                        conn.sendall(b"<!!Formato de grupo invalido!!>\n")
                        continue
                    owner_id = get_user_id(getName(conn))
                    member_ids = []
                    invalid_member = None
                    for username in parts[1:]:
                        member_id = get_user_id(username)
                        if member_id is None:
                            invalid_member = username
                            break
                        member_ids.append(member_id)
                    if invalid_member is not None:
                        conn.sendall(f"<!!Usuario no encontrado: {invalid_member}!!>\n".encode('utf-8'))
                        continue
                    group_id = create_group(parts[0], owner_id, member_ids)
                    if group_id is None:
                        conn.sendall(f"<!!El grupo ya existe: {parts[0]}!!>\n".encode('utf-8'))
                    else:
                        conn.sendall(f"<Grupo creado> {parts[0]} (id {group_id})\n".encode('utf-8'))
                elif msg.startswith('--checkGroupName'):
                    parts = [part.strip() for part in msg[len('--checkGroupName'):].split('--') if part.strip()]
                    if len(parts) != 1:
                        conn.sendall(b"--groupNameInvalid----\n")
                        continue
                    name = parts[0]
                    if group_exists(name):
                        conn.sendall(f"--groupNameExists--{name}--\n".encode('utf-8'))
                    else:
                        conn.sendall(f"--groupNameAvailable--{name}--\n".encode('utf-8'))
                elif msg.startswith('--validateGroupMember'):
                    parts = [part.strip() for part in msg[len('--validateGroupMember'):].split('--') if part.strip()]
                    if len(parts) != 1:
                        conn.sendall(b"--groupMemberInvalid----\n")
                        continue
                    username = parts[0]
                    if get_user_id(username) is None:
                        conn.sendall(f"--groupMemberInvalid--{username}--\n".encode('utf-8'))
                    else:
                        conn.sendall(f"--groupMemberValid--{username}--\n".encode('utf-8'))
                elif msg.startswith('--channel'):
                    parts = [part.strip() for part in msg[len('--channel'):].split('--') if part.strip()]
                    if len(parts) != 2:
                        conn.sendall(b"<!!Formato de canal invalido!!>\n")
                        continue
                    name = parts[0]
                    owner = parts[1]
                    owner_id = get_user_id(owner)
                    if owner_id is None:
                        conn.sendall(b"<!!Usuario no encontrado!!>\n")
                        continue
                    channel_id = create_channel(name, owner_id)
                    conn.sendall(f"<Canal creado> {name} (owner {owner}, id {channel_id})\n".encode('utf-8'))
                elif msg.startswith('--checkChannelJoin'):
                    parts = [part.strip() for part in msg[len('--checkChannelJoin'):].split('--') if part.strip()]
                    if len(parts) != 1:
                        conn.sendall(b"--channelJoinInvalid----\n")
                        continue
                    name = parts[0]
                    channel = get_channel_by_name(name)
                    if channel is None:
                        conn.sendall(f"--channelJoinNotFound--{name}--\n".encode('utf-8'))
                        continue
                    channel_id, owner_id = channel
                    user_id = get_user_id(getName(conn))
                    if owner_id == user_id:
                        conn.sendall(f"--channelJoinOwner--{name}--\n".encode('utf-8'))
                    elif user_can_read_channel(channel_id, user_id):
                        conn.sendall(f"--channelJoinSubscribed--{name}--\n".encode('utf-8'))
                    else:
                        conn.sendall(f"--channelJoinAvailable--{name}--\n".encode('utf-8'))
                elif msg.startswith('--joinChannel'):
                    parts = [part.strip() for part in msg[len('--joinChannel'):].split('--') if part.strip()]
                    if len(parts) != 1:
                        conn.sendall(b"--channelJoinInvalid----\n")
                        continue
                    name = parts[0]
                    channel = get_channel_by_name(name)
                    if channel is None:
                        conn.sendall(f"--channelJoinNotFound--{name}--\n".encode('utf-8'))
                        continue
                    channel_id, owner_id = channel
                    user_id = get_user_id(getName(conn))
                    if owner_id == user_id:
                        conn.sendall(f"--channelJoinOwner--{name}--\n".encode('utf-8'))
                        continue
                    if user_can_read_channel(channel_id, user_id):
                        conn.sendall(f"--channelJoinSubscribed--{name}--\n".encode('utf-8'))
                        continue
                    if join_channel(channel_id, user_id):
                        conn.sendall(f"--channelJoined--{name}--\n".encode('utf-8'))
                    else:
                        conn.sendall(f"--channelJoinSubscribed--{name}--\n".encode('utf-8'))
                elif msg.startswith('--retrievePublic'):
                    conn.sendall(b"--publicStart--\n")
                    for username, content in get_public_messages():
                        conn.sendall(f"--public--{username}--{content}--\n".encode('utf-8'))
                    conn.sendall(b"--publicEnd--\n")
                elif msg.startswith('--getProfile'):
                    profile_pic = get_user_profile_pic(getName(conn))
                    conn.sendall(f"--profile--{profile_route(profile_pic)}--\n".encode('utf-8'))
                elif msg.startswith('--retrievePrivate'):
                    parts = [part.strip() for part in msg[len('--retrievePrivate'):].split('--') if part.strip()]
                    if not parts:
                        user_id = get_user_id(getName(conn))
                        for chat_id, username, profile_pic in get_recent_private_chats(user_id):
                            conn.sendall(f"--privateChat--{chat_id}--{username}--{profile_route(profile_pic)}--\n".encode('utf-8'))
                    else:
                        if not parts[0].isdigit():
                            continue
                        chat_id = int(parts[0])
                        for username, content in get_private_history(chat_id):
                            conn.sendall(f"--privateMessage--{username}--{content}--\n".encode('utf-8'))
                elif msg.startswith('--retrieveGroup'):
                    parts = [part.strip() for part in msg[len('--retrieveGroup'):].split('--') if part.strip()]
                    if not parts:
                        user_id = get_user_id(getName(conn))
                        for group_id, name in get_user_groups(user_id):
                            conn.sendall(f"--group--{group_id}--{name}--\n".encode('utf-8'))
                    else:
                        if not parts[0].isdigit():
                            continue
                        group_id = int(parts[0])
                        for username, content in get_group_history(group_id):
                            conn.sendall(f"--groupMessage--{username}--{content}--\n".encode('utf-8'))
                elif msg.startswith('--retrieveChannel'):
                    parts = [part.strip() for part in msg[len('--retrieveChannel'):].split('--') if part.strip()]
                    if not parts:
                        user_id = get_user_id(getName(conn))
                        for channel_id, name in get_user_channels(user_id):
                            conn.sendall(f"--channel--{channel_id}--{name}--\n".encode('utf-8'))
                    else:
                        if not parts[0].isdigit():
                            continue
                        channel_id = int(parts[0])
                        user_id = get_user_id(getName(conn))
                        if user_can_read_channel(channel_id, user_id):
                            for username, content in get_channel_history(channel_id):
                                conn.sendall(f"--channelMessage--{username}--{content}--\n".encode('utf-8'))
                        else:
                            conn.sendall(b"<!!No estas suscrito a este canal!!>\n")
                elif msg.startswith('--sendPrivate'):
                    parts = [part.strip() for part in msg[len('--sendPrivate'):].split('--') if part.strip()]
                    if len(parts) == 2 and parts[0].isdigit():
                        chat_id = int(parts[0])
                        sender = get_user_id(getName(conn))
                        save_private_message(chat_id, sender, parts[1])
                        participants = get_private_participants(chat_id)
                        if participants is not None:
                            live_message = f"--privateMessage--{chat_id}--{getName(conn)}--{parts[1]}--\n"
                            for client in list_of_clients:
                                if client.name in participants:
                                    client.conn.sendall(live_message.encode('utf-8'))
                elif msg.startswith('--sendGroup'):
                    parts = [part.strip() for part in msg[len('--sendGroup'):].split('--') if part.strip()]
                    if len(parts) == 2 and parts[0].isdigit():
                        group_id = int(parts[0])
                        sender = get_user_id(getName(conn))
                        save_group_message(group_id, sender, parts[1])
                        live_message = f"--groupMessage--{group_id}--{getName(conn)}--{parts[1]}--\n".encode('utf-8')
                        recipients = get_group_recipients(group_id)
                        for client in list_of_clients:
                            if client.name in recipients:
                                client.conn.sendall(live_message)
                elif msg.startswith('--sendChannel'):
                    parts = [part.strip() for part in msg[len('--sendChannel'):].split('--') if part.strip()]
                    if len(parts) == 2 and parts[0].isdigit():
                        channel_id = int(parts[0])
                        sender = get_user_id(getName(conn))
                        if get_channel_owner(channel_id) != sender:
                            conn.sendall(b"<!!Solo el propietario puede enviar mensajes al canal!!>\n")
                            continue
                        save_channel_message(channel_id, sender, parts[1])
                        live_message = f"--channelMessage--{getName(conn)}--{parts[1]}--\n".encode('utf-8')
                        recipients = get_channel_recipients(channel_id)
                        for client in list_of_clients:
                            if client.name in recipients:
                                client.conn.sendall(live_message)
                else:
                    sender = get_user_id(getName(conn))
                    if sender is None:
                        created_user = create_user(getName(conn),getPassword(conn))
                        print(f"Usuario {created_user} creado")
                        sender = get_user_id(getName(conn))
                    save_public(sender, msg)
                    # Reenviamos el mensaje recibido a todos los demás clientes.
                    message_to_send = f"<{getName(conn)}> {message.decode('utf-8')}\n"
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        #except:
        #    break

def shutdown_server():
    shutdown_requested.set()
    broadcast_client_connections = list(list_of_clients)
    for client in broadcast_client_connections:
        try:
            client.conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            client.conn.close()
    list_of_clients.clear()
    server.close()

if __name__ == "__main__":
    try:
        print(f"{check_connection()}")
    except Exception as error:
        print(f"No se pudo conectar a la base de datos: {error}")
        raise SystemExit(1)
    #host = socket.gethostname()  # Esta función nos da el nombre de la máquina
    host = "0.0.0.0"
    port = 80
    BUFFER_SIZE = 1024  # Usamos un número pequeño para tener una respuesta rápida
    # Creamos un socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(100)  # Escuchamos hasta 100 clientes
    list_of_clients = []  # Lista de clientes conectados
    shutdown_requested = threading.Event()
    print(f"Escuchando conexiones en: {(host, port)}")
    try:
        while True:
            conn, addr = server.accept()
            nuevo_cliente = Cliente()
            nuevo_cliente.conn = conn
            nuevo_cliente.addr = addr
            nuevo_cliente.authenticated = False
            #list_of_clients.append(conn)  # Agregamos a la lista de clientes
            list_of_clients.append(nuevo_cliente)  # Agregamos a la lista de clientes
            print(f"Cliente conectado: {addr}")
            # Creamos y ejecutamos el hilo para atender al cliente
            threading.Thread(target=clientthread, args=(conn, addr)).start()
    except OSError:
        if not shutdown_requested.is_set():
            raise
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        for client in list_of_clients:
            client.conn.close()
        server.close()   
    print("Conexión terminada.")
