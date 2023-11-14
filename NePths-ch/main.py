import telebot

import random
import datetime
import time

bot = telebot.TeleBot('6085793195:AAFNk5Luf6-vQuUd708UMsVw-xR2W5CA3cU', skip_pending=True)

# Временные бдшки
users = set()  # {tg_id}

users_in_flood = set()
users_in_friends = set()
users_in_hw = set()

users_nick_idkey = dict()  # {tg_id: nick}
users_nick_nickkey = dict()  # {nick: tg_id}

chat_all_id = '-1001655602242'  # id беседы

chat_theme_friends = 2  # id тем Беседы
chat_theme_flood = 0
chat_theme_hw = 12
cur_theme = 0  # Текущая тема

type_of_files = {'audio': 'Аудио', 'document': 'Документ', 'photo': 'Фото', 'sticker': 'Стикер', 'video': 'Видео',
                 'location': 'Геопозиция', 'contact': 'Контакт', 'text': 'Текст', 'voice': 'Голосовое сообщение',
                 'video_note': 'Видео-сообщение', 'animation': 'Гифка', 'poll': 'Опрос', 'dice': 'Кубик',
                 'venue': 'Место', 'invoice': 'Счет', 'successful_payment': 'Успешный платеж', 'game': 'Игра',
                 'photo': 'Фото', 'video': 'Видео', 'voice': 'Голосовое сообщение', 'video_note': 'Видео-сообщение',
                 'animation': 'Гифка'}
name_of_chats = {chat_theme_flood: 'Флудилка', chat_theme_hw: 'Помощь с ДЗ', chat_theme_friends: 'Признавашки'}

start_commands = '/help - помощь\n/me - Узнать ник\n/change - Сменить ник\n/sms - Отправить сообщение пользователю\n\n/b - Начать флудеть\n/friends - Признавашки\n/hw - Помощь с дз\n\n/whereme - Узнать в каком ты чате\n/exit - Выйти из текущего чата'

messages_in_flood = []
messages_in_hw = []
messages_in_friends = []



nick_of_user = 1  # Ник чела
is_in_chat = False  # Флаг для проверки нахождения в чате

with open('numbers.txt', 'r') as file:  # Генерация ников из файла
    numbers = file.readlines()


# TODO Антиспам, ЧС в бд
# TODO - Локалка для localtest
# TODO - БД для хранения ников и id
# TODO - Глобальный рефакторинг (+ разделение кода на несколько .py)
# TODO Система ников
# TODO - Иногда бот позволяет сделать несколько команд подряд, надо исправить
# TODO - Кнопки для быстрого использования
# TODO - Трансляция геопозиции отправка / реплай?
# TODO Сделать подписи к форвардам
# TODO - Рефакторинг рассылки 5ти сообщений

# TODO 4. Может бот будет присылать последние 5 сообщений? [СДЕЛАНО]
# TODO - Полуанонимный чат [СДЕЛАНО]
# TODO 2./whereami (в каком ты сейчас чате) [СДЕЛАНО]
# TODO 1. /startflood —> /b [СДЕЛАНО]
# TODO 3. /exit вместо /stop… (закрытие сессии в текущем разделе) [СДЕЛАНО]

def delete_the_sign(sm_text, sender_id, replied_id):  # Удалить первую строку, т.е. подпись [xxx]
    if sender_id == replied_id:
        return sm_text
    return sm_text.split('\n', 1)[1]


def get_the_sign(sm_text, sender_id, replied_id):  # Получить первую строку, т.е. подпись [xxx]
    if sender_id == replied_id:
        return f'[{users_nick_idkey[sender_id]}]'
    return sm_text.split('\n', 1)[0][:-1]


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'location', 'contact', 'voice', 'video_note', 'animation', 'poll', 'dice', 'venue', 'invoice', 'successful_payment', 'game'])
def start(message):
    if str(message.chat.id) == str(chat_all_id):
        cur_chat = message.message_thread_id
        if cur_chat is None:
            for cur_user in users_in_flood:
                bot.forward_message(cur_user, message.chat.id, message.message_id)
        elif cur_chat == chat_theme_friends:
            for cur_user in users_in_friends:
                bot.forward_message(cur_user, message.chat.id, message.message_id)
        elif cur_chat == chat_theme_hw:
            for cur_user in users_in_hw:
                bot.forward_message(cur_user, message.chat.id, message.message_id)
        else:
            pass
    elif message.chat.id in users:
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/reg' and message.chat.id not in users:
        bot.send_message(message.chat.id, start_commands)
        nick = random.choice(numbers).rstrip()
        users_nick_idkey[message.chat.id] = str(nick)  # Присвоение ника в мапу
        users_nick_nickkey[str(nick)] = message.chat.id
        bot.send_message(message.chat.id, f"Ты зареган под ником {nick}")
        users.add(message.chat.id)
        print(users)
        print(users_nick_idkey)
        print("_______________________")
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/reboot':
        bot.send_message(message.chat.id, 'Перезагрузка')
        users.clear()
        users_in_flood.clear()
        users_in_friends.clear()
        users_in_hw.clear()
        users_nick_idkey.clear()
        users_nick_nickkey.clear()
        n = 5 / 0
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, "Необходимо обязательно зарегистрироваться /reg")
        bot.send_message(message.chat.id, start_commands)
        bot.register_next_step_handler(message, start)


def get_command(message):  # Команды для зареганных пользователей
    global cur_theme, is_in_chat
    if message.text == '/sms':
        bot.register_next_step_handler(message, direct_message)
    elif message.text == '/change':
        bot.send_message(message.chat.id, 'Сейчас произойдёт смена ника')
        change_nick(message)
    elif message.text == '/me':
        bot.send_message(message.chat.id, f'Твой ник: <b>{users_nick_idkey[message.chat.id]}</b>', parse_mode='HTML')
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/help':
        bot.send_message(message.chat.id, start_commands)
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/whereme':
        bot.send_message(message.chat.id, f'<b>Вы сейчас не в чате</b>\n\n{start_commands}', parse_mode='HTML')
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/reboot':
        bot.send_message(message.chat.id, 'Перезагрузка')
        users.clear()
        users_in_flood.clear()
        users_in_friends.clear()
        users_in_hw.clear()
        users_nick_idkey.clear()
        users_nick_nickkey.clear()
        n = 5 / 0
        bot.register_next_step_handler(message, start)
    elif message.text == '/b':
        is_in_chat = True
        cur_theme = chat_theme_flood
        users_in_flood.add(message.chat.id)
        bot.send_message(message.chat.id, 'Начинаю флудить')
        for last_message in messages_in_flood:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        bot.register_next_step_handler(message, flood)
    elif message.text == '/friends':
        is_in_chat = True
        cur_theme = chat_theme_friends
        bot.send_message(message.chat.id, 'Можно писать')
        users_in_friends.add(message.chat.id)
        for last_message in messages_in_friends:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        bot.register_next_step_handler(message, friend_chat)
    elif message.text == '/hw':
        is_in_chat = True
        cur_theme = chat_theme_hw
        bot.send_message(message.chat.id, 'Можно писать в дз')
        users_in_hw.add(message.chat.id)
        for last_message in messages_in_hw:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        bot.register_next_step_handler(message, hw_chat)
    else:
        bot.send_message(message.chat.id, start_commands)
        bot.register_next_step_handler(message, get_command)


def change_nick(message):
    new_nick = random.choice(numbers).rstrip()
    print(users_nick_nickkey, users_nick_idkey)
    users_nick_nickkey.pop(users_nick_idkey[message.chat.id], None)
    users_nick_idkey[message.chat.id] = new_nick
    users_nick_nickkey[new_nick] = message.chat.id
    bot.send_message(message.chat.id, f"Твой новый ник: <b>{new_nick}</b>", parse_mode='html')
    if is_in_chat:
        bot.send_message(message.chat.id, f"Продолжай общаться")
        check_chat(message, cur_theme)
    else:
        bot.register_next_step_handler(message, get_command)


def flood(message):
    if message.text == '/exit':  # Cтоп флуда
        global cur_theme
        cur_theme = chat_theme_flood
        bot.send_message(message.chat.id, 'Вы вышли из чата /flood')
        users_in_flood.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/hw':
        cur_theme = chat_theme_hw
        bot.send_message(message.chat.id, 'Вы вышли из /flood Можно писать в /hw')
        for last_message in messages_in_hw:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_hw.add(message.chat.id)
        users_in_flood.remove(message.chat.id)
        bot.register_next_step_handler(message, hw_chat)
    elif message.text == '/friends':
        cur_theme = chat_theme_friends
        bot.send_message(message.chat.id, 'Вы вышли из /flood Можно писать в /friends')
        for last_message in messages_in_friends:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_friends.add(message.chat.id)
        users_in_flood.remove(message.chat.id)
        bot.register_next_step_handler(message, friend_chat)
    elif message.content_type == 'text' and message.text.startswith('/'):  # Команда внутри чата
        get_command_and_chat(message, chat_theme_flood)
    else:  # Ветка флуда
        mailing(message, chat_theme_flood)


def friend_chat(message):
    global cur_theme, is_in_chat
    if message.text == '/exit':
        is_in_chat = False
        cur_theme = chat_theme_flood
        bot.send_message(message.chat.id, 'Вы вышли из чата /friends')
        users_in_friends.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/b':
        cur_theme = chat_theme_flood
        bot.send_message(message.chat.id, 'Вы вышли из чата /friends и перешли в /b')
        for last_message in messages_in_flood:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_flood.add(message.chat.id)
        users_in_friends.remove(message.chat.id)
        bot.register_next_step_handler(message, flood)
    elif message.text == '/hw':
        cur_theme = chat_theme_hw
        bot.send_message(message.chat.id, 'Вы вышли из /friends и перешли в /hw')
        users_in_hw.add(message.chat.id)
        for last_message in messages_in_hw:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_friends.remove(message.chat.id)
        bot.register_next_step_handler(message, hw_chat)
    elif message.content_type == 'text' and message.text.startswith('/'):
        get_command_and_chat(message, chat_theme_friends)
    else:
        mailing(message, chat_theme_friends)


def hw_chat(message):
    global cur_theme, is_in_chat
    if message.text == '/exit':
        is_in_chat = False
        cur_theme = chat_theme_flood
        bot.send_message(message.chat.id, 'Вы вышли из чата /hw')
        users_in_hw.remove(message.chat.id)
        bot.register_next_step_handler(message, get_command)
    elif message.text == '/b':
        cur_theme = chat_theme_flood
        bot.send_message(message.chat.id, 'Вы вышли из чата /hw и перешли в /flood')
        for last_message in messages_in_flood:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_flood.add(message.chat.id)
        users_in_hw.remove(message.chat.id)
        bot.register_next_step_handler(message, flood)
    elif message.text == '/friends':
        cur_theme = chat_theme_friends
        bot.send_message(message.chat.id, 'Вы вышли из чата /hw и перешли в /friends')
        for last_message in messages_in_friends:
            for it in last_message:
                bot.forward_message(message.chat.id, chat_all_id, message_id=it)
        users_in_friends.add(message.chat.id)
        users_in_hw.remove(message.chat.id)
        bot.register_next_step_handler(message, friend_chat)
    elif message.content_type == 'text' and message.text.startswith('/'):
        get_command_and_chat(message, chat_theme_hw)
    else:
        mailing(message, chat_theme_hw)


def get_command_and_chat(message, chat_thread_id):  # Команды доступные в чате
    if message.text == '/sms':
        bot.send_message(message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(message, direct_message)
    elif message.text == '/help':
        bot.send_message(message.chat.id, start_commands)
        bot.send_message(message.chat.id, 'Продолжайте общение')
        check_chat(message, chat_thread_id)
    elif message.text == '/whereme':
        bot.send_message(message.chat.id, f'Вы сейчас в чате {name_of_chats[chat_thread_id]}')
        check_chat(message, chat_thread_id)
    elif message.text == '/change':
        bot.send_message(message.chat.id, 'Сейчас произойдёт смена ника')
        change_nick(message)
    elif message.text == '/me':
        bot.send_message(message.chat.id, f'Твой ник: <b>{users_nick_idkey[message.chat.id]}</b>', parse_mode='HTML')
        check_chat(message, chat_thread_id)
    elif message.text == '/reboot':
        bot.send_message(message.chat.id, 'Перезагрузка')
        users.clear()
        users_in_flood.clear()
        users_in_friends.clear()
        users_in_hw.clear()
        users_nick_idkey.clear()
        users_nick_nickkey.clear()
        n = 5 / 0
        bot.register_next_step_handler(message, start)
    else:
        check_chat(message, chat_thread_id)
        # bot.register_next_step_handler(message, flood)


def check_thread(messages, chat_thread_id): # Проверка на принадлежность к чату
    if chat_thread_id is None or chat_thread_id == chat_theme_flood:
        if type(messages) == list:
            messages_in_flood.append(messages)
        else:
            messages_in_flood.append([messages])
        if len(messages_in_flood) > 5:
            messages_in_flood.pop(0)
    elif chat_thread_id == chat_theme_friends:
        if type(messages) == list:
            messages_in_friends.append(messages)
        else:
            messages_in_friends.append([messages])
        if len(messages_in_flood) > 5:
            messages_in_flood.pop(0)
    elif chat_thread_id == chat_theme_hw:
        if type(messages) == list:
            messages_in_hw.append(messages)
        else:
            messages_in_hw.append([messages])
        if len(messages_in_flood) > 5:
            messages_in_flood.pop(0)
    else:
        pass



def mailing(message, chat_thread_id):  # Рассылка
    if chat_thread_id == chat_theme_flood:
        users_in_chat = users_in_flood
    elif chat_thread_id == chat_theme_friends:
        users_in_chat = users_in_friends
    else:
        users_in_chat = users_in_hw

    if message.reply_to_message:  # reply to message
        # get a date of reply_to_message
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]:</b>'
        sign_replied = f'<b>[{users_nick_idkey[message.reply_to_message.chat.id]}]</b>'

        content_of_reply = message.reply_to_message.content_type
        caption_of_reply = '' if message.reply_to_message.caption is None else f'> <i>{message.reply_to_message.caption}</i>\n'
        caption_of_message = type_of_files[message.content_type] if message.caption is None else f'{message.caption}'

        date_mc = message.reply_to_message.date
        date_mc = datetime.datetime.fromtimestamp(date_mc)
        date_mc = date_mc.strftime("%H:%M:%S")

        if message.content_type == 'text':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                message_bot = bot.send_message(chat_all_id,
                                 f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{message.text}',
                                 message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user,
                                         f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{message.text}',
                                         parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{message.text}'
                message_bot = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'audio':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_audio(chat_all_id, message.audio.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_audio(cur_user, message.audio.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_audio(chat_all_id, message.audio.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_audio(cur_user, message.audio.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'photo':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f"{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}"
                message_bot = bot.send_photo(chat_all_id, message.photo[0].file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_photo(cur_user, message.photo[0].file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_photo(chat_all_id, message.photo[0].file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_photo(cur_user, message.photo[0].file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'document':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_document(chat_all_id, message.document.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_document(cur_user, message.document.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_document(chat_all_id, message.document.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_document(cur_user, message.document.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'video':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_video(chat_all_id, message.video.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_video(cur_user, message.video.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_video(chat_all_id, message.video.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_video(cur_user, message.video.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'animation':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_animation(chat_all_id, message.animation.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_animation(cur_user, message.animation.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_animation(chat_all_id, message.animation.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_animation(cur_user, message.animation.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'voice':
            if content_of_reply == 'text':
                reply_text = f'> <i>{delete_the_sign(message.reply_to_message.text, message.chat.id, message.reply_to_message.from_user.id)}</i>'
                text = f'{reply_text}\nОт {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_voice(chat_all_id, message.voice.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_voice(cur_user, message.voice.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
            else:
                text = f'{caption_of_reply}{type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot = bot.send_voice(chat_all_id, message.voice.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
                check_thread(message_bot.message_id, chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_voice(cur_user, message.voice.file_id, caption=text, parse_mode="html")
                check_chat(message, chat_thread_id)
        elif message.content_type == 'sticker':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_sticker(chat_all_id, message.sticker.file_id, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_sticker(cur_user, message.sticker.file_id)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_sticker(chat_all_id, message.sticker.file_id, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_sticker(cur_user, message.sticker.file_id)
                check_chat(message, chat_thread_id)
        elif message.content_type == 'video_note':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_video_note(chat_all_id, message.video_note.file_id, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_video_note(cur_user, message.video_note.file_id)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_video_note(chat_all_id, message.video_note.file_id, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_video_note(cur_user, message.video_note.file_id)
                check_chat(message, chat_thread_id)
        elif message.content_type == 'location':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_location(chat_all_id, message.location.latitude, message.location.longitude, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_location(cur_user, message.location.latitude, message.location.longitude)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_location(chat_all_id, message.location.latitude, message.location.longitude, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_location(cur_user, message.location.latitude, message.location.longitude)
                check_chat(message, chat_thread_id)
        elif message.content_type == 'contact':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_contact(chat_all_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_contact(cur_user, message.contact.phone_number, message.contact.first_name,
                                         message.contact.last_name)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_contact(chat_all_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name, message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_contact(cur_user, message.contact.phone_number, message.contact.first_name,
                                         message.contact.last_name)
                check_chat(message, chat_thread_id)
        elif message.content_type == 'venue':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_venue(chat_all_id, message.venue.location.latitude, message.venue.location.longitude,
                               message.venue.title, message.venue.address, message.venue.foursquare_id,
                               message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_venue(cur_user, message.venue.location.latitude, message.venue.location.longitude,
                                       message.venue.title, message.venue.address, message.venue.foursquare_id)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                message_bot2 = bot.send_venue(chat_all_id, message.venue.location.latitude, message.venue.location.longitude,
                               message.venue.title, message.venue.address, message.venue.foursquare_id,
                               message_thread_id=chat_thread_id)
                check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user != message.chat.id:
                        bot.send_message(cur_user, text, parse_mode="html")
                        bot.send_venue(cur_user, message.venue.location.latitude, message.venue.location.longitude,
                                       message.venue.title, message.venue.address, message.venue.foursquare_id)
                check_chat(message, chat_thread_id)
        elif message.content_type == 'poll':
            if content_of_reply == 'text':
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                id_pol = (
                    bot.send_poll(chat_all_id, message.poll.question, message.poll.options, message.poll.is_anonymous,
                                  message.poll.type, message.poll.allows_multiple_answers,
                                  message.poll.correct_option_id, message.poll.explanation,
                                  message.poll.explanation_entities, message.poll.open_period, message.poll.close_date,
                                  message.poll.is_closed, message_thread_id=chat_thread_id)).message_id
                check_thread([message_bot1.message_id, id_pol], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user == message.chat.id:
                        bot.send_message(cur_user, "Проголосуй тут пожалуйста", parse_mode="html")
                        bot.forward_message(cur_user, chat_all_id, id_pol)
                        continue
                    bot.send_message(cur_user, text, parse_mode="html")
                    bot.forward_message(cur_user, chat_all_id, id_pol)
                check_chat(message, chat_thread_id)
            else:
                text = f'Ответ на {type_of_files[content_of_reply]} от {sign_replied}, {date_mc}\n\n{sign_sender}\n{caption_of_message}'
                message_bot1 = bot.send_message(chat_all_id, text, message_thread_id=chat_thread_id, parse_mode="html")
                id_pol = (
                    bot.send_poll(chat_all_id, message.poll.question, message.poll.options, message.poll.is_anonymous,
                                  message.poll.type, message.poll.allows_multiple_answers,
                                  message.poll.correct_option_id, message.poll.explanation,
                                  message.poll.explanation_entities, message.poll.open_period, message.poll.close_date,
                                  message.poll.is_closed, message_thread_id=chat_thread_id)).message_id
                check_thread([message_bot1.message_id, id_pol], chat_thread_id)
                for cur_user in users_in_chat:
                    if cur_user == message.chat.id:
                        bot.send_message(cur_user, "Проголосуй тут пожалуйста", parse_mode="html")
                        bot.forward_message(cur_user, chat_all_id, id_pol)
                        continue
                    bot.send_message(cur_user, text, parse_mode="html")
                    bot.forward_message(cur_user, chat_all_id, id_pol)
                check_chat(message, chat_thread_id)

    elif message.content_type == 'audio':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot = bot.send_audio(chat_all_id, message.audio.file_id, text, message_thread_id=chat_thread_id, parse_mode="html")
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_audio(cur_user, message.audio.file_id, text, parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'photo':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot = bot.send_photo(chat_all_id, message.photo[0].file_id, text, message_thread_id=chat_thread_id, parse_mode="html")
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_photo(cur_user, message.photo[0].file_id, text, message_thread_id=chat_thread_id,
                               parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'text':
        message_bot = bot.send_message(chat_all_id, f'<b>[{users_nick_idkey[message.chat.id]}]:</b>\n{message.text}', parse_mode="html", message_thread_id=chat_thread_id)
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, f'<b>[{users_nick_idkey[message.chat.id]}]:</b>\n{message.text}',
                                 parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'video':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot = bot.send_video(chat_all_id, message.video.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_video(cur_user, message.video.file_id, caption=text, parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'voice':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot = bot.send_voice(chat_all_id, message.voice.file_id, message_thread_id=chat_thread_id, caption=text, parse_mode="html")
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_voice(cur_user, message.voice.file_id, caption=text, parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'document':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot = bot.send_document(chat_all_id, message.document.file_id, caption=text, message_thread_id=chat_thread_id, parse_mode="html")
        check_thread(message_bot.message_id, chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_document(cur_user, message.document.file_id, caption=text, parse_mode="html")
        check_chat(message, chat_thread_id)
    elif message.content_type == 'sticker':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_sticker(chat_all_id, message.sticker.file_id, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_sticker(cur_user, message.sticker.file_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'video_note':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_video_note(chat_all_id, message.video_note.file_id, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_video_note(cur_user, message.video_note.file_i)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'location':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_location(chat_all_id, message.location.latitude, message.location.latitude, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_location(cur_user, message.location.latitude, message.location.longitude)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'contact':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_contact(chat_all_id, message.contact.phone_number, message.contact.first_name, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_contact(cur_user, message.contact.phone_number, message.contact.first_name)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'animation':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_animation(chat_all_id, message.animation.file_id, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_animation(cur_user, message.animation.file_id, message_thread_id=chat_thread_id)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'venue':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        message_bot2 = bot.send_venue(chat_all_id, message.venue.location.latitude, message.venue.location.longitude,
                       message.venue.title, message.venue.address, message_thread_id=chat_thread_id)
        check_thread([message_bot1.message_id, message_bot2.message_id], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user != message.chat.id:
                bot.send_message(cur_user, text, parse_mode="html")
                bot.send_venue(cur_user, message.venue.location.latitude, message.venue.location.longitude,
                               message.venue.title, message.venue.address)
        check_chat(message, chat_thread_id)
    elif message.content_type == 'poll':
        sign_sender = f'<b>[{users_nick_idkey[message.chat.id]}]</b>'
        caption_message = '' if message.caption is None else f'{message.caption}\n'
        text = f'{sign_sender}:\n{caption_message}'
        message_bot1 = bot.send_message(chat_all_id, text, parse_mode="html", message_thread_id=chat_thread_id)
        id_pol = bot.send_poll(chat_all_id, message.poll.question, message.poll.options, True, message.poll.type,
                               message.poll.allows_multiple_answers, message.poll.correct_option_id,
                               message.poll.explanation, message.poll.explanation_entities, message.poll.open_period,
                               message.poll.close_date, message.poll.is_closed,
                               message_thread_id=chat_thread_id).message_id
        check_thread([message_bot1.message_id, id_pol], chat_thread_id)
        for cur_user in users_in_chat:
            if cur_user == message.chat.id:
                bot.send_message(cur_user, "Проголосуй пожалуйста тут:", parse_mode="html")
                bot.forward_message(cur_user, chat_all_id, id_pol)
                continue
            bot.send_message(cur_user, text, parse_mode="html")
            bot.forward_message(cur_user, chat_all_id, id_pol)
        check_chat(message, chat_thread_id)
    else:
        bot.send_message('me', f'Новый тип сообщения{message.content_type}')
        bot.send_message(message.chat.id, 'Неверный тип сообщения')
        check_chat(message, chat_thread_id)


def check_chat(message, id):
    if id == chat_theme_flood:
        bot.register_next_step_handler(message, flood)
    elif id == chat_theme_friends:
        bot.register_next_step_handler(message, friend_chat)
    elif id == chat_theme_hw:
        bot.register_next_step_handler(message, hw_chat)
    else:
        pass


def direct_message(message):  # Получение id для sms
    id_user_for_sms = message.text
    bot.send_message(message.chat.id, 'Введите текст')
    bot.register_next_step_handler(message, direct_message_send, id_user_for_sms)


def direct_message_send(message, id_user_for_sms):  # Отправка смс
    global is_in_chat
    try:
        bot.send_message(users_nick_nickkey[id_user_for_sms],
                         f'Вам пришло личное сообщение от <b>[{users_nick_idkey[message.chat.id]}]:</b>\n\n{message.text}',
                         parse_mode='HTML')
    except KeyError:
        bot.send_message(message.chat.id, 'Неверный id')

    if is_in_chat:  # Проверка нахождения в чате
        bot.send_message(message.chat.id, 'Продолжайте общение')
        check_chat(message, cur_theme)
    else:
        bot.register_next_step_handler(message, get_command)


# bot.polling(none_stop=True, interval=0, skip_pending=True)  # debug mode

while True:
    try:
        bot.polling(none_stop=True, interval=0, skip_pending=True)
    except Exception as e:
        try:
            if str(e) == 'division by zero':
                bot.send_message('-1001655602242', '<b>[!Перезагрузка Бота!]\n</b>', parse_mode='HTML')
                print("Перезагрузка Бота\n")
            else:
                bot.send_message('-1001655602242', '<b>[!БОТ ЛЁГ!]\n</b>' + str(e), parse_mode='HTML')
                print("БОТ ЛЁГ!\n", e)
        except Exception as e:
            continue
        continue
