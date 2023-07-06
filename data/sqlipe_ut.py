import sqlite3


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
