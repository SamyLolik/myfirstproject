import requests
import telebot
from telebot import types
import const

bot = telebot.TeleBot(const.TELEGRAM_API_TOKEN)

location = ''
category = ''
subcategory = ''
def get_json(url):
    return requests.get(url).json()


def get_palaces(kwargs):
    return 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + kwargs['location'] \
           + '&radius=' + str(kwargs['radius']) \
           + '&type=' + kwargs['type'] \
           + '&language=' + kwargs['language'] \
           + '&key=' + const.GOOGLE_API_KEY


def get_info(location, type):
    return {
        'location': location,
        'radius': 1000,
        'type': type,
        'language': 'ru'
    }


def funk(message):
    global subcategory
    if message.text == 'Туризм':
        print(message.text)
        subcategory = 'tourism'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Парки',
                                                               'Музеи',
                                                               'Арт галереи',
                                                               'Зоопарки',
                                                               'Кемпинги',
                                                               'Церкви',
                                                               'Ночлег',
                                                               'Тур агенства'
                                                               ]])
        msg = bot.send_message(message.chat.id, 'Выбирай скорее категорию, дружище, и погнали!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, main)
    elif message.text == 'Покушать/Попить':
        subcategory = 'eating'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Кафе',
                                                                'Бары',
                                                                'Еда',
                                                                'Здоровье',
                                                                'Рестораны',
                                                                'Доставка еды',
                                                                'Булочные',
                                                                'Ночные клубы'
                                                               ]])
        msg = bot.send_message(message.chat.id, 'Выбирай скорее категорию, дружище, и погнали!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, main)
    elif message.text == 'Шопинг':
        subcategory = 'shopping'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Магазины одежды',
                                                                'Все магазины',
                                                                'Магазины электроники',
                                                                'Товары для дома',
                                                                'Цветочные',
                                                                'Супермаркеты'
                                                               ]])
        msg = bot.send_message(message.chat.id, 'Выбирай скорее категорию, дружище, и погнали!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, main)
    elif message.text == 'Досуг':
        subcategory = 'leisure'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['СПА',
                                                                'Здоровье',
                                                                'Кинотеатры',
                                                                'Боулинг',
                                                                'Салоны красоты'
                                                               ]])
        msg = bot.send_message(message.chat.id, 'Выбирай скорее категорию, дружище, и погнали!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, main)


def main(msg):
    global category, subcategory
    print('category={}'.format(category))
    print('subcategory={}'.format(subcategory))
    category = const.KEY_WORDS[subcategory][msg.text]
    info = get_info(location, category)
    json = get_json(get_palaces(info))
    if json['status'] == 'OK':
        for data in json['results'][:5]:
            coordinate = data['geometry']['location']
            name = data['name']
            address = data['vicinity']
            bot.send_venue(msg.chat.id,
                           coordinate['lat'],
                           coordinate['lng'],
                           name,
                           address)
            print('Координаты {}\nИмя {}\nАдресс {}'.format(coordinate, name, address))
            print('-------------------------------------------------------------------------------------')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Да', 'Нет']])
        answer = bot.send_message(msg.chat.id, 'Хочешь попробовать снова?', reply_markup=keyboard)
        bot.register_next_step_handler(answer, again)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Да', 'Нет']])
        answer = bot.send_message(msg.chat.id, 'В какое же днище ты забрался, рядом ничего нет!\n'
                                               'Хочешь попробовать снова?', reply_markup=keyboard)
        bot.register_next_step_handler(answer, again)


def again(message):
    if message.text == 'Да':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_coordinate = types.KeyboardButton(text='Отправить местоположение', request_location=True)
        keyboard.add(btn_coordinate)
        bot.send_message(message.chat.id, 'Отправь мне координаты и начнем', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Ну ты, это, пиши есичо')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_coordinate = types.KeyboardButton(text='Отправить местоположение', request_location=True)
    keyboard.add(btn_coordinate)
    bot.reply_to(message, 'Привет! Я есть БОТ! И я покажу тебе ближайшие крутые места!\n'
                          , reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Готов помочь тебе, друг!\n'
                          'Смотри... Жмешь на интересующую тебя тему, подтверждаешь отправку местоположения и '
                          'смотришь кучу мест вокруг тебя по заданной тематике!\n'
                          'Я работаю в любом городе любой страны(!!!) в радиусе 1000 метров от тебя',
                 )


@bot.message_handler(func=lambda message: True, content_types=['location'])
def shop_location(message):
    print(message)
    global location
    location = str(str(message.location.latitude) + ',' + str(message.location.longitude))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Туризм', 'Покушать/Попить', 'Шопинг', 'Досуг']])
    msg = bot.send_message(message.chat.id, 'Выбирай скорее категорию, дружище, и погнали!', reply_markup=keyboard)
    #funk(msg, location)
    bot.register_next_step_handler(msg, funk)


'''
@bot.message_handler(content_types=["text"])
def any_msg(msg):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Да', 'Нет']])
    answer = bot.send_message(msg.chat.id, 'Хочешь попробовать снова?', reply_markup=keyboard)
    bot.register_next_step_handler(answer, again)
'''

if __name__ == '__main__':
    bot.polling()
