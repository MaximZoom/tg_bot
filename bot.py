import config
import telebot
from func import get_translation
import requests
from telebot import types
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.token)
global l
l='English'
########################################################## START

@bot.message_handler(commands=['start'])
def start(message):            
    if l=='English':
        send = bot.send_message(message.chat.id, 'What is your name?')
        bot.register_next_step_handler(send, hello)
    elif l=='Russian':
        send = bot.send_message(message.chat.id, 'Как тебя зовут?')
        bot.register_next_step_handler(send, hello)


def hello(message):
    if l=='English':
        bot.send_message(message.chat.id, 'Hello, {name}. Glad to see you.'.format(name=message.text))
    elif l=='Russian':
        bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть.'.format(name=message.text))

########################################################## LANG
    
@bot.message_handler(commands=['language'])    
def lang(message):
    keyboardd = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    if l=='English':
        keyboardd.add(*[types.KeyboardButton(name) for name in ['English', 'Russian']])
        send = bot.send_message(message.chat.id, 'Choose language.',reply_markup=keyboardd)       
        bot.register_next_step_handler(send, nlang)
       
    elif l=='Russian':
        keyboardd.add(*[types.KeyboardButton(name) for name in ['Английский', 'Русский']])
        send = bot.send_message(message.chat.id, 'Выберите язык.',reply_markup=keyboardd)
        bot.register_next_step_handler(send, nlang)
        

def nlang(message):
    global l    
    if (message.text=='English') or (message.text=='Английский') :
        l = 'English'
        bot.send_message(message.chat.id, 'You chose English.')
    elif (message.text=='Russian') or (message.text=='Русский'):
        l = 'Russian'
        bot.send_message(message.chat.id, 'Вы выбрали русский язык.')
        
########################################################## HELP
    
@bot.message_handler(commands=['help'])
def helps(message):
    if l=='English':
        bot.send_message(message.chat.id, 'If you have any questions about PA2Bot, you can write to one of the developers:\n Medvedinca: https://bit.ly/2HL5cCA \n ZooM: https://bit.ly/2r94kS3 "' )
    elif l=='Russian':
        bot.send_message(message.chat.id, 'Если у вас есть вопросы по PA2Bot, вы можете написать одному из разработчиков:\n Medvedinca: https://bit.ly/2HL5cCA \n ZooM: https://bit.ly/2r94kS3 "' )

########################################################## COMMANDS

@bot.message_handler(commands=['commands'])
def commands(message):
    if l=='English':
        bot.send_message(message.chat.id,'Command list: \n 1)/translate \n 2)/language \n 3)/help \n 4)/wlvl')
    elif l=='Russian':
        bot.send_message(message.chat.id,'Список команд: \n 1)/translate \n 2)/language \n 3)/help \n 4)/wlvl')
        

##########################################################  TRANSLATER  

@bot.message_handler(commands=['translate'])
def translate(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    if l=='English':
        keyboard.add(*[types.KeyboardButton(name) for name in ['English', 'Russian','German']])
        send=bot.send_message(message.chat.id, 'Select the language in which you want to translate the text.',reply_markup=keyboard)
        bot.register_next_step_handler(send, htrans)
    elif l=='Russian':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Английский', 'Русский','Немецкий']])
        send=bot.send_message(message.chat.id, 'Выберите язык в который хотите перевести текст.',reply_markup=keyboard)
        bot.register_next_step_handler(send, htrans)
    

    

def htrans(message):       
    if l=='English': 
        if message.text=='English':
            send=bot.send_message(message.chat.id, 'Enter text.')
            bot.register_next_step_handler(send, en)
        elif message.text=='Russian':
            send=bot.send_message(message.chat.id, 'Enter text.')
            bot.register_next_step_handler(send, ru)
        elif message.text=='German':
            send=bot.send_message(message.chat.id, 'Enter text.')
            bot.register_next_step_handler(send, de)
            
    elif l=='Russian':
        if message.text=='Английский':
            send=bot.send_message(message.chat.id, 'Введите текст.')
            bot.register_next_step_handler(send, en)
        elif message.text=='Русский':
            send=bot.send_message(message.chat.id, 'Введите текст.')
            bot.register_next_step_handler(send, ru)
        elif message.text=='Немецкий':
            send=bot.send_message(message.chat.id, 'Введите текст.')
            bot.register_next_step_handler(send, de)

           
def en(message):

    bot.send_message(message.chat.id, *get_translation(message.text,'en')['text'])

def ru(message):
    
    bot.send_message(message.chat.id, *get_translation(message.text,'ru')['text'])    
    
def de(message):
    
    bot.send_message(message.chat.id, *get_translation(message.text,'de')['text'])      

########################################################## WATER LVL

@bot.message_handler(commands=['wlvl']) 
def wlvl(message): 
    url = config.w_lvl_url 
    page = requests.get(url) 
    soup = BeautifulSoup(page.text, 'html.parser') 
    lvl = soup.find_all('b')[2].get_text()
    if l=='English':
        bot.send_message(message.chat.id, 'Water level in the Biya river: ' + lvl)

    elif l=='Russian':
        bot.send_message(message.chat.id, 'Уровень воды в реке Бия: ' + lvl)
            
    

##########################################################

bot.polling(none_stop=True)
