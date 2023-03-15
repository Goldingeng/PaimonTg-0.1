import lib
import banner
import telebot
from datetime import datetime
import sqlite3
import traceback
import random

db = "/root/qwerty/bd/db"
bot = ("5409304847:AAGtNYiN8p_GtHzvYZLQB6S6oGG2sMAwHv0")
client = telebot.TeleBot(token = bot)


@client.message_handler(commands=["рег"])
def reg(message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        if lib.is_user_registered(user_id):
            client.send_message(chat_id=message.chat.id, text="Ты уже зарегистрирован!\n Если что-то не понятно, напиши /помощь!", reply_to_message_id = message.message_id)
        else:
           lib.db_table_val(user_id = user_id, user_name = user_name)
           client.send_message(chat_id = message.chat.id, text = "Добро пожаловать в симулятор круток! :) \nЕсли что-то не понятно, напиши /помощь", reply_to_message_id = message.message_id)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text= f"Упс. Отправь это @ALMMST {e}", reply_to_message_id = message.message_id)


@client.message_handler(commands=["имя"])
def name(message):
    try:
        user_id = message.from_user.id
        args = message.text.split()[1:]
        user_name = ' '.join(args)
        if lib.is_user_registered(user_id):
            if len(user_name) < 15:
                lib.name(us_name=user_name, us_id=user_id)
                client.send_message(chat_id=message.chat.id, text=f"Твое имя изменено на {user_name}!", reply_to_message_id=message.message_id)
                acc(message=message)
            else:
                client.send_message(chat_id=message.chat.id, text=f"Имя слишком длинное! Не более 15 символов.", reply_to_message_id=message.message_id)
        else:
           reg(message)
           name(message)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text=f"Упс. Отправь это @ALMMST {e}", reply_to_message_id=message.message_id)


@client.message_handler(commands=["акк"])
def acc(message):
    try:
        user = message.from_user
        user_id = user.id
        user_name = user.username
        if lib.is_user_registered(user_id):
            account_info, characters = lib.acc(user_id)
            acc = lib.send_account_info(account_info, characters)
            user_avatar = client.get_user_profile_photos(user_id).photos[0][-1]
            file_info = client.get_file(user_avatar.file_id)
            downloaded_file = client.download_file(file_info.file_path)
            client.send_photo(chat_id = message.chat.id, photo = downloaded_file, caption = acc, reply_to_message_id = message.message_id)
        else:
            reg(message)
            acc(message)
    except Exception as e:
        print(e)

@client.message_handler(commands=["еже"])
def money(message):
    try:
        user_id = message.from_user.id
        if lib.is_user_registered(user_id):
            client.send_message(chat_id=message.chat.id, text = lib.add_to_wallet(user_id = user_id))
            acc(message = message)
        else:
            reg(me)
            money(message)
    except Exception as e:
        None

class Banner:
    def banner_day(self):
        global db
        with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
            day = datetime.now().day
            error_day = [7, 8, 15, 16, 24, 26, 31]
            if day in error_day:
                banner1 = random.choice([x for x in range(31) if x not in error_day])
            else:
                target = day
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM characters')
                column_names = [description[0] for description in cursor.description]
                banner1 = column_names[target]
            return banner1

banner_obj = Banner()

@client.message_handler(commands=["баннер"])
def banner2(message):
    try:
        banner_data = banner_obj.banner_day()
        banner_name = banner_data
        client.send_message(chat_id=message.chat.id, text = banner_obj.banner_day(), reply_to_message_id = message.message_id)
    except Exception as e:
        print(e)


@client.message_handler(commands=["крутка"])
def twist(message):
    try:
        user_id = message.from_user.id
        if lib.is_user_registered(user_id):
            with open('banner1.jpg', 'rb') as photo:
                client.send_photo(chat_id=message.chat.id, photo=photo, caption = banner.twist(user_id), reply_to_message_id = message.message_id)
            acc(message = message)
        else:
            reg(message)
            twist(message)
    except Exception as e:
        print(e )


@client.message_handler(commands=["промо"])
def promo(message):
    try:
        user_id = message.from_user.id
        if lib.is_user_registered(user_id):
            client.send_message(chat_id = message.chat.id, text = lib.promo_status(user_id), reply_to_message_id = message.message_id)
        else:
            reg(message)
            promo(message)
    except Exception as e:
        print(e)


@client.message_handler(commands=["шанс"])
def chance(message):
    try:
        user_id = message.from_user.id
        if lib.is_user_registered(user_id):
            client.send_message(chat_id = message.chat.id, text = lib.chance(user_id), reply_to_message_id = message.message_id)
            acc(message = message)
        else:
            reg(message)
            chance(message)
    except Exception as e:
        print(e)


@client.message_handler(commands=["кости"])
def bones(message):
    try:
        user_id = message.from_user.id
        bid = message.text.split()[1:]
        number = ' '.join(bid)
        number = int(number)
        if lib.is_user_registered(user_id):
            client.send_message(chat_id = message.chat.id, text = lib.bones(user_id, number), reply_to_message_id = message.message_id)
            acc(message)
        else:
            reg(message)
            bones(message)
    except Exception as e:
        print(e)
        
@client.message_handler(commands=["start"])
def help(message):
    try:
        us_id = message.from_user.id
        client.send_message(chat_id=message.chat.id, text = """


Автор бота: @ALMMST
ТГ канал бота: @bannersim

Привет! Этот бот - симулятор круток из геншин. 
Снизу приведен список всех команд. Все механики приблежены к механикам из геншина.

Команды:
/рег - регестрация
/еже - ежечасовая награда (от 30 до 1600)
/шанс - возможность приумножить примогемы. Осторожно....)
/аккаунт - просмотр аккаунта
/имя "Ваше имя" - смена имени. Не более 15 символов
/баннер - просмотр баннера сейчас
/крутка - 10 круток
/промо - промокод на примогемы. От 1 до 5К


Структура аккаунта:

Имя - твое имя
Примогемы - твои примогемы
История круток - крутки после легендарки
Гарант - гарант на лимитированного персонажа дня

Струтура крутки:

Первое сообщение - то что тебе выпало
Второе сообщение - итоги обновления твоего аккаунта
        """)
    except Exception as e:
        print("Ошибка при оказании помощи!" + e)
        
@client.message_handler(commands=["помощь"])
def help(message):
    try:
        us_id = message.from_user.id
        client.send_message(chat_id=message.chat.id, text = """


Автор бота: @ALMMST
ТГ канал бота: @bannersim

Привет! Этот бот - симулятор круток из геншин. 
Снизу приведен список всех команд. Все механики приблежены к механикам из геншина.

Команды:
/рег - регестрация
/еже - ежечасовая награда (от 30 до 1600)
/шанс - возможность приумножить примогемы. Осторожно....)
/аккаунт - просмотр аккаунта
/имя "Ваше имя" - смена имени. Не более 15 символов
/баннер - просмотр баннера сейчас
/крутка - 10 круток
/промо - промокод на примогемы. От 1 до 5К


Структура аккаунта:

Имя - твое имя
Примогемы - твои примогемы
История круток - крутки после легендарки
Гарант - гарант на лимитированного персонажа дня

Струтура крутки:

Первое сообщение - то что тебе выпало
Второе сообщение - итоги обновления твоего аккаунта
        """)
    except Exception as e:
        print("Ошибка при оказании помощи!" + e)


try:
    client.polling(none_stop=True)
except:
    None
