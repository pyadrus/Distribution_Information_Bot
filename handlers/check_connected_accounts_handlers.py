from aiogram import types, F

from system.dispatcher import bot, dp
from system.dispatcher import router
from utils.sqlipe_utils import checking_connected_accounts


@router.callback_query(F.data == "check_connected_accounts")
async def check_connected_accounts_handlers(callback_query: types.CallbackQuery):
    """Вывод списка подключенных аккаунтов"""
    user_id = callback_query.from_user.id  # Получите конкретный user_id из callback_query
    rows = checking_connected_accounts(user_id)
    # Создайте текстовое сообщение с подключенными учетными записями
    text = "✅ Подключенные аккаунты:\n\n"
    for row in rows:
        phone_number = row[0]  # Предполагая, что phone_number хранится в первом столбце
        text += f"📱 {phone_number}\n"
    await bot.send_message(callback_query.from_user.id, text)


def register_check_connected_accounts_handlers():
    dp.message.register(check_connected_accounts_handlers)
