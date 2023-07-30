from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def greeting_keyboards():
    """Клавиатура приветствия, с выбором действий пользователя"""
    keyboards_greeting = InlineKeyboardMarkup()
    connection_new_account = InlineKeyboardButton(text="➕ Подключение аккаунта", callback_data="connection_new_account")
    post_parsing_settings = InlineKeyboardButton(text="⚙️ Настройка parsing", callback_data="post_parsing_settings")
    find_out_username_keyboard = InlineKeyboardButton(text="🔎 Узнать ID группы / канала", callback_data="find_out_username")
    check_connected_accounts = InlineKeyboardButton(text="✔️ Проверить подключения", callback_data="check_connected_accounts")
    help_keyboards = InlineKeyboardButton(text="‼️Помощь", callback_data="help_key")
    keyboards_greeting.row(connection_new_account, post_parsing_settings)
    keyboards_greeting.row(find_out_username_keyboard)
    keyboards_greeting.row(check_connected_accounts)
    keyboards_greeting.row(help_keyboards)
    return keyboards_greeting


if __name__ == "__main__":
    greeting_keyboards()
