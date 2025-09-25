import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n /show_city <city_name> - Показать город на карте\n /remember_city <city_name> - Запомнить город\n /show_my_cities - Показать все запомненные города")
    # Допиши команды бота
    

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    # Реализуй отрисовку города по запросу
    user_id = message.chat.id
    manager.create_grapf(f'{user_id}_map.png', [city_name])
    with open (f'{user_id}_map.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    if cities:
        
        manager.create_grapf(f'{message.chat.id}_map.png',cities)
        with open (f'{message.chat.id}_map.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Ты еще не добавил ни одного города!')

@bot.message_handler(commands=['time'])
def handle_time(message):
    city_name = message.text.split()[-1]
    timezone = manager.get_time(city_name)
    if timezone:
        bot.send_message(message.chat.id, f'Текущее время в {city_name}: {timezone}')
    else:
        bot.send_message(message.chat.id, 'Не удалось определить время для этого города. Убедись, что он написан на английском!')

        
if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
