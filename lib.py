import random
import datetime
import sqlite3

db = "bd/db"
db_server = "/root/qwerty/bd/db"

#Проверка зареган ли пользователь
def is_user_registered(user_id):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
    return result is not None

#Регестрация
def db_table_val(user_id, user_name):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, user_name, wallet, guarantee, hystory, time, promo) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, user_name, 1600, 0, 1, 25, 1))
        cursor.execute("INSERT INTO characters (Albedo, Al_Haytham, Ayaka, Ayato, Venti, Gan_Yu, Jean, Dilyuk, Ye_Lan, Yaimiya, Itto, Kadzuha, Klee, Kokomi, Ke_Qing, Mona, Nahida, Nile, Raiden, Sayno, Wanderer, Xiao, Tartaglia, Tignari, Hu_Tao, Qiqi, ZhongLi, Shen_He, Eola, Ya_Miko, user_id_characters) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, user_id,))
        conn.commit()

#Смена ника
def name(us_name, us_id):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (us_name, us_id))

#Полчение данных об аккаунте
def acc(us_id):
    global db
    emoji = ["🤡","😎","👹","😄","🙄","😯","😵‍💫","🥸","🤭","🤥","👿","👽","👻","🤖","💀","🤬","🤪","😮‍💨","😦","😜","😏","🤨","😑","🙂","🥰","😁",'🤔']
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM characters WHERE user_id_characters = {us_id}")
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()

        non_null_columns = []
        for column_name, value in zip(columns[1:], result[1:]):
            if value != 0:
                non_null_columns.append((column_name, value))

        if non_null_columns:
            characters = "Персонажи и их созведия:\n\n"
            for column_name, value in non_null_columns:
                emoji_one = random.choice(emoji)
                characters += f"┃ {emoji_one} {column_name} : ⭐ {value} \n"
        else:
            characters = "У тебя нет персонажей :D"
            
        cursor.execute("SELECT user_name, wallet, guarantee, hystory FROM users WHERE user_id = ? ", (us_id,))
        account = cursor.fetchone()
        
    return account, characters

#Отправка данных об аккаунте
def send_account_info(account_info, characters=""):
    if account_info[2] == 1:
        guarantee = "Да"
    else:
        guarantee = "Нет"
    
    if account_info:
        message_account_info = f"""
┃Ник: {account_info[0]}🟢
┃Примогемы: {account_info[1]}❇️
┃История круток: {account_info[3]}📗
┃Гарант:{guarantee}☯️
--------------------------------
{characters}
Автор бота: @ALMMST
ТГ канал бота: @bannersim
"""
    else:
        message_account_info = "Пользователь не найден :("
    return message_account_info

#промокод
def promo_status(user_id):
    global db
    print("Либа")
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT promo FROM users WHERE user_id = ?", (user_id,))
        status_prom = cursor.fetchone()[0]
        if status_prom == 1:
            amount = random.randint(1, 5000)
            cursor.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
            cursor.execute("UPDATE users SET promo = ? WHERE user_id = ?", (2, user_id))
            conn.commit()
            answer = f"Успешно!\nТы получил: {amount} примогемов! ✪"
        else:
            answer = "Халявы не будет. -___-"
        return answer



#Пополнение кошелька
def add_to_wallet(user_id):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT time FROM users WHERE user_id = ?", (user_id,))
        last_request_time = cursor.fetchone()[0]
        
        if datetime.datetime.now().hour != last_request_time:
            amount = random.randint(30, 1600)
            cursor.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
            cursor.execute("UPDATE users SET time = ? WHERE user_id = ?", (datetime.datetime.now().hour, user_id))
            conn.commit()
            
            return f"▶️ Ты получил {amount} ❇️ примогемов!"
        
        return "▶️ Ты уже запрашивал награду.\nПопробуй через час! 🕐"

#шанс
def chance(user_id):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
        wallet = cursor.fetchone()[0]

        if random.randint(1, 13) == 1:
            wallet = wallet * random.randint(5, 15)
            message = f"Ого!\nТебе повезло!"
        else:
            wallet = wallet * 0
            message = f"С кем не бывает :)\nТвой счет обнулен"
        cursor.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet, user_id))
        return message

def bones(user_id, number):
    if isinstance(number, int):
        if number > 0:
            with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                wallet = cursor.fetchone()[0]
                if number <= wallet:
                    if random.randint(1, 2) == 1:
                        wallet = (number * 2) - number
                        message = f"Ого!\nТебе повезло. Ты выиграл {wallet} примогемов!"
                        cursor.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (wallet, user_id))
                    else:
                        message = f"Я выиграл. Примогемов не будет."
                        cursor.execute("UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (number, user_id))
                else:
                    message = "У тебя недостаточно примогемов!"
        else:
            message = "Число должно быть больше нуля o_0"
    else:
        message = "Введи число после команды"
    return message
