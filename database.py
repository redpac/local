import os
import random
import mssql_python

#ya sé que se ve fea aquí, pero pa pronto
def random_number():
    return random.randint(1, 10)


def check_connection():
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return "ya ta conectao"


def get_user_id(username):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM jesus.banios.users WHERE username = ?",(username,))
            row = cursor.fetchone()
            return row[0] if row else None


def get_user_profile_pic(username):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT profile_pic FROM jesus.banios.users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            return row[0] if row else None


def verify_password(username, password):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM jesus.banios.users WHERE username = ? AND password = ?",
                (username, password)
            )
            return cursor.fetchone() is not None


def create_user(username, password):
    profile_pic = f"{random_number()}.jpg"
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO jesus.banios.users
                (username, password, profile_pic)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?)
            """,(username,password,profile_pic))
            row = cursor.fetchone()
            return row[0] if row else None


def create_chat(user_1, user_2):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id
                FROM jesus.banios.[private-chats]
                WHERE (user_1 = ? AND user_2 = ?)
                   OR (user_1 = ? AND user_2 = ?)
                """,(user_1, user_2, user_2, user_1))
            if cursor.fetchone() is not None:
                return None
            cursor.execute("""
                INSERT INTO jesus.banios.[private-chats]
                    (user_1,user_2)
                OUTPUT INSERTED.id
                VALUES (?, ?)
                """,(user_1,user_2))
            row = cursor.fetchone()
            return row[0] if row else None


def create_channel(name, owner_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jesus.banios.channels
                    (name, owner_id)
                OUTPUT INSERTED.id
                VALUES (?, ?)
                """,(name, owner_id))
            row = cursor.fetchone()
            return row[0] if row else None


def create_group(name, owner_id, member_ids):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1
                FROM jesus.banios.groups
                WHERE name = ?
                """,(name,))
            if cursor.fetchone() is not None:
                return None
            cursor.execute("""
                INSERT INTO jesus.banios.groups
                    (name)
                OUTPUT INSERTED.id
                VALUES (?)
                """,(name,))
            row = cursor.fetchone()
            if not row:
                return None
            group_id = row[0]
            for user_id in set(member_ids) | {owner_id}:
                cursor.execute("""
                    INSERT INTO jesus.banios.groups_users
                        (group_id, user_id)
                    VALUES (?, ?)
                    """,(group_id, user_id))
            return group_id


def group_exists(name):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1
                FROM jesus.banios.groups
                WHERE name = ?
                """,(name,))
            return cursor.fetchone() is not None


def save_public(sender_id, content):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jesus.banios.[public]
                    (sender, content)
                OUTPUT INSERTED.id
                VALUES (?, ?)
                """,(sender_id, content))
            row = cursor.fetchone()
            return row[0] if row else None


def get_public_messages():
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.username, p.content
                FROM jesus.banios.[public] AS p
                JOIN jesus.banios.users AS u ON u.id = p.sender
                ORDER BY p.id
                """)
            return cursor.fetchall()


def get_recent_private_chats(user_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id,
                    CASE WHEN c.user_1 = ? THEN u2.username ELSE u1.username END,
                    CASE WHEN c.user_1 = ? THEN u2.profile_pic ELSE u1.profile_pic END
                FROM jesus.banios.[private-chats] AS c
                JOIN jesus.banios.users AS u1 ON u1.id = c.user_1
                JOIN jesus.banios.users AS u2 ON u2.id = c.user_2
                WHERE c.user_1 = ? OR c.user_2 = ?
                ORDER BY c.id DESC
                """,(user_id, user_id, user_id, user_id))
            return cursor.fetchall()


def get_private_history(chat_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.username, m.content
                FROM jesus.banios.private_messages AS m
                JOIN jesus.banios.users AS u ON u.id = m.sender_id
                WHERE m.chat_id = ?
                ORDER BY m.id
                """,(chat_id,))
            return cursor.fetchall()


def get_private_participants(chat_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u1.username, u2.username
                FROM jesus.banios.[private-chats] AS c
                JOIN jesus.banios.users AS u1 ON u1.id = c.user_1
                JOIN jesus.banios.users AS u2 ON u2.id = c.user_2
                WHERE c.id = ?
                """,(chat_id,))
            row = cursor.fetchone()
            return (row[0], row[1]) if row else None


def get_user_groups(user_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.id, g.name
                FROM jesus.banios.groups AS g
                JOIN jesus.banios.groups_users AS gu ON gu.group_id = g.id
                WHERE gu.user_id = ?
                """,(user_id,))
            return cursor.fetchall()


def get_group_history(group_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.username, m.content
                FROM jesus.banios.group_messages AS m
                JOIN jesus.banios.users AS u ON u.id = m.sender_id
                WHERE m.group_id = ?
                ORDER BY m.id
                """,(group_id,))
            return cursor.fetchall()


def get_group_recipients(group_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT u.username
                    FROM jesus.banios.users AS u
                    JOIN jesus.banios.groups_users AS gu ON gu.user_id = u.id
                    WHERE gu.group_id = ?
                    """,(group_id,))
                return {row[0] for row in cursor.fetchall()}


def get_user_channels(user_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT c.id, c.name
                FROM jesus.banios.channels AS c
                LEFT JOIN jesus.banios.channels_users AS cu ON cu.channel_id = c.id
                WHERE cu.user_id = ? OR c.owner_id = ?
                """,(user_id, user_id))
            return cursor.fetchall()


def get_channel_owner(channel_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT owner_id
                FROM jesus.banios.channels
                WHERE id = ?
                """,(channel_id,))
            row = cursor.fetchone()
            return row[0] if row else None


def get_channel_by_name(name):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, owner_id
                FROM jesus.banios.channels
                WHERE name = ?
                """,(name,))
            row = cursor.fetchone()
            return (row[0], row[1]) if row else None


def join_channel(channel_id, user_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1
                FROM jesus.banios.channels_users
                WHERE channel_id = ? AND user_id = ?
                """,(channel_id, user_id))
            if cursor.fetchone() is not None:
                return False
            cursor.execute("""
                INSERT INTO jesus.banios.channels_users
                    (channel_id, user_id)
                VALUES (?, ?)
                """,(channel_id, user_id))
            return True


def user_can_read_channel(channel_id, user_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1
                FROM jesus.banios.channels AS c
                LEFT JOIN jesus.banios.channels_users AS cu
                    ON cu.channel_id = c.id AND cu.user_id = ?
                WHERE c.id = ? AND (c.owner_id = ? OR cu.user_id IS NOT NULL)
                """,(user_id, channel_id, user_id))
            return cursor.fetchone() is not None


def get_channel_recipients(channel_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.username
                FROM jesus.banios.users AS u
                JOIN jesus.banios.channels_users AS cu ON cu.user_id = u.id
                WHERE cu.channel_id = ?
                UNION
                SELECT u.username
                FROM jesus.banios.users AS u
                JOIN jesus.banios.channels AS c ON c.owner_id = u.id
                WHERE c.id = ?
                """,(channel_id, channel_id))
            return {row[0] for row in cursor.fetchall()}


def get_channel_history(channel_id):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.username, m.content
                FROM jesus.banios.channel_messages AS m
                JOIN jesus.banios.users AS u ON u.id = m.sender_id
                WHERE m.channel_id = ?
                ORDER BY m.id
                """,(channel_id,))
            return cursor.fetchall()


def save_private_message(chat_id, sender_id, content):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jesus.banios.private_messages
                    (chat_id, sender_id, content)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?)
                """,(chat_id, sender_id, content))
            row = cursor.fetchone()
            return row[0] if row else None


def save_group_message(group_id, sender_id, content):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jesus.banios.group_messages
                    (group_id, sender_id, content)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?)
                """,(group_id, sender_id, content))
            row = cursor.fetchone()
            return row[0] if row else None


def save_channel_message(channel_id, sender_id, content):
    with mssql_python.connect(os.environ["MSSQL_CONNECTION_STRING"], timeout=30) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jesus.banios.channel_messages
                    (channel_id, sender_id, content)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?)
                """,(channel_id, sender_id, content))
            row = cursor.fetchone()
            return row[0] if row else None

