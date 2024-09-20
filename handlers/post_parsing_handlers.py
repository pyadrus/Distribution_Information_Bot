import sqlite3

from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest

from keyboards.greeting_keyboards import keyboard_return_start_menu
from system.dispatcher import dp, bot, tg_id, tg_hash
from system.dispatcher import router
from utils.sqlipe_utils import we_get_the_data_of_the_connected_accounts


def get_parsing_post_group():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parsing_groups")
    parsing_groups = cursor.fetchall()  # Возвращаем все строки
    conn.close()  # Не забываем закрыть соединение
    return parsing_groups

@router.callback_query(F.data == "parsing_run")
async def run_parsing(callback_query: types.CallbackQuery):
    """Запуск парсинга постов"""
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Парсинг постов запущен!")

    parsing_groups = get_parsing_post_group()
    logger.info(parsing_groups)

    if not parsing_groups:
        await bot.send_message(callback_query.from_user.id, "Нет доступных групп для парсинга.")
        return

    for row in parsing_groups:
        group_id_post_send = row[1]  # id группы, куда отправляются посты
        group_id_post_pars = row[2]  # id группы, откуда берутся посты

        # Запускаем парсинг сообщений
        await post(callback_query.from_user.id, group_id_post_send, group_id_post_pars)


async def post(user_id, group_id_post_send, group_id_post_pars):
    """Создание экземпляра клиента Telethon и запуск парсинга"""
    row = we_get_the_data_of_the_connected_accounts()
    logger.info(row)
    if row:
        client = TelegramClient(f"accounts/{user_id}/{row[1]}", api_id=tg_id, api_hash=tg_hash,
                                system_version="4.16.30-vxCUSTOM")
        await client.connect()

        await client(JoinChannelRequest(group_id_post_pars))  # Подключаемся к группе

        @client.on(events.NewMessage(chats=group_id_post_pars))  # Обработчик новых сообщений в группе
        async def forward_message_wrapper(event):
            """Фильтр для обработки всех новых сообщений в исходной группе"""
            message = event.message

            # Проверяем, является ли это личный аккаунт или группа для отправки
            if str(group_id_post_send).startswith('9'):  # Если это ID пользователя (начинается на 9)
                # Отправляем сообщение от имени бота
                if message.media:
                    # Если сообщение содержит медиа, отправляем медиа-файл
                    media = message.media
                    await bot.send_photo(chat_id=int(group_id_post_send), photo=media)
                else:
                    # Отправляем текстовое сообщение
                    await bot.send_message(chat_id=int(group_id_post_send), text=message.text)
            else:  # Если это группа
                if message.media:
                    # Отправляем медиа-сообщение
                    media = message.media
                    await bot.send_photo(chat_id=int(group_id_post_send), photo=media)
                else:
                    # Отправляем текстовое сообщение
                    await bot.send_message(chat_id=int(group_id_post_send), text=message.text)

            logger.info('Пост успешно отправлен ботом')

        # Запуск клиента и обработка событий
        logger.info(f"Запуск клиента для аккаунта {row[1]}")
        await client.run_until_disconnected()


# Функция для записи в базу данных
def group_id_entry_for_publication(account_id, group_id_post_send, group_id_post_pars):
    conn = sqlite3.connect('setting/database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS parsing_groups (
                        account_id INTEGER,
                        group_id_post_send INTEGER,
                        group_id_post_pars INTEGER)""")
    conn.commit()
    cursor.execute("INSERT INTO parsing_groups (account_id, group_id_post_send, group_id_post_pars) VALUES (?, ?, ?)",
                   (account_id, group_id_post_send, group_id_post_pars))
    conn.commit()
    conn.close()


class IDGroupCreation(StatesGroup):
    """Определение StatesGroup для управления ходом разговора"""
    group_id_post_send = State() # id группы для отправки сообщений (куда публикуются посты)
    group_id_post_pars = State() # id группы для публикации постов (откуда парсятся посты)


@router.callback_query(F.data == "group_entry_for_publication")
async def group_entry_for_publication(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало процесса ввода ID групп для публикации"""
    await callback_query.answer()
    connect_ac_post = ("<b>ID группы, куда публикуются посты</b>\n\n"
                       "Для возврата нажмите на /start")
    await bot.send_message(callback_query.from_user.id, connect_ac_post, parse_mode="HTML",
                           reply_markup=keyboard_return_start_menu())
    await state.set_state(IDGroupCreation.group_id_post_send)


@router.message(StateFilter(IDGroupCreation.group_id_post_send))
async def id_group_pars(message: Message, state: FSMContext):
    """Получение ID группы, куда публикуются посты"""
    group_id_pars = message.text
    # Сохраняем ID группы в состоянии
    await state.update_data(group_id_pars=group_id_pars)
    connect_ac_post = ("<b>ID группы, откуда публикуются посты</b>\n\n"
                       "Для возврата нажмите на /start")
    await bot.send_message(message.from_user.id, connect_ac_post, parse_mode="HTML",
                           reply_markup=keyboard_return_start_menu())
    await state.set_state(IDGroupCreation.group_id_post_pars)


@router.message(StateFilter(IDGroupCreation.group_id_post_pars))
async def id_group_post(message: Message, state: FSMContext):
    """Получение ID группы, откуда публикуются посты и запись в базу"""
    group_id_post_pars = message.text
    # Получаем сохраненные данные из FSM
    data = await state.get_data()
    group_id_post_send = data.get('group_id_post_send')
    # Получаем account_id из ID пользователя
    account_id = message.from_user.id
    # Записываем данные в базу
    group_id_entry_for_publication(account_id, group_id_post_send, group_id_post_pars)
    # Завершаем состояние
    await bot.send_message(message.from_user.id, "<b>Данные успешно сохранены!</b>", parse_mode="HTML",
                           reply_markup=keyboard_return_start_menu())
    await state.clear()




def register_handlers_post_parsing():
    dp.message.register(run_parsing)
    dp.message.register(group_entry_for_publication)
