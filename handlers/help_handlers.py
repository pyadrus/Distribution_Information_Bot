from aiogram import types

from system.dispatcher import dp, bot


@dp.callback_query_handler(lambda c: c.data == "help_key")
async def help_handlers(callback_query: types.CallbackQuery):
    text = "Для использование бота, подключите аккаунт и вам может потребоваться ID группы и канала"
    await bot.send_message(callback_query.from_user.id, text)


def register_handlers_help():
    dp.register_message_handler(help_handlers)
