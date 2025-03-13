import os
import telebot
from telebot import types
import requests
import json
from currency_converter import CurrencyConverter
import currencyapicom
from dotenv import load_dotenv

load_dotenv()

#Weahter site API
API_W = os.getenv('WEATHER_API_KEY')
API_CUR = os.getenv('CURRENCY_API_KEY')

# Telegram bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#Bot commands
command_list = [
    "/help - to check list of commands.",
    "/social_media - to check creator instagram.",
    "/weather - to check weather.",
    "/currency - to calculate your amount of your value."
]


#Command /start
@bot.message_handler(commands=['start'])
def Hello_message(message):
  bot.send_message(
      message.chat.id,
      f"Hello what can i do for you {message.from_user.first_name}?\nType /help to check list of commands."
  )


#Command /help:
#Give list of all commands for user
@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, "Here is the list of commands:")
  for i in range(len(command_list)):
    bot.send_message(message.chat.id, command_list[i])


#Command /social_media:
#Give user link to creator instagram
@bot.message_handler(commands=['social_media'])
def creator_instagram(message):
  markup = types.InlineKeyboardMarkup()
  markup.add(
      types.InlineKeyboardButton(
          "Creator instagram",
          url=
          "https://www.instagram.com/wand.erlust_zero_?igsh=bnQ1NnQ1bXN1MG0y&utm_source=qr"
          ))
  bot.send_message(message.chat.id,
                   "This is page of my creator you.\nPlease subscrube to him!",
                   reply_markup=markup)


#Command /weather:
#Show weather for user in users chosen city
@bot.message_handler(commands=['weather'])
def weather(message):
  bot.send_message(message.chat.id, "Please enter your city name")
  bot.register_next_step_handler(message, get_city)


def get_city(message):
  city = message.text.strip().lower()
  res = requests.get(
      f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_W}&units=metric'
  )  #request for weahter site API

  if res.status_code == 200:  #if status code is done
    data = json.loads(res.text)
    bot.send_message(message.chat.id,
                     f"Temperature in {city} is {data['main']['temp']} C.")
  else:
    bot.send_message(
        message.chat.id,
        "Sorry, I couldn't find the weather information for that city.")


#Command /currency:
#Calculate user amount of value in another currency
@bot.message_handler(commands=['currency'])
def value(message):
  bot.send_message(message.chat.id, "Please enter your summ.")
  bot.register_next_step_handler(message, summ)



def summ(message):
  global amount
  try:
    amount = int(message.text)
  except ValueError:
    bot.send_message(message.chat.id, "Please enter right summ.\nTry again: /currency.")
    bot.register_next_step_handler(message, summ)
    return
  if amount > 0:
    markup = types.InlineKeyboardMarkup(row_width=2)
    but1 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
    but2 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
    but3 = types.InlineKeyboardButton('EUR/CZK', callback_data='EUR/CZK')
    but4 = types.InlineKeyboardButton('CZK/EUR', callback_data='CZK/EUR')
    but5 = types.InlineKeyboardButton('USD/CZK', callback_data='USD/CZK')
    but6 = types.InlineKeyboardButton('CZK/USD', callback_data='CZK/USD')
    but7 = types.InlineKeyboardButton('Other option', callback_data='other')
    markup.add(but1, but2, but3, but4, but5, but6, but7)
    bot.send_message(message.chat.id,
                     "Please choose option:",
                     reply_markup=markup)
  else:
    bot.send_message(message.chat.id, "Summ must be heighter than 0.\nTry again: /currency.")
    bot.register_next_step_handler(message, summ)

def other_option(message):
  
      client = currencyapicom.Client(f'{API_CUR}')
      curr = CurrencyConverter()
      values = message.text.upper().split('/')
      if values[0] == 'UAH':
        result = client.latest(base_currency=[values[0]], currencies=[values[1]])
        res1 = result["data"][values[1]]['value']
        res = res1 * amount
        res = round(res, 2)
        bot.send_message(message.chat.id,
                        f'{amount}{values[0]} = {res}{values[1]}')
        
      elif values[1] == 'UAH':
        result = client.latest(base_currency=[values[0]], currencies=[values[1]])
        res1 = result["data"][values[1]]['value']
        res = res1 * amount
        res = round(res, 2)
        bot.send_message(message.chat.id,
                        f'{amount}{values[0]} = {res}{values[1]}')
        
      else:
        res = curr.convert(amount, values[0], values[1])
        res = round(res, 2)
        bot.send_message(message.chat.id,
                        f'{amount}{values[0]} = {res}{values[1]}')

#Callback function for currency
@bot.callback_query_handler(func=lambda call: True)
def curr(call):
  if call.data == 'other':
    bot.send_message(call.message.chat.id, 'Write your option like this:\nExp_curr/exp_curr_2')
    bot.register_next_step_handler(call.message, other_option)
  else:
    curr = CurrencyConverter()
    values = call.data.upper().split('/')
    res = curr.convert(amount, values[0], values[1])
    res = round(res, 2)
    bot.send_message(call.message.chat.id,
                    f'{amount}{values[0]} = {res}{values[1]}')



#Answear for some regulare questions or texst
@bot.message_handler(content_types=['text'])
def message_reply(message):
  message.text = message.text.lower()
  if message.text == "hello" or message.text == "hi":
    bot.send_message(message.chat.id, f"Hi {message.from_user.first_name}")
  elif message.text == "how are you?":
    bot.send_message(message.chat.id, "I am fine")


bot.polling()
