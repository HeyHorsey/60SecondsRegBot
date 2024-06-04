from settings import STOP_WORD
import telebot
bot = telebot.TeleBot(TOKEN)


# extract text from announcement
def handle_announcement(message):
    text_lines = message.text.split('\n')
    message_text = ''
    for line in text_lines:
        if STOP_WORD in line:
            break
        message_text += line + '\n'
    return message_text


# Check if team is already registered
def already_registered(message):
    messages = bot.get_chat_history()
