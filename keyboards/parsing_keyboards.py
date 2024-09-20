from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def parsing_keyboards():
    """Клавиатура приветствия, с выбором действий пользователя"""
    rows = [
        [
            InlineKeyboardButton(text="⚙️ Настройка parsing", callback_data="connection_parsing"),
            InlineKeyboardButton(text="Запуск parsing", callback_data="parsing_run")
        ],

        [InlineKeyboardButton(text="Запись группы для публикации", callback_data="group_entry_for_publication")],

        [InlineKeyboardButton(text="Остановить parsing", callback_data="parsing_pass")],
        [InlineKeyboardButton(text="В начальное меню", callback_data="start_menu")],
    ]
    keyboards_greeting = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboards_greeting


if __name__ == "__main__":
    parsing_keyboards()
