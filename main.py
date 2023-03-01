import lib
import banner
import telebot
from datetime import datetime
import sqlite3
import traceback
import random

bot = ("5409304847:AAGtNYiN8p_GtHzvYZLQB6S6oGG2sMAwHv0")
client = telebot.TeleBot(token = bot)


@client.message_handler(commands=["рег"])
def reg(message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        if lib.is_user_registered(user_id):
            client.send_message(chat_id=message.chat.id, text="Ты уже зарегистрирован! Если что то не понятно, напиши /помoщь !", reply_to_message_id=message.message_id)
        else:
            lib.db_table_val(user_id=user_id, user_name=user_name)
            client.send_message(chat_id=message.chat.id, text="Успешно! :) Если что то не понятно, напиши /помoщь", reply_to_message_id=message.message_id)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text="Что то пошло не по плану.", reply_to_message_id=message.message_id)
        print("Ошибка при регистрации пользователя:", e)

            
@client.message_handler(commands=["имя"])
def name(message):
    try:
        lib.name(us_name=message.from_user.first_name, us_id=message.from_user.id)
        client.send_message(chat_id=message.chat.id, text="Твое имя изменено!", reply_to_message_id=message.message_id)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text="Сначала регестрация, дорогуша). Напиши /рег. Если что то не понятно, напиши /помoщь")
        print("Ошибка при изменении имени пользователя:", e)


@client.message_handler(commands=["аккаунт"])
def acc(message):
    try:
        us_id = message.from_user.id
        account_info, characters = lib.acc(us_id)
        acc = lib.send_account_info(account_info, characters)
        with open('images.png', 'rb') as photo:
            client.send_photo(chat_id=message.chat.id, photo=photo, caption=acc, reply_to_message_id = message.message_id)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text="Сначала регестрация, дорогуша). Напиши /рег. Если что то не понятно, напиши /помoщь")
        print("Ошибка при получении информации об аккаунте:", e)

@client.message_handler(commands=["еже"])
def money(message):
    try:
        us_id = message.from_user.id
        client.send_message(chat_id=message.chat.id, text = lib.add_to_wallet(user_id = us_id))
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text="Сначала регестрация, дорогуша). Напиши /рег. Если что то не понятно, напиши /помoщь")
        print("Ошибка при получении примогемов!", e)

class Banner:
    def banner_day(self):
        with sqlite3.connect("/root/qwerty/bd/db", check_same_thread=False) as conn:
            day = datetime.now().day
            error_day = [8, 9, 16, 17, 25, 27, 31]
            if day in error_day:
                target = random.choice([x for x in range(31) if x not in error_day])
            else:
                target = day + 1
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM characters')
                column_names = [description[0] for description in cursor.description]
                banner = column_names[target]
            return banner

banner_obj = Banner()

@client.message_handler(commands=["баннер"])
def banner2(message):
    try:
        banner_data = banner_obj.banner_day()
        banner_name = banner_data
        client.send_message(chat_id=message.chat.id, text = banner_name, reply_to_message_id = message.message_id)
    except Exception as e:
        print("Ошибка при получении баннера", e)

@client.message_handler(commands=["крутка"])
def twist(message):
    try:
        user_id = message.from_user.id
        with open('banner1.jpg', 'rb') as photo:
            spisok = banner.twist(user_id)
            text = '\n'.join(spisok)
            client.send_photo(chat_id=message.chat.id, photo=photo, caption = f"👉{text}👻", reply_to_message_id=message.message_id)
        acc(message=message)
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text="У тебя не хватает примогемов. Иди работай! Если что-то не понятно, напиши /помощь")
        traceback.print_exc()


@client.message_handler(commands=["помощь"])
def help(message):
    try:
        us_id = message.from_user.id
        client.send_message(chat_id=message.chat.id, text = """
Команды:

/рег - регестрация
/еже - ежечасовая награда (от 30 до 1600)
/аккаунт - просмотр аккаунта
/имя - смена имени
/баннер - просмотр баннера сейчас
/крутка - 10 круток

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

client.polling(none_stop=True)
