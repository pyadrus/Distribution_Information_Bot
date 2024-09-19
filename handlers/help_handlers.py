from aiogram import types, F

from system.dispatcher import dp, bot
from system.dispatcher import router


@router.callback_query(F.data == "help_key")
async def help_handlers(callback_query: types.CallbackQuery):
    """Помощь пользователю"""
    text = "Для использование 🤖 бота, ➕ подключите аккаунт и вам может потребоваться ID группы и канала"
    await bot.send_message(callback_query.from_user.id, text)


def register_handlers_help():
    dp.message.register(help_handlers)
