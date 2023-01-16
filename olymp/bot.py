import telebot
bot = telebot.TeleBot('5962720905:AAFTMSAJ0Lkvt5SQ1ljKMaIFQD4MdrFfEo0')
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')
@bot.message_handler(content_types=["text"])

def sendfile(m):
    bot.send_document(m.chat.id, open('tmp.txt', 'rb'))

def handle_text(message):
    bot.send_message(message.chat.id, sendfile(message.text))
bot.polling(none_stop=True, interval=0)