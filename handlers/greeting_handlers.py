from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.greeting_keyboards import greeting_keyboards
from messages.greeting_post_massages import greeting_post
from system.dispatcher import dp


@dp.message(CommandStart())
async def start(message: Message):
    """Обработчик команды /start"""
    await message.answer(greeting_post, reply_markup=greeting_keyboards(), parse_mode="HTML")


def start_handler():
    """Регистрируем handlers start"""
    dp.message.register(start)# Обработчик команды /start, он же пост приветствия
