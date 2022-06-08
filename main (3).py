import telebot
import db
import os.path
from telebot import types
bot = telebot.TeleBot('5304790182:AAE7wyYy1lu3n6N2y9pHERDfxmRIbMtEKcQ')
db = db.Database("data")

curr_num = ''
place = ''
curr_name = ''


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_add = types.InlineKeyboardButton(text='Добавить оборудование', callback_data='add')
    keyboard.add(key_add)
    key_find = types.InlineKeyboardButton(text='Найти оборудование', callback_data='find')
    keyboard.add(key_find)
    key_set = types.InlineKeyboardButton(text='Указать местоположение оборудования', callback_data='set')
    keyboard.add(key_set)
    key_del = types.InlineKeyboardButton(text='Удалить оборудование', callback_data='del')
    keyboard.add(key_del)
    return keyboard


@bot.message_handler(content_types=['text'])
def start(message):
    mess = message.text.lower()
    if (mess == "найти") or (mess == "find"):
        bot.send_message(message.chat.id, text = "Введите строку для поиска")
        bot.register_next_step_handler(message, find_handler)
    elif(mess == "добавить") or (mess == "add"):
        bot.send_message(message.chat.id, text = "Введите инвенторный номер")
        bot.register_next_step_handler(message, add_handler_num)
    else:
        bot.send_message(message.from_user.id, text="Что хотите сделать?", reply_markup=get_main_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "find":
        bot.send_message(call.message.chat.id, 'Введите строку для поиска')
        bot.register_next_step_handler(call.message, find_handler)
    elif call.data == "set":
        bot.send_message(call.message.chat.id, 'Введите инвентарный номер')
        bot.register_next_step_handler(call.message, set_handler_num)
    elif call.data == "del":
        bot.send_message(call.message.chat.id, 'Введите инвентарный номер или название оборудование')
        bot.register_next_step_handler(call.message, del_files)
    elif call.data == "set_yes":
        db.save_place(curr_num, place)
        bot.send_message(call.message.chat.id, 'Сохранено', reply_markup=get_main_keyboard())
        start(call.message)
    elif call.data == "set_no":
        start(call.message)
    elif call.data == "add":
        bot.send_message(call.message.chat.id, 'Введите инвентарный номер')
        bot.register_next_step_handler(call.message, add_handler_num)
    elif call.data == "add_yes":
        db.save_item(curr_num, curr_name)
        db.save_place(curr_num, place)
        bot.send_message(call.message.chat.id, 'Сохранено', reply_markup=get_main_keyboard())
        start(call.message)
    elif call.data == "add_no":
        start(call.message)




def find_handler(message):
    search_string = message.text.lower()
    items = db.find_item(search_string)
    if type(items) == list:
        bot.send_message(message.chat.id, f"{items[0]}: 1")
    else:
        bot.send_message(message.chat.id, "0")
        
def del_files(message):
    obj_dell = message.text.lower()
    _del = db.del_file(obj_dell)
    bot.send_message(message.chat.id, text = 'Удаленно' + ":" + _del, reply_markup=get_main_keyboard())


def set_handler_num(message):
    global curr_num
    curr_num = message.text
    bot.send_message(message.chat.id, 'Где вы это нашли?')
    bot.register_next_step_handler(message, set_handler_place)


def set_handler_place(message):
    global place
    place = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='set_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='set_no')
    keyboard.add(key_no)
    question = 'Оборудование: ' + curr_num + '\nМесто: ' + place
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def add_handler_num(message):
    global curr_num
    curr_num = message.text
    check_file = os.path.exists('data/catalog.txt')
    if check_file  == True:
        listt=[]
        cat = open("data/catalog.txt", "r", encoding="utf=8")
    
        for i in cat:
            end = i.split("\t")[0]
            listt.append(end)
        try:
            def dist(x):
                return(x[0])
            filtered = list(filter(lambda  x: dist(x) == curr_num, listt))
            for o in filtered:
                sett = list(o)
            print(sett[0])
        except NameError:
            bot.send_message(message.chat.id, "Номер свободин. Введите название оборудования.",)
            bot.register_next_step_handler(message, add_handler_name)

        else:
            bot.send_message(message.chat.id, "Занято, выберите другой номер.")
            bot.register_next_step_handler(message, add_handler_num)
    else:
        bot.send_message(message.chat.id, "Номер свободин. Введите название оборудования.",)
        bot.register_next_step_handler(message, add_handler_name)




    

def add_handler_name(message):
    global curr_name
    curr_name = message.text.lower()
    bot.send_message(message.chat.id, 'Где это лежит?')
    bot.register_next_step_handler(message, add_handler_place)


def add_handler_place(message):
    global place
    place = message.text.lower()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='add_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='add_no')
    keyboard.add(key_no)
    question = 'Оборудование: ' + curr_num \
               + '\nНазвание: ' + curr_name \
               + '\nМесто: ' + place
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
