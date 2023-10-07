import time
import telebot
from telebot import types

bot = telebot.TeleBot('*') #tg token


def handle_text(message):
    print("id:", message.from_user.id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    bot.send_document(message.chat.id, open('need_stock_markets(10).txt', 'rb'))
    bot.send_document(message.chat.id, open('other_stock_markets.txt', 'rb'))


@bot.message_handler(commands=['help'])
def handle_help(message):
    print("id:", message.from_user.id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    bot.send_message(message.chat.id, '1. /start - выбор связок' + '\n' + '2. /info - информация о боте')


@bot.message_handler(commands=['info'])
def handle_help(message):
    print("id:", message.from_user.id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    bot.send_message(message.chat.id, 'Parsing of stock markets and chains of crypto currencies v1.01')


@bot.message_handler(commands=['start'])
def start(message):
    print("id:", message.from_user.id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Связки среди 10 бирж")
    btn3 = types.KeyboardButton("Цепочки из двух связок")
    btn2 = types.KeyboardButton("Все связки")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Welcome, {0.first_name}! Это бот для парсинга связок".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    print("id:", message.from_user.id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if (message.text == "Связки среди 10 бирж"):
        bot.send_message(message.chat.id, text="Связки среди 10 бирж")
        try:
            bot.send_document(message.chat.id, open('need_stock_markets(10).txt', 'rb'), caption=' Связки на Hotbit, Binance, Huobi, OKX, Bilaxy, Gate.io, Kraken, AEX, Uniswap(v2)')
        except Exception as e:
            bot.reply_to(message, 'Файл пока пуст')
    elif (message.text == "Все связки"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        try:
            bot.send_document(message.chat.id, open('other_stock_markets.txt', 'rb'), caption='All chains')
        except Exception as e:
            bot.send_message(message.chat.id, 'Файл пока пуст')
    elif (message.text == "Цепочки из двух связок"):
        try:
            bot.send_document(message.chat.id, open('double_chains.txt', 'rb'), caption='Double chains')
        except Exception as e:
            bot.send_message(message.chat.id, 'Файл пока пуст')
    else:
        bot.send_message(message.chat.id, text="Такой команды нет. Посмотрите /start")


bot.polling(none_stop=True)
