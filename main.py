import asyncio
import logging
import sys
from loguru import logger
from handlers.check_connected_accounts_handlers import register_check_connected_accounts_handlers
from handlers.user_account_handlers import account_connection_handler
from handlers.username_handlers import register_handlers_find_out_username
from handlers.greeting_handlers import start_handler
from handlers.post_parsing_handlers import register_handlers_post_parsing
from handlers.parsing_settings_handlers import register_handlers_post_parsing_setting
from system.dispatcher import dp, bot
from handlers.help_handlers import register_handlers_help

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


async def main():
    await dp.start_polling(bot)
    start_handler()  # Запуск бота через /start
    account_connection_handler()  # Подключение аккаунта
    register_handlers_post_parsing_setting()  # Настройка parsing
    register_handlers_post_parsing()
    register_handlers_find_out_username()  # Узнать ID группы / канала
    register_handlers_help()
    register_check_connected_accounts_handlers()  # Узнать подключенные аккаунты


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Ошибка: {e}")
