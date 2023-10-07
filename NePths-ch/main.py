import random
import telebot

bot = telebot.TeleBot('6085793195:AAFNk5Luf6-vQuUd708UMsVw-xR2W5CA3cU')

users = set()  # {tg_id}

users_in_flood = set()
users_in_love = set()
users_in_hw = set()

users_nick_idkey = dict()  # {tg_id: nick}
users_nick_nickkey = dict()  # {nick: tg_id}

chat_bred_id = '-1001655602242'

chat_theme_love = 2 # Темы Беседы
chat_theme_bred = 0
chat_theme_hw = 12

start_commands = '/startflood - Начать флудеть\n/stopflood - Перестать флудеть\n\n/sms - Отправить сообщение пользователю\n/help - помощь\n/love - Признавашки\n/hwhelp - Дз'

nick = 1 # Ник чела
in_chat = False # Флаг для проверки нахождения в чате

with open('numbers.txt', 'r') as file: # Генирация ников из файла
    numbers = file.readlines()

@bot.message_handler(content_types=['text'])
def start(message):
    # bot.send_message(chat_bred_id, "ку", message_thread_id=2)
    if message.chat.id in users:
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/reg':
        bot.send_message(message.chat.id, start_commands)
        nick = random.choice(numbers).rstrip()
        users_nick_idkey[message.chat.id] = str(nick)  # Присвоение ника в мапу
        users_nick_nickkey[str(nick)] = message.chat.id
        bot.send_message(message.chat.id, f"Ты зареган под ником {nick}")
        users.add(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/help':
        bot.send_message(message.chat.id, start_commands)
        bot.register_next_step_handler(message, start)
    else:
        bot.register_next_step_handler(message, start)


def get_command(message): # Команды для зареганных пользователей
    if message.text == '/startflood':
        global in_chat
        in_chat = True
        bot.send_message(message.chat.id, 'Начинаю флудить')
        users_in_flood.add(message.chat.id)
        bot.register_next_step_handler(message, flood)
    elif message.text == '/sms':
        bot.send_message(message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(message, direct_message)
    elif message.text == '/love':
        bot.send_message(message.chat.id, 'Можно писать')
        users_in_love.add(message.chat.id)
        bot.register_next_step_handler(message, love_chat)
    elif message.text == '/hwhelp':
        bot.send_message(message.chat.id, 'Можно писать в дз')
        users_in_hw.add(message.chat.id)
        bot.register_next_step_handler(message, hwhelp_chat)
    else:
        bot.send_message(message.chat.id, '/startflood - Начать флудеть\n/stopflood - Перестать флудеть\n/help - помощь')
        bot.register_next_step_handler(message, get_command)


def hwhelp_chat(message):
    if message.text == '/stophw':
        bot.send_message(message.chat.id, 'Дз остановлено')
        users_in_hw.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.content_type == 'text' and message.text.startswith('/'):
        get_command_and_chat(message, chat_theme_hw)
    else:
        mailing(message, chat_theme_hw)

def love_chat(message):
    print(users_in_love)
    if message.text == '/stoplove':
        bot.send_message(message.chat.id, 'Любовь остановлена')
        users_in_love.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.content_type == 'text' and message.text.startswith('/'):
        get_command_and_chat(message, chat_theme_love)
    else:
        mailing(message, chat_theme_love)
def get_command_and_chat(message, chat_thread_id): # Команды доступные в чате
    if message.text == '/sms':
        bot.send_message(message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(message, direct_message)
    elif message.text == '/help':
        bot.send_message(message.chat.id, start_commands)
        bot.send_message(message.chat.id, 'Продолжайте общение')
        if chat_thread_id == chat_theme_bred:
            bot.register_next_step_handler(message, flood)
        elif chat_thread_id == chat_theme_love:
            bot.register_next_step_handler(message, love_chat)
        elif chat_thread_id == chat_theme_hw:
            bot.register_next_step_handler(message, hwhelp_chat)
    else:
        check_chat(message, chat_thread_id)
        # bot.register_next_step_handler(message, flood)


def flood(message):
    if message.text == '/stopflood':  # Cтоп флуда
        bot.send_message(message.chat.id, 'Флуд остановлен')
        users_in_flood.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.content_type == 'text' and message.text.startswith('/'):  # Команда внутри чата
        get_command_and_chat(message, chat_theme_bred)
    else:  # Ветка флуда
        mailing(message, chat_theme_bred)
def mailing(message, chat_thread_id): # Рассылка
    users_in_chat = {}
    if chat_thread_id == chat_theme_bred:
        users_in_chat = users_in_flood
    elif chat_thread_id == chat_theme_love:
        users_in_chat = users_in_love
    else:
        users_in_chat = users_in_hw

    if message.reply_to_message: #reply to message
        if message.content_type == 'text':
            text = f"Ответ на сообщение '{message.reply_to_message.text}'\n\n"
            bot.send_message(chat_bred_id, text + message.text + f" от {users_nick_idkey[message.chat.id]} ", message_thread_id = chat_thread_id)
            for i in users_in_chat:
                if i != message.chat.id:
                    bot.send_message(i, text + message.text + f" от {users_nick_idkey[message.chat.id]} ")
            check_chat(message, chat_thread_id)
        elif message.content_type == 'audio':
            text = f"Ответ на сообщение '{message.reply_to_message.caption}'\n\n"
            bot.send_audio(chat_bred_id, message.audio.file_id, text + message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
            for i in users_in_chat:
                if i != message.chat.id:
                    bot.send_audio(i, message.audio.file_id, text + message.caption + f' от {users_nick_idkey[message.chat.id]}')
            check_chat(message, chat_thread_id)
        elif message.content_type == 'photo':
            text = f"Ответ на сообщение '{message.reply_to_message.text}'\n\n"
            bot.send_photo(chat_bred_id, message.photo[0].file_id, text + message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
            for i in users_in_chat:
                if i != message.chat.id:
                    bot.send_photo(i, message.photo[0].file_id, text + message.caption + f' от {users_nick_idkey[message.chat.id]}')
            check_chat(message, chat_thread_id)


    elif message.content_type == 'audio':
        bot.send_audio(chat_bred_id, message.audio.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_audio(chat_bred_id, message.audio.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'photo':
        bot.send_photo(chat_bred_id, message.photo[0].file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_photo(i, message.photo[0].file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}')
        check_chat(message, chat_thread_id)
    elif message.content_type == 'text':
        bot.send_message(chat_bred_id, message.text + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_message(i, message.text + f' от {users_nick_idkey[message.chat.id]}')
        check_chat(message, chat_thread_id)
    elif message.content_type == 'video':
        bot.send_video(chat_bred_id, message.video.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_video(i, message.video.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}')
        check_chat(message, chat_thread_id)
    elif message.content_type == 'voice':
        bot.send_voice(chat_bred_id, message.voice.file_id, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_voice(i, message.voice.file_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'document':
        # bot.send_document(chat_bred_id, message.document.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}')
        bot.send_document(chat_bred_id, message.document.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}', message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_document(i, message.document.file_id, message.caption + f' от {users_nick_idkey[message.chat.id]}')
        check_chat(message, chat_thread_id)
    elif message.content_type == 'sticker':
        bot.send_sticker(chat_bred_id, message.sticker.file_id, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_sticker(i, message.sticker.file_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'video_note':
        bot.send_video_note(chat_bred_id, message.video_note.file_id, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_video_note(i, message.video_note.file_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'location':
        bot.send_location(chat_bred_id, message.location.latitude, message.location.longitude, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_location(i, message.location.latitude, message.location.longitude)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'contact':
        bot.send_contact(chat_bred_id, message.contact.phone_number, message.contact.first_name, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_contact(i, message.contact.phone_number, message.contact.first_name)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'animation':
        bot.send_animation(chat_bred_id, message.animation.file_id, message_thread_id = chat_thread_id)
        for i in users_in_chat:
            if i != message.chat.id:
                bot.send_animation(i, message.animation.file_id)
        check_chat(message, chat_thread_id)
    else:
        bot.send_message(message.chat.id, 'Неверный тип сообщения')
        check_chat(message, chat_thread_id)


def check_chat(message, id):
    if id == chat_theme_bred:
        bot.register_next_step_handler(message, flood)
    elif id == chat_theme_love:
        bot.register_next_step_handler(message, love_chat)
    elif id == chat_theme_hw:
        bot.register_next_step_handler(message, hwhelp_chat)
    else:
        pass

def direct_message(message):  # Получение id для sms
    id_user_for_sms = message.text
    bot.send_message(message.chat.id, 'Введите текст')
    bot.register_next_step_handler(message, direct_message_send, id_user_for_sms)


def direct_message_send(message, id_user_for_sms): # Отправка смс
    global in_chat
    try:
        bot.send_message(users_nick_nickkey[id_user_for_sms], message.text)
    except KeyError:
        bot.send_message(message.chat.id, 'Неверный id')

    if in_chat: # Проверка нахождения в чате
        bot.send_message(message.chat.id, 'Продолжайте общение')
        bot.register_next_step_handler(message, flood)
    else:
        bot.register_next_step_handler(message, get_command)


bot.polling(none_stop=True, interval=0)
