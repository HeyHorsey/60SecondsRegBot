from settings import STOP_WORD, TOKEN
import telebot
bot = telebot.TeleBot(TOKEN)


# extract text from announcement
def handle_announcement(text):
    # Handle both string input and message object
    if not isinstance(text, str):
        return ""

    text_lines = text.split('\n')
    message_text = ''
    for line in text_lines:
        if STOP_WORD in line:
            break
        message_text += line + '\n'

    return message_text.strip()



# Check if team is already registered
def already_registered(message):
    # Ensure we have a reply to a poll
    if not message.reply_to_message or not message.reply_to_message.poll:
        return False

    poll_message_id = message.reply_to_message.message_id
    chat_id = message.chat.id

    try:

        # Check our registration log
        with open('registration_log.txt', 'r') as file:
            log_entries = file.readlines()

        # Check if this poll has been registered already
        registration_key = f"{chat_id}:{poll_message_id}"
        for entry in log_entries:
            if registration_key in entry:
                return True

        # If we reach here, no registration was found
        return False

    except FileNotFoundError:
        # No registration log exists yet
        return False

# Log registrations (to be moved to DB sometime later)
def log_registration(message):

    if not message.reply_to_message or not message.reply_to_message.poll:
        return

    poll_message_id = message.reply_to_message.message_id
    chat_id = message.chat.id
    registration_key = f"{chat_id}:{poll_message_id}"

    # Append to registration log
    with open('registration_log.txt', 'a+') as file:
        file.write(f"{registration_key}\n")