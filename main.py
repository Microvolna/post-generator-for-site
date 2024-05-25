from config import TOKEN
from do_post import do_post

import telebot
import time
from loguru import logger

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    while True:
        logger.debug('Цикл запущен')
        if time.strftime("%H", time.localtime()) in ['9', '14', '21']:

            logger.debug('Генерирую пост')

            try:
                msg_text = do_post()  # Возвращает сообщение, str
                print(msg_text)

                logger.debug('Публикую пост')

                bot.send_message('@masterskaya_AI', msg_text, parse_mode='MARKDOWN')

            except Exception as e:
                logger.error(f'Ошибка во время генерации поста - {e}')

        time.sleep(3600)

bot.infinity_polling()