import os
import re

from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger
from telethon import TelegramClient
from telethon.errors import (SessionPasswordNeededError)

from system.dispatcher import dp, bot, tg_id, tg_hash
from system.dispatcher import router
from utils.sqlipe_utils import writing_account_data_to_the_database

# Словарь для хранения экземпляров Pyrogram Client для каждого пользователя
clients = {}


class SessionCreation(StatesGroup):
    """Определение StatesGroup для управления ходом разговора"""
    ask_number = State()
    ask_code = State()
    ask_2fa = State()


@router.callback_query(F.data == "connection_new_account")
async def auth(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    connect_ac_post = ("<b>Напишите номер 📱 телефона в формате 79999999999</b>\n\n"
                       "Для возврата нажмите на /start")
    await bot.send_message(callback_query.from_user.id, connect_ac_post, parse_mode="HTML")
    await state.set_state(SessionCreation.ask_number)


@router.message(StateFilter(SessionCreation.ask_number))
async def get_number(message: Message, state: FSMContext):
    """Обработчик получения номера телефона от пользователя"""
    phone = message.text
    # Проверка формата номера телефона
    if re.match(r"\d{3}\d{3}\d{4}", phone):
        await bot.send_chat_action(message.from_user.id, action="typing")

        # Создаем папку для хранения сессии
        client_id = str(message.from_user.id)
        session_folder = f"accounts/{message.from_user.id}"
        os.makedirs(session_folder, exist_ok=True)
        session_file = os.path.join(session_folder, f"{phone}")

        client = TelegramClient(session_file, api_id=tg_id, api_hash=tg_hash,
                                system_version="4.16.30-vxCUSTOM")
        await client.connect()
        # try:
        # Проверяем авторизацию пользователя
        if not await client.is_user_authorized():
            logger.info("Пользователь не авторизован")
            # Отправляем код подтверждения
            sent_code = await client.send_code_request(phone)
            # Сохраняем данные в состоянии FSM
            await state.update_data(
                client_id=client_id,
                code_hash=sent_code.phone_code_hash,
                phone=phone
            )
            clients[client_id] = client
            # Сообщаем пользователю об отправке кода и просим ввести его
            await message.answer(f'<b>Отправьте код подтверждения в таком виде: 1-2-3-4-5\n</b>')
            await state.set_state(SessionCreation.ask_code)

    else:
        await message.answer("<b>Неправильный формат номера телефона</b>")
        await state.set_state(SessionCreation.ask_number)


@router.message(StateFilter(SessionCreation.ask_code))
async def get_code(message: Message, state: FSMContext):
    """Обработчик получения кода подтверждения от пользователя"""

    code = message.text.replace('-', '')
    data = await state.get_data()
    client_id = data['client_id']
    client = clients[client_id]

    try:
        # Убираем параметр `phone_code` и используем `sign_in(phone, code)`
        signed_in = await client.sign_in(
            phone=data['phone'],
            code=code
        )

        user = await client.get_me()
        await message.answer(f'<b>✅ <i>{user.first_name}</i> добавлен</b>')

        cursor, conn = writing_account_data_to_the_database()

        # Вставляем данные пользователя в базу данных
        cursor.execute("""
                        INSERT INTO connected_accounts (user_id, phone_number)
                        VALUES (?, ?)
                    """, (message.from_user.id, data['phone']))
        conn.commit()  # Подтверждаем изменения в базе данных

        await client.disconnect()
        clients.pop(client_id)
        await state.clear()

    except SessionPasswordNeededError:
        await message.answer('<b>Введите 2FA пароль</b>')
        await state.set_state(SessionCreation.ask_2fa)



@router.message(StateFilter(SessionCreation.ask_2fa))
async def get_2fa(message: Message, state: FSMContext):
    """Обработчик получения 2FA пароля от пользователя"""

    await bot.send_chat_action(message.chat.id, action="typing")  # Отправляем действие "typing"
    data = await state.get_data()

    client_id = data['client_id']
    client = clients.get(client_id)

    try:
        await client.connect()
    except ConnectionError:
        await message.answer("<b>Ошибка соединения</b>")
        return

    try:
        # Используем `sign_in` с паролем 2FA
        await client.sign_in(password=message.text)

        user = await client.get_me()
        await message.answer(f'<b>✅ <i>{user.first_name}</i> добавлен</b>')

        cursor, conn = writing_account_data_to_the_database()

        # Проверяем наличие записи перед вставкой
        cursor.execute("SELECT COUNT(*) FROM connected_accounts WHERE user_id = ?", (message.from_user.id,))
        exists = cursor.fetchone()[0]

        if not exists:
            cursor.execute("""
                            INSERT INTO connected_accounts (user_id, phone_number)
                            VALUES (?, ?)
                        """, (message.from_user.id, data['phone']))
            conn.commit()  # Подтверждаем изменения в базе данных
        else:
            await message.answer("<b>Этот аккаунт уже подключен</b>")

        await client.disconnect()
        clients.pop(client_id)
        await state.clear()

    except Exception as e:
        await message.answer(f"<b>Ошибка: {str(e)}</b>")
        await client.disconnect()
        clients.pop(client_id)
        await state.clear()




def account_connection_handler():
    """Обработчик запроса на подключение аккаунта"""
    dp.message.register(auth)
    dp.message.register(get_number)
    dp.message.register(get_code)
    dp.message.register(get_2fa)
