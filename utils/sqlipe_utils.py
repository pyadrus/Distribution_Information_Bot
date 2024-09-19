import sqlite3


def we_get_the_data_of_the_connected_accounts():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM connected_accounts")
    row = cursor.fetchone()
    return row


def writing_channel_group_ids_to_database():
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS parsing_groups (account_id, group_id_pars, group_id_post)""")
    conn.commit()
    return cursor, conn


def writing_account_data_to_the_database():
    # Create a connection to the database
    conn = sqlite3.connect('setting/database.db')
    # Create a cursor object
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS connected_accounts (user_id INTEGER PRIMARY KEY, phone_number TEXT)""")
    return cursor, conn


def read_parsing_groups():
    """Считывание данных групп и каналов с базы данных"""
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parsing_groups")
    rows = cursor.fetchall()
    conn.close()
    return rows


def checking_connected_accounts(user_id) -> list:
    """
    Проверка подключенных аккаунтов базе данных
    :param user_id: id пользователя telegram
    :return: список подключенных аккаунтов пользователя telegram
    """
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    # Получить подключенные учетные записи для определенного user_id
    cursor.execute("SELECT phone_number FROM connected_accounts WHERE user_id = ?", (user_id,))
    # Получить все строки, возвращенные запросом
    rows = cursor.fetchall()

    return rows

def write_data_into_database_account_id_and_group_id_from_which_you_want_parse_posts(message, group_ids_str):
    """
    Записываем данные в базу данных ID аккаунта и ID группы с которого нужно parsing посты
    :param message: сообщение, которое нужно parsing
    :param group_ids_str: строка с ID групп
    """
    cursor, conn = writing_channel_group_ids_to_database()
    cursor.execute("INSERT INTO parsing_groups (account_id, group_id_pars) VALUES (?, ?)",
                   (message.from_user.id, group_ids_str))
    conn.commit()

def record_id_group_to_which_posts_should_be_published(group_id_post, message):
    """Запись ID группы в которую нужно публиковать посты"""
    cursor, conn = writing_channel_group_ids_to_database()
    cursor.execute("UPDATE parsing_groups SET group_id_post = ? WHERE account_id = ?",
                   (group_id_post, message.from_user.id))
    conn.commit()

def recording_phone_number_account_that_user_connected(message, data):
    # Вставляем данные пользователя в базу данных
    cursor, conn = writing_account_data_to_the_database()
    cursor.execute("""
                            INSERT INTO connected_accounts (user_id, phone_number)
                            VALUES (?, ?)
                        """, (message.from_user.id, data['phone']))
    conn.commit()  # Подтверждаем изменения в базе данных

def writing_phone_number_to_a_database(message, data):
    cursor, conn = writing_account_data_to_the_database()
    # Проверяем наличие записи перед вставкой
    cursor.execute("SELECT COUNT(*) FROM connected_accounts WHERE user_id = ?", (message.from_user.id,))
    exists = cursor.fetchone()[0]
    return exists

def checking_your_connected_account(message, data):
    cursor, conn = writing_account_data_to_the_database()
    cursor.execute("""
                            INSERT INTO connected_accounts (user_id, phone_number)
                            VALUES (?, ?)
                        """, (message.from_user.id, data['phone']))
    conn.commit()  # Подтверждаем изменения в базе данных


if __name__ == "__main__":
    read_parsing_groups()
    writing_channel_group_ids_to_database()
    writing_channel_group_ids_to_database()
    we_get_the_data_of_the_connected_accounts()
