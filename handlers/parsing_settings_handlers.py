from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types, F
from keyboards.parsing_keyboards import parsing_keyboards
from system.dispatcher import dp, bot
from system.dispatcher import router
from utils.sqlipe_utils import writing_channel_group_ids_to_database
from aiogram.types import Message


class GroupIdConnection(StatesGroup):
    ask_id_pars_group = State()
    ask_id_pars_post = State()


@router.callback_query(F.data == "post_parsing_settings")
async def parsing_parsing(callback_query: types.CallbackQuery, state: FSMContext):
    parsing_post = ("<b>Для начала работы давайте определимся с чем будем работать?</b>\n\n"
                    "Для возврата введите команду /start\n\n")
    keyboards_parsing = parsing_keyboards()  # Клавиатура
    await bot.send_message(callback_query.from_user.id, parsing_post, reply_markup=keyboards_parsing, parse_mode="HTML")


@router.callback_query(F.data == "connection_parsing")
async def connection_parsing(callback_query: types.CallbackQuery, state: FSMContext):
    """Настройка parsing постов группы / канала"""
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Напишите ID группы или канала, из которой нужно parsing посты")
    await state.set_state(GroupIdConnection.ask_id_pars_group)


@router.message(GroupIdConnection.ask_id_pars_group)
async def parsing_parsing(message: Message, state: FSMContext):
    """Записываем ID группы / канала в базу данных"""
    cursor, conn = writing_channel_group_ids_to_database()
    group_ids = message.text.split(',')
    group_ids = ['-{}'.format(id.strip()) if not id.startswith('-') else id.strip() for id in group_ids]
    group_ids_str = ','.join(group_ids)
    # Записываем данные в базу данных ID аккаунта и ID группы с которого нужно parsing посты
    cursor.execute("INSERT INTO parsing_groups (account_id, group_id_pars) VALUES (?, ?)",
                   (message.from_user.id, group_ids_str))
    conn.commit()

    await bot.send_message(message.chat.id, "Напишите ID группы, в которую нужно постить посты")
    await state.set_state(GroupIdConnection.ask_id_pars_post)


@router.message(GroupIdConnection.ask_id_pars_post)
async def post_parsing(message: Message, state: FSMContext):
    """Запись ID группы в которую нужно публиковать посты"""
    group_id_post = message.text.strip()
    cursor, conn = writing_channel_group_ids_to_database()
    cursor.execute("UPDATE parsing_groups SET group_id_post = ? WHERE account_id = ?",
                   (group_id_post, message.from_user.id))
    conn.commit()
    await bot.send_message(message.chat.id,
                           "⚙️ Настройки сохранены 💾. Готово для parsing и постинга. Для возврата введите команду /start")
    await state.clear()


def register_handlers_post_parsing_setting():
    dp.message.register(parsing_parsing)
    dp.message.register(post_parsing)
