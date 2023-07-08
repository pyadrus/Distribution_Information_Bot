import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.parsing_keyboards import parsing_keyboards
from system.dispatcher import dp, bot
from utils.sqlipe_utils import writing_channel_group_ids_to_database


@dp.callback_query_handler(lambda c: c.data == "post_parsing_settings")
async def parsing_parsing(callback_query: types.CallbackQuery):
    parsing_post = "<b>Для начала работы давайте определимся с чем будем работать?</b>\n\n"
    keyboards_parsing = parsing_keyboards()  # Клавиатура
    await bot.send_message(callback_query.from_user.id, parsing_post, reply_markup=keyboards_parsing)


class GroupIdConnection(StatesGroup):
    ask_id_pars_group = State()
    ask_id_pars_post = State()


@dp.callback_query_handler(lambda c: c.data == "connection_parsing")
async def connection_parsing(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Напишите ID группы или канала, из которой нужно парсить посты")
    await GroupIdConnection.ask_id_pars_group.set()


@dp.message_handler(state=GroupIdConnection.ask_id_pars_group, content_types=types.ContentType.TEXT)
async def parsing_parsing(message: types.Message, state: FSMContext):
    cursor, conn = writing_channel_group_ids_to_database()
    group_ids = message.text.split(',')
    group_ids = ['-{}'.format(id.strip()) if not id.startswith('-') else id.strip() for id in group_ids]
    group_ids_str = ','.join(group_ids)

    cursor.execute("INSERT INTO parsing_groups (account_id, group_id_pars) VALUES (?, ?)",
                   (message.from_user.id, group_ids_str))
    conn.commit()

    await bot.send_message(message.chat.id, "Напишите ID группы, в которую нужно постить посты")
    await GroupIdConnection.next()


@dp.message_handler(state=GroupIdConnection.ask_id_pars_post, content_types=types.ContentType.TEXT)
async def post_parsing(message: types.Message, state: FSMContext):
    group_id_post = message.text.strip()
    cursor, conn = writing_channel_group_ids_to_database()
    cursor.execute("UPDATE parsing_groups SET group_id_post = ? WHERE account_id = ?",
                   (group_id_post, message.from_user.id))
    conn.commit()
    await bot.send_message(message.chat.id,
                           "Настройки сохранены. Готово для парсинга и постинга. Для возврата введите команду /start")
    await state.finish()


def register_handlers_post_parsing_setting():
    dp.register_callback_query_handler(parsing_parsing, lambda c: c.data == "post_parsing_settings")
    dp.register_message_handler(parsing_parsing)
    dp.register_message_handler(post_parsing)
