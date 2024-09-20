from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.greeting_keyboards import greeting_keyboards
from messages.greeting_post_massages import greeting_post
from system.dispatcher import bot, dp
from system.dispatcher import router


@dp.message(CommandStart())
async def start(message: Message):
    """Обработчик команды /start"""
    await message.answer(greeting_post, reply_markup=greeting_keyboards(), parse_mode="HTML")


@router.callback_query(F.data == "start_menu")
async def start_menu_handlers(callback_query: types.CallbackQuery):
    """Помощь пользователю"""
    await bot.send_message(callback_query.from_user.id, greeting_post, reply_markup=greeting_keyboards(),
                           parse_mode="HTML")


def start_handler():
    """Регистрируем handlers start"""
    dp.message.register(start)  # Обработчик команды /start, он же пост приветствия
    dp.message.register(start_menu_handlers)  # Обработчик команды /start, он же пост приветствия
