import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    send = bot.send_message(message.chat.id, 'What is your name?')
    bot.register_next_step_handler(send, hello)


def hello(message):
    bot.send_message(message.chat.id, 'Hello, {name}. Glad to see you.'.format(name=message.text))


@bot.message_handler(commands=['help'])
def helps(message):
    bot.send_message(message.chat.id, 'If you have any questions about PA2Bot, you can write to one of the developers:\n Medvedinca: https://bit.ly/2HL5cCA \n ZooM: https://bit.ly/2r94kS3')



bot.polling(none_stop=True)