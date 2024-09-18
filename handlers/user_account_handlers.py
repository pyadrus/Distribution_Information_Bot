import os
import re

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.errors import FloodWait
from pyrogram.errors import PhoneCodeExpired
from pyrogram.errors import PhoneCodeInvalid
from pyrogram.errors import PhoneNumberInvalid
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import User
from aiogram.filters import StateFilter
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
    await bot.send_message(callback_query.from_user.id, connect_ac_post)
    await state.set_state(SessionCreation.ask_number)


@router.message(StateFilter(SessionCreation.ask_number))
async def get_number(message: Message, state: FSMContext):
    """Обработчик получения номера телефона от пользователя"""
    phone = message.text
    if re.match(r"\d{3}\d{3}\d{4}", phone):
        await bot.send_chat_action(message.from_user.id, types.ChatActions.TYPING)
        async with state.proxy() as data:
            client_id = str(message.from_user.id)
            session_folder = f"accounts/{message.from_user.id}"
            os.makedirs(session_folder, exist_ok=True)
            session_file = os.path.join(session_folder, f"{phone}")
            client = Client(session_file, tg_id, tg_hash)
            await client.connect()
            try:
                sent_code = await client.send_code(phone)
                data['client_id'] = client_id
                data['code_hash'] = sent_code.phone_code_hash
                data['phone'] = phone
                clients[client_id] = client
                await message.answer(f'<b>Отправьте код подтверждения в таком виде: 1-2-3-4-5\n</b>')
                await state.set_state(SessionCreation.ask_code)
            except FloodWait as e:
                await message.answer(
                    f"<b>Слишком много попыток входа, попробуйте через <code>{e.value}</code> секунд</b>")
                await client.disconnect()
                await state.clear()
            except PhoneNumberInvalid:
                await message.answer("<b>Неверный номер телефона</b>")
                await client.disconnect()
                await state.clear()
    else:
        await message.answer("<b>Неправильный формат номера телефона</b>")
        await state.set_state(SessionCreation.ask_number)


@router.message(state=SessionCreation.ask_code)
async def get_code(message: types.Message, state: FSMContext):
    """Обработчик получения кода подтверждения от пользователя"""
    await bot.send_chat_action(message.from_user.id, types.ChatActions.TYPING)
    code = message.text.replace('-', '')
    async with state.proxy() as _data:
        data = _data.as_dict()
    client_id = data['client_id']
    client = clients[client_id]
    try:
        signed_in = await client.sign_in(phone_number=data['phone'],
                                         phone_code_hash=data['code_hash'],
                                         phone_code=code)
        if isinstance(signed_in, User):
            await message.answer(f'<b>✅ <i>{signed_in.first_name}</i> добавлен</b>')
            cursor, conn = writing_account_data_to_the_database()
            # Insert the user ID and phone number into the database
            cursor.execute("""
                            INSERT INTO connected_accounts (user_id, phone_number)
                            VALUES (?, ?)
                        """, (message.from_user.id, data['phone']))

            # Commit the changes to the database
            conn.commit()

            await client.disconnect()
            clients.pop(client_id)
            await state.clear()
    except PhoneCodeInvalid:
        await message.answer('<b>Неверный код</b>')
        await state.set_state(SessionCreation.ask_code)
    except SessionPasswordNeeded:
        await message.answer('<b>Введите 2FA пароль</b>')
        await state.set_state(SessionCreation.ask_2fa)
    except PhoneCodeExpired:
        await message.answer("<b>Срок действия кода подтверждения истек</b>")
        await client.disconnect()
        clients.pop(client_id)
        await state.clear()


@router.message(state=SessionCreation.ask_2fa)
async def get_2fa(message: types.Message, state: FSMContext):
    """Обработчик получения 2FA пароля от пользователя"""
    await bot.send_chat_action(message.from_user.id, types.ChatActions.TYPING)
    async with state.proxy() as _data:
        data = _data.as_dict()
    client_id = data['client_id']
    client = clients[client_id]
    try:
        await client.connect()
    except ConnectionError:
        pass
    try:
        await client.check_password(message.text)
        await message.answer(f'<b>✅ <i>{(await client.get_me()).first_name}</i> добавлен</b>')
        cursor, conn = writing_account_data_to_the_database()
        # Insert the user ID and phone number into the database
        cursor.execute("""
                    INSERT INTO connected_accounts (user_id, phone_number)
                    VALUES (?, ?)
                """, (message.from_user.id, data['phone']))

        # Commit the changes to the database
        conn.commit()

    except BadRequest:
        await message.answer('<b>Неправильный 2FA пароль. Попробуйте ещё раз</b>')
        return
    await client.disconnect()
    clients.pop(client_id)
    await state.clear()


def account_connection_handler():
    """Обработчик запроса на подключение аккаунта"""
    dp.message.register(auth)
    dp.message.register(get_number)
    dp.message.register(get_code)
    dp.message.register(get_2fa)
