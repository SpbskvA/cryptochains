import os
import time
import telebot
import pyscreenshot

token_prod = '6035937527:AAHf68mE5luEy9W_nxTnXs1SfUSLzeUyOAs'
bot = telebot.TeleBot(token_prod, skip_pending=True)
path = 'D:\\ProgramFiles\\sample'


# get root users from file

@bot.message_handler(
    content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'location', 'contact', 'voice',
                   'video_note', 'animation', 'poll', 'dice', 'venue', 'invoice', 'successful_payment', 'game'])
def start(message):
    if message.text == '/imr':
        xlsx = open(f'{path}/imr.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)
    if message.text == '/cusum':
        xlsx = open(f'{path}/cusum.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)
    if message.text == '/ewma':
        xlsx = open(f'{path}/ewma.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)
    if message.text == '/mewma':
        xlsx = open(f'{path}/mewma.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)
    if message.text == '/xmr':
        xlsx = open(f'{path}/xmr.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)
    if message.text == '/smr':
        xlsx = open(f'{path}/smr.jpg', 'rb')
        bot.send_photo(message.chat.id, xlsx)

while True:
    try:
        bot.polling(none_stop=True, interval=0, skip_pending=True)
    except Exception as e:
        try:
            bot.send_message('613881281', '<b>[!БОТ ЛЁГ!]\n</b>' + str(e), parse_mode='HTML')
            print("БОТ ЛЁГ!\n", e)
            time.sleep(30)
        except Exception as e:
            continue
        continue
