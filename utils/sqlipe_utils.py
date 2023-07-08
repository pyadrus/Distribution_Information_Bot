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


if __name__ == "__main__":
    read_parsing_groups()
    writing_channel_group_ids_to_database()
    writing_channel_group_ids_to_database()
    we_get_the_data_of_the_connected_accounts()
