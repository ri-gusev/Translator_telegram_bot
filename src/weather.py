import telebot  
from telebot import types
import requests
from googletrans import Translator
import os
translator = Translator()

token = 'put your token here'
bot = telebot.TeleBot(token)



def new_file(message):
  if os.path.isfile(str(message.chat.id)+'.txt'):
    print("Файл есть")
  else:
    print("Файл создан")
    with open(str(message.chat.id)+'.txt', 'a',encoding='utf-8') as file:
      file.write("")

@bot.message_handler(commands=['start'])
def start(message):
  new_file(message)
  with open(str(message.chat.id)+'.txt', 'r',encoding='utf-8') as file:
      list_of_cities = file.readlines()

  markup = types.ReplyKeyboardMarkup()

  while len(list_of_cities)  < 4 :
        list_of_cities = '----'
  item1 = types.KeyboardButton(list_of_cities[-3])
  item2 = types.KeyboardButton(list_of_cities[-2])
  item3 = types.KeyboardButton(list_of_cities[-1])


  markup.add(item1)
  markup.add(item2)
  markup.add(item3)
  bot.send_message(message.chat.id, "Назови город, в котором хочешь узнать погоду. ",reply_markup=markup)



@bot.message_handler(content_types=['text'])
def some_func(message):
    city = message.text
    with open(str(message.chat.id)+'.txt', 'a',encoding='utf-8') as file:
      file.write(city +'\n')
    result = translator.translate(city, src='ru', dest='en') # переводим
    result = result.text # название города на английском
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + result + "&appid=" + "1e2bcd50e02258b0acd19d0612fd3bdb"
    response = requests.get(url)
    data = response.json()
    try: # попробуй
      bot.send_message(message.chat.id, f"""Город: {result}. \nТемпература: {str(int(data['main']['temp']-273))}\n
Скорость ветра: {str(int(data['wind']['speed']))} м/с
      """)
    except KeyError:  # если ошибка, то выполни код ниже
      bot.send_message(message.chat.id, f"Каких-то данных нет. ")

bot.polling()












