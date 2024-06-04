import telebot
import toolbox
from telebot import types
from settings import TOKEN, TEAM_CHAT, GAME_ADMIN

bot = telebot.TeleBot(TOKEN)


# send poll when game is announced
@bot.message_handler(func=lambda message: '#анонс' in message.text)
def poll_create(message):
    poll_options = ['Иду', 'Не иду', 'Посмотреть результаты']
    poll_message = bot.send_poll(chat_id=TEAM_CHAT, question=toolbox.handle_announcement(message), options=poll_options, is_anonymous=False)
    bot.pin_chat_message(chat_id=TEAM_CHAT, message_id=poll_message.message_id, disable_notification=False)
