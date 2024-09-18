import time

from aiogram import types, F
from pyrogram import Client, filters

from system.dispatcher import dp, bot, tg_id, tg_hash
from system.dispatcher import router
from utils.sqlipe_utils import read_parsing_groups, we_get_the_data_of_the_connected_accounts


async def forward_message(client, message, group_id_pars, group_id_post):
    """Фильтр для обработки всех сообщений в исходной группе"""
    print(message)
    if str(message.chat.id) == str(int(group_id_pars)):
        if message.media_group_id is None:
            time.sleep(1)
            await client.copy_message(chat_id=group_id_post, from_chat_id=message.chat.id, message_id=message.id)
        else:
            if message.media_group_id not in int(group_id_pars):
                media_group = await client.get_media_group(chat_id=message.chat.id, message_id=message.id)
                time.sleep(1)
                await client.send_media_group(chat_id=group_id_post, media=media_group)
        print('Пост опубликован')


async def post(account_id, group_id_pars, group_id_post):
    """Создание экземпляра клиента Pyrogram"""
    row = we_get_the_data_of_the_connected_accounts()
    if row:
        app = Client(f"accounts/{row[0]}/{row[1]}", api_id=tg_id, api_hash=tg_hash)

        @app.on_message(filters.chat(int(group_id_pars)))
        async def forward_message_wrapper(client, message):
            """Фильтр для обработки всех сообщений в исходной группе"""
            await forward_message(client, message, group_id_pars, group_id_post)

        # Запуск клиента Pyrogram
        await app.start()

@router.callback_query(F.data == "parsing_run")
async def run_parsing(callback_query: types.CallbackQuery):
    """Запуск parsing постов"""
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Парсинг постов запущен!")

    parsing_groups = read_parsing_groups()
    for row in parsing_groups:
        account_id = row[0]  # id аккаунта
        group_id_pars = row[1]  # id группы
        group_id_post = row[2]  # Разделение строки на отдельные идентификаторы групп
        await post(account_id, group_id_pars, group_id_post)


def register_handlers_post_parsing():
    dp.message.register(run_parsing)
