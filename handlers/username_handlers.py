from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from telethon import TelegramClient, errors
from loguru import logger

from keyboards.greeting_keyboards import keyboard_return_start_menu
from system.dispatcher import dp, bot, tg_id, tg_hash
from system.dispatcher import router
from utils.sqlipe_utils import we_get_the_data_of_the_connected_accounts


class FindOutUsername(StatesGroup):
    """Создание машины состояний для обработки сообщений"""
    find_out = State()


@router.callback_query(F.data == "find_out_username")
async def find_out_username_prompt(callback_query: types.CallbackQuery, state: FSMContext):
    text = "Введите username в виде @username группы или канала, чтобы узнать ID"
    await bot.send_message(callback_query.from_user.id, text, parse_mode="HTML",
                           reply_markup=keyboard_return_start_menu())
    await state.set_state(FindOutUsername.find_out)


@router.message(FindOutUsername.find_out)
async def process_find_out_username(message: Message, state: FSMContext):
    username_group = message.text.strip()

    row = we_get_the_data_of_the_connected_accounts()
    logger.info(row)
    if row:
        logger.info(row[1])
        client = TelegramClient(f"accounts/{message.from_user.id}/{row[1]}", api_id=tg_id, api_hash=tg_hash,
                                system_version="4.16.30-vxCUSTOM")
        logger.info(message.from_user.id)
        await client.connect()

        try:
            entity = await client.get_entity(username_group)

            # Проверяем, является ли это каналом или группой
            if hasattr(entity, 'id') and hasattr(entity, 'megagroup'):
                chat_id = entity.id
                await message.answer(f"ID группы / канала {username_group}: <code>{chat_id}</code>",
                                     parse_mode="HTML", reply_markup=keyboard_return_start_menu())
            else:
                await message.answer(f"Не удалось найти ID для {username_group}. Это не группа или канал.",
                                     parse_mode="HTML", reply_markup=keyboard_return_start_menu())
        except errors.UsernameInvalidError:
            await message.answer("Неправильный username. Попробуйте снова.", parse_mode="HTML",
                                 reply_markup=keyboard_return_start_menu())
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}", parse_mode="HTML",
                                 reply_markup=keyboard_return_start_menu())
        finally:
            await client.disconnect()
            await state.clear()


def register_handlers_find_out_username():
    dp.message.register(process_find_out_username, FindOutUsername.find_out)
