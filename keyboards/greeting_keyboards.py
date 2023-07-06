from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def greeting_keyboards():
    """Клавиатура приветствия, с выбором действий пользователя"""
    keyboards_greeting = InlineKeyboardMarkup()
    connection_new_account = InlineKeyboardButton(text="➕ Подключение аккаунта", callback_data="connection_new_account")
    post_parsing_settings = InlineKeyboardButton(text="⚙️ Настройка parsing", callback_data="post_parsing_settings")
    find_out_username_keyboard = InlineKeyboardButton(text="🔎 Узнать ID группы / канала", callback_data="find_out_username")
    keyboards_greeting.row(connection_new_account, post_parsing_settings)
    keyboards_greeting.row(find_out_username_keyboard)
    return keyboards_greeting


if __name__ == "__main__":
    greeting_keyboards()
