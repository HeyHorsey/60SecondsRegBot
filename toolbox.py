from settings import STOP_WORD


# extract text from announcement
def handle_announcement(message):
    text_lines = message.text.split('\n')
    message_text = ''
    for line in text_lines:
        if STOP_WORD in line:
            break
        message_text += line + '\n'
    return message_text
