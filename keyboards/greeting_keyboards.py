from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboards():
    """Клавиатура приветствия, с выбором действий пользователя"""

    rows = [
        [
        InlineKeyboardButton(text="➕ Подключение аккаунта", callback_data="connection_new_account"),
        InlineKeyboardButton(text="⚙️ Настройка parsing", callback_data="post_parsing_settings")
         ],
        [InlineKeyboardButton(text="🔎 Узнать ID группы / канала", callback_data="find_out_username")],
        [InlineKeyboardButton(text="✔️ Проверить подключения", callback_data="check_connected_accounts")],
        [InlineKeyboardButton(text="‼️Помощь", callback_data="help_key")],
    ]
    keyboards_greeting = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboards_greeting


if __name__ == "__main__":
    greeting_keyboards()
