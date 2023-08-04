import telebot
import requests
from config import Token

bot = telebot.TeleBot(Token())

def shorten_url(url):
    api_url = "https://clck.ru/--"
    response = requests.post(api_url, data={'url': url})
    if response.status_code == 200:
        short_url = response.text
        return short_url
    else:
        print(f"Failed to shorten URL. Status code: {response.status_code}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, <b>{message.from_user.full_name}</b>!\n Отправь мне ссылку, и я сокращу её через Яндекс Кликер.", parse_mode='html')

@bot.message_handler(func=lambda message: True)
def shorten_link(message):
    if message.text.startswith("http://") or message.text.startswith("https://"):
        short_url = shorten_url(message.text)
        if short_url:
            bot.reply_to(message, short_url)
        else:
            bot.reply_to(message, "Произошла ошибка при сокращении ссылки.")
    else:
        bot.reply_to(message, "Извините, я могу обрабатывать только ссылки, начинающиеся с http:// или https://.")

bot.polling()
