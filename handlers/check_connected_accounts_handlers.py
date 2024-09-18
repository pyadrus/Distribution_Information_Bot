import sqlite3

from aiogram import types, F

from system.dispatcher import bot, dp
from system.dispatcher import router


@router.callback_query(F.data == "check_connected_accounts")
async def check_connected_accounts_handlers(callback_query: types.CallbackQuery):
    """Вывод списка подключенных аккаунтов"""
    user_id = callback_query.from_user.id  # Получите конкретный user_id из callback_query
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    # Получить подключенные учетные записи для определенного user_id
    cursor.execute("SELECT phone_number FROM connected_accounts WHERE user_id = ?", (user_id,))
    # Получить все строки, возвращенные запросом
    rows = cursor.fetchall()
    # Создайте текстовое сообщение с подключенными учетными записями
    text = "✅ Подключенные аккаунты:\n\n"
    for row in rows:
        phone_number = row[0]  # Предполагая, что phone_number хранится в первом столбце
        text += f"📱 {phone_number}\n"

    await bot.send_message(callback_query.from_user.id, text)


def register_check_connected_accounts_handlers():
    dp.register_message_handler(check_connected_accounts_handlers)
