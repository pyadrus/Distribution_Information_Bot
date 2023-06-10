import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота и диспетчера
bot_token = 'YOUR_BOT_TOKEN'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def forward_message(message: types.Message):
    # Получение информации о канале, из которого нужно переслать пост
    channel_id = '@YOUR_CHANNEL_USERNAME'

    # Получение информации о группах, в которые нужно переслать пост
    group_ids = ['@GROUP_USERNAME_1', '@GROUP_USERNAME_2', '@GROUP_USERNAME_3']

    # Пересылка поста в каждую группу
    for group_id in group_ids:
        try:
            await bot.forward_message(chat_id=group_id, from_chat_id=channel_id, message_id=message.message_id)
            logging.info(f"Post forwarded to {group_id}")
        except Exception as e:
            logging.error(f"Failed to forward post to {group_id}: {str(e)}")


if __name__ == '__main__':
    # Запуск бота
    try:
        logging.info("Starting bot...")
        dp.run_polling()
    except Exception as e:
        logging.error(f"Error occurred while running the bot: {str(e)}")
