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
        bot.send_message(message.chat.id,'Command list: \n 1)/translate - translates the entered text  \n 2)/language - changes the language  \n 3)/help - help \n 4)/wlvl -  water level in the Biya river \n 5)/course - course USD EUR BTC in rubles \n 6)/weather - weather in Biysk')
    elif l=='Russian':
         bot.send_message(message.chat.id,'Список команд: \n 1)/translate - переводчик введенного текста  \n 2)/language - смена языка интерфейса  \n 3)/help - помощь \n 4)/wlvl -  уровень воды в реке Бия \n 5)/course - курсы USD EUR BTC к рублю \n 6)/weather - погода в Бийске')
        

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

########################################################## COURSE            

@bot.message_handler(commands=['course']) 
def course(message): 
    url = config.bank 
    page = requests.get(url) 
    soup = BeautifulSoup(page.text, 'html.parser') 
    usd = soup.find_all('td')[3].get_text() 
    eur = soup.find_all('td')[8].get_text() 
    url = config.bitcoin 
    page = requests.get(url) 
    soup = BeautifulSoup(page.text, 'html.parser') 
    btc = soup.find_all(class_='pretty-sum')[2].get_text()

    if l=='English':
        bot.send_message(message.chat.id, 'Courses:\n USD: ' + usd + ' RUB\n EUR: ' + eur + ' RUB\n BTC: ' + btc + ' RUB')

    elif l=='Russian':
        bot.send_message(message.chat.id, 'Курсы:\n USD: ' + usd + ' RUB\n EUR: ' + eur + ' RUB\n BTC: ' + btc + ' RUB')

########################################################## WEATHER

@bot.message_handler(commands=['weather']) 
def weather(message): 
    url = config.weather 
    page = requests.get(url) 
    soup = BeautifulSoup(page.text, 'html.parser') 
    state = soup.find_all(class_='today_nowcard-phrase')[0].get_text() 
    temp = soup.find_all(class_='today_nowcard-temp')[0].get_text() 
    feels = soup.find_all(class_='deg-feels')[0].get_text() 
    wind = soup.find_all('td')[0].get_text() 
    wet = soup.find_all('td')[1].get_text()

    if l=='English':
        bot.send_message(message.chat.id, 'Current weather condition:\n Temperature: ' + temp + '\n State: ' + state + '\n By sensation: ' + feels + '\n Wind: ' + wind + '\n Wet: ' + wet)

    elif l=='Russian':
         bot.send_message(message.chat.id, 'Текущее состояние погоды:\n Температура: ' + temp + '\n Состояние: ' + state + '\n По ощущениям: ' + feels + '\n Ветер: ' + wind + '\n Влажность: ' + wet)

##########################################################
bot.polling(none_stop=True)
