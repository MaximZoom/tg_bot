import config
import telebot
from func import get_translation
import requests
from telebot import types


bot = telebot.TeleBot(config.token)

########################################################## START
@bot.message_handler(commands=['start'])
def start(message):
    send = bot.send_message(message.chat.id, 'What is your name?')
    bot.register_next_step_handler(send, hello)


def hello(message):
    bot.send_message(message.chat.id, 'Hello, {name}. Glad to see you.'.format(name=message.text))

########################################################## HELP
    
@bot.message_handler(commands=['help'])
def helps(message):
    bot.send_message(message.chat.id, 'If you have any questions about PA2Bot, you can write to one of the developers:\n Medvedinca: https://bit.ly/2HL5cCA \n ZooM: https://bit.ly/2r94kS3 "' )

########################################################## COMMANDS

@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id,'Command list: \n 1)/translate')

##########################################################  TRANSLATER  

@bot.message_handler(commands=['translate'])
def translate(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['English', 'Russian','German']])
    send=bot.send_message(message.chat.id, 'Выберите язык в который хотите перевести текст.',reply_markup=keyboard)
    
    bot.register_next_step_handler(send, htrans)
    

def htrans(message):
    if message.text=='English':
        send=bot.send_message(message.chat.id, 'Введите текст')
        bot.register_next_step_handler(send, en)
    elif message.text=='Russian':
        send=bot.send_message(message.chat.id, 'Введите текст')
        bot.register_next_step_handler(send, ru)
    elif message.text=='German':
        send=bot.send_message(message.chat.id, 'Введите текст')
        bot.register_next_step_handler(send, de)

           
def en(message):

    bot.send_message(message.chat.id, *get_translation(message.text,'en')['text'])

def ru(message):
    
    bot.send_message(message.chat.id, *get_translation(message.text,'ru')['text'])    
    
def de(message):
    
    bot.send_message(message.chat.id, *get_translation(message.text,'de')['text'])      

##########################################################

bot.polling(none_stop=True)
