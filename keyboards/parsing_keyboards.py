from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def parsing_keyboards():
    """Клавиатура приветствия, с выбором действий пользователя"""
    keyboards_parsing = InlineKeyboardMarkup()
    connection_parsing = InlineKeyboardButton(text="⚙️ Настройка parsing", callback_data="connection_parsing")
    rum_parsing = InlineKeyboardButton(text="Запуск parsing", callback_data="parsing_run")
    pass_parsing = InlineKeyboardButton(text="Остановить parsing", callback_data="parsing_pass")
    keyboards_parsing.row(connection_parsing, rum_parsing)
    keyboards_parsing.row(pass_parsing)
    return keyboards_parsing


if __name__ == "__main__":
    parsing_keyboards()
