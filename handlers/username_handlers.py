from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from pyrogram import Client

from system.dispatcher import dp, bot, tg_id, tg_hash
from system.dispatcher import router
from utils.sqlipe_utils import we_get_the_data_of_the_connected_accounts


class FindOutUsername(StatesGroup):
    """Создание машины состояний для обработки сообщений"""
    find_out = State()


@router.callback_query(F.data == "find_out_username")
async def find_out_username(callback_query: types.CallbackQuery, state: FSMContext):
    text = "Введите username в виде @username группы или канала, чтобы узнать ID"
    await bot.send_message(callback_query.from_user.id, text)
    await state.set_state(FindOutUsername.find_out)


@router.message(FindOutUsername.find_out)
async def find_out_username(message: Message, state: FSMContext):
    username_group = message.text
    row = we_get_the_data_of_the_connected_accounts()
    if row:
        app = Client(f"accounts/{row[0]}/{row[1]}", api_id=tg_id, api_hash=tg_hash)
        await app.connect()
        try:
            result = await app.resolve_peer(username_group)
            chat_id = result.channel_id
            await message.answer(f"ID группы / канала {username_group}:  <code>-{chat_id}</code>")
            await app.disconnect()
        except Exception as e:
            await message.answer(f"Error: {e}")
            await app.disconnect()


def register_handlers_find_out_username():
    dp.message.register(find_out_username)
