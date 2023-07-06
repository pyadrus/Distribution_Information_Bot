
from aiogram import executor

from handlers.account_connection import account_connection_handler
from handlers.greeting import start_handler
from handlers.post_parsing import register_handlers_post_parsing
from handlers.post_parsing_settings import register_handlers_post_parsing_setting
from system.dispatcher import dp


def main():
    executor.start_polling(dp, skip_updates=True)
    start_handler()
    account_connection_handler()
    register_handlers_post_parsing_setting()
    register_handlers_post_parsing()


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        print(e)
