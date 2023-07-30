from aiogram import types

from keyboards.greeting_keyboards import greeting_keyboards
from messages.greeting_post_massages import greeting_post
from system.dispatcher import dp


@dp.message_handler(commands="start")
async def start(message: types.Message):
    """Обработчик команды /start"""
    keyboards_greeting = greeting_keyboards()
    await message.answer(greeting_post, reply_markup=keyboards_greeting)


def start_handler():
    """Регистрируем handlers start"""
    dp.register_message_handler(start)  # Обработчик команды /start, он же пост приветствия
