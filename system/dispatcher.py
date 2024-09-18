import configparser

from aiogram import Bot
from aiogram import Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
config.read("setting/config.ini")
bot_token = config.get('BOT_TOKEN', 'BOT_TOKEN')
tg_id = config.get('TG_ID', 'TG_ID')
tg_hash = config.get('TG_HASH', 'TG_HASH')

logger.info(bot_token)

bot = Bot(token=bot_token)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)
