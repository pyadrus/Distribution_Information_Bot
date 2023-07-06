from aiogram import types

from keyboards.greeting_keyboards import greeting_keyboards
from system.dispatcher import dp


@dp.message_handler(commands="start")
async def start(message: types.Message):
    """Обработчик команды /start"""
    greeting_post = (f"👋 Привет, {message.from_user.first_name}!\n\n"
                     f"<i>Я 🤖 бот для parsing постов с групп и каналов в вашу группу.\n\n"
                     f"Я могу помочь вам автоматически собирать посты с различных 💬 групп и каналов и "
                     f"публиковать их в вашей группе.\n\n"
                     f"Для начала мне понадобятся некоторые ⚙️ настройки. Пожалуйста, предоставьте мне "
                     f"📋 список групп и каналов, из которых вы хотели бы получать посты, а также указания по "
                     f"формату и 🗓 расписанию публикации.\n\n"
                     f"Давайте начнем!</i>\n\n")
    keyboards_greeting = greeting_keyboards()
    await message.answer(greeting_post, reply_markup=keyboards_greeting)


def start_handler():
    """Регистрируем handlers start"""
    dp.register_message_handler(start)  # Обработчик команды /start, он же пост приветствия
