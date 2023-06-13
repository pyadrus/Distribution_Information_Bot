from pyrogram import Client, filters


# Создайте экземпляр клиента Pyrogram
app = Client("my_bot", api_id=21759468, api_hash="645f4b02751bf9a45d7218f7a009325e")

# Здесь указывается идентификатор исходной группы, из которой вы хотите парсить текст
source_group_id = -1001802341602

# Здесь указываются идентификаторы групп, в которые вы хотите отправить текст
destination_group_ids = [-1001844894766, -1001604184709]


# Фильтр для обработки всех сообщений в исходной группе
@app.on_message(filters.chat(source_group_id))
async def forward_message(message):
    print(message)
    # Проверка, является ли чат текущего сообщения исходной группой
    if str(message.chat.id) == str(source_group_id):
        # Если сообщение не содержит медиа-группы
        if message.media_group_id is None:
            # Копирование сообщения в каждую группу назначения
            for destination_group_id in destination_group_ids:
                await app.copy_message(chat_id=destination_group_id, from_chat_id=message.chat.id, message_id=message.id)
        else:
            # Если сообщение содержит медиа-группу
            if message.media_group_id not in destination_group_ids:
                # Получение медиа-группы из исходного сообщения
                media_group = await app.get_media_group(chat_id=message.chat.id, message_id=message.message_id)
                # Отправка медиа-группы в каждую группу назначения
                for destination_group_id in destination_group_ids:
                    await app.send_media_group(chat_id=destination_group_id, media=media_group)
        print('Пост опубликован')

# Запуск клиента Pyrogram
app.run()
