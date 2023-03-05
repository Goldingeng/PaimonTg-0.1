import random
import datetime
import sqlite3

db = "/root/qwerty/bd/db"
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
        cursor.execute("INSERT INTO characters (Albedo, Al Haytham, Ayaka, Ayato, Venti, Gan Yu, Jean, Dilyuk, Ye Lan, Yaimiya, Itto, Kadzuha, Klee, Kokomi, Ke Qing, Mona, Nahida, Nile, Raiden, Sayno, Wanderer, Xiao, Tartaglia, Tignari, Hu Tao, Qiqi, ZhongLi, Shen He, Eola, Ya Miko, user_id_characters) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, user_id,))
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
┃Имя пользователя: {account_info[0]}🟢
┃Примогемы: {account_info[1]}❇️
┃История круток: {account_info[3]}📗
┃Гарант:{guarantee}☯️
--------------------------------
{characters}
"""
    else:
        message_account_info = "Пользователь не найден"
    return message_account_info


def promo_status(user_id):
    global db
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT promo FROM users WHERE user_id = ?", (user_id,))
        status_prom = cursor.fetchone()[0]
        if status_prom == 1:
            amount = random.randint(1, 5000)
            cursor.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
            cursor.execute("UPDATE users SET promo = 0 WHERE user_id = ?", (user_id))
            conn.commit()
            answer = f"Успешно! Ты получил: {amount} примогемов!"
        else:
            answer = "Халявы не будет."
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
        
        return "▶️ Ты уже запрашивал награду. Попробуй через час! 🕐"
