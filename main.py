from aiogram import executor

from handlers.user_account_handlers import account_connection_handler
from handlers.username_handlers import register_handlers_find_out_username
from handlers.greeting_handlers import start_handler
from handlers.post_parsing_handlers import register_handlers_post_parsing
from handlers.parsing_settings_handlers import register_handlers_post_parsing_setting
from system.dispatcher import dp


def main():
    executor.start_polling(dp, skip_updates=True)
    start_handler()  # Запуск бота через /start
    account_connection_handler()  # Подключение аккаунта
    register_handlers_post_parsing_setting()  # Настройка parsing
    register_handlers_post_parsing()
    register_handlers_find_out_username()  # Узнать ID группы / канала


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        print(e)
