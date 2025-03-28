import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import toolbox
from telebot import types
from settings import TOKEN, TEAM_CHAT, GAME_ADMIN, TEAM_NAME
bot = telebot.TeleBot(TOKEN)

#Send poll when announcement received
@bot.channel_post_handler(content_types=['photo', 'text'])
def handle_all_channel_posts(message):
    print(f"Received channel post with content type: {message.content_type}")

    if message.content_type == 'photo':
        print("This is a photo post")
        if hasattr(message, 'caption') and message.caption:
            print(f"Caption: {message.caption}")
            if '#анонс' in message.caption:
                print("Processing photo announcement")
                poll_options = ['Иду', 'Не иду', 'Посмотреть результаты']
                question = toolbox.handle_announcement(message.caption)
                poll_message = bot.send_poll(
                    chat_id=TEAM_CHAT,
                    question=question,
                    options=poll_options,
                    is_anonymous=False
                )
                bot.pin_chat_message(
                    chat_id=TEAM_CHAT,
                    message_id=poll_message.message_id,
                    disable_notification=False
                )

    elif message.content_type == 'text' and '#анонс' in message.text:
        print("Processing text announcement")
        poll_options = ['Иду', 'Не иду', 'Посмотреть результаты']
        poll_message = bot.send_poll(
            chat_id=TEAM_CHAT,
            question=toolbox.handle_announcement(message),
            options=poll_options,
            is_anonymous=False
        )
        bot.pin_chat_message(
            chat_id=TEAM_CHAT,
            message_id=poll_message.message_id,
            disable_notification=False
        )

# Registration
@bot.message_handler(commands=['reg'])
def register_team(message):

    # Debug: Print out all available message attributes
    print("Message attributes:")
    #print(f"Text: {message.text}")
    #print(f"Reply to message: {message.reply_to_message}")

    if message.reply_to_message and message.reply_to_message.poll:

        # Debug: Print poll details
        #print("Poll details:")
        #print(f"Poll question: {message.reply_to_message.poll.question}")
        #print(f"Message reply text: {message.reply_to_message.text}")
        #print(f"Message reply caption: {message.reply_to_message.caption}")

        poll = message.reply_to_message.poll

        # Get participants count and game details from poll
        participants_count = 0
        for option in poll.options:
            if option.text == "Иду":
                participants_count = option.voter_count
                break

        game_details = poll.question

        # Check if already registered
        if not toolbox.already_registered(message):
            # Generate application message
            application_message = f"Заявка на регистрацию\n{game_details}\nКоманда: {TEAM_NAME}\nИгроков: {participants_count}"
            confirm_button = InlineKeyboardButton(text="Подтвердить", callback_data='confirm')
            confirm_markup = InlineKeyboardMarkup([[confirm_button]])

            # Send application to admin
            bot.send_message(chat_id=GAME_ADMIN, text=application_message, reply_markup=confirm_markup)

            # Log this registration
            toolbox.log_registration(message)

            # Send confirmation
            bot.send_message(chat_id=TEAM_CHAT, text="Заявка отправлена")
        else:
            bot.send_message(chat_id=TEAM_CHAT, text="Команда уже зарегистрирована на эту игру")
    else:
        bot.send_message(chat_id=TEAM_CHAT, text="Игра не найдена")


@bot.callback_query_handler(func=lambda call: True)
def button(call):
    if call.data == 'confirm':
        message_id = call.message.message_id

        # Send confirmation message to team
        bot.send_message(chat_id=TEAM_CHAT, text="Команда зарегистрирована на игру")

        # Update the admin message to show confirmation is complete
        new_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(text="✓ Подтверждено", callback_data='confirmed')
        ]])

        bot.edit_message_reply_markup(
            chat_id=GAME_ADMIN,
            message_id=message_id,
            reply_markup=new_markup
        )

        # Answer the callback to remove loading state
        bot.answer_callback_query(call.id, text="Регистрация подтверждена")

    elif call.data == 'confirmed':
        # This handles clicks on the already-confirmed button
        bot.answer_callback_query(call.id, text="Регистрация уже была подтверждена")


# Just leave it here
bot.polling()
