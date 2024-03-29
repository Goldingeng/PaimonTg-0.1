from datetime import datetime
import sqlite3
import random

db = "/root/qwerty/bd/db"

class Banner:
    def banner_day(self):
        global db
        with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
            day = datetime.now().day
            error_day = [7, 8, 15, 16, 24, 26, 31]
            banner1 = None
            if day in error_day:
                target = random.choice([x for x in range(31) if x not in error_day])
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM characters')
                column_names = [description[0] for description in cursor.description]
                banner1 = column_names[target]
            else:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM characters')
                column_names = [description[0] for description in cursor.description]
                banner1 = column_names[day]
            return banner1

banner_obj = Banner()

def twist(user_id):
    global db
    user_id = user_id
    with sqlite3.connect(f"{db}", check_same_thread=False) as conn:
        message_twist = []
        garbage = ["Парный нефрит", "Посыльный", "Потусторонняя история","Предвестник зари","Рогатка", "Руководство по магии", "Тёмный железный меч", "Филейный нож", "Холодное лезвие", "Чёрная кисть", "Эпос о драконоборцах"]
        cursor = conn.cursor()
        cursor.execute("SELECT hystory, guarantee, wallet FROM users WHERE user_id = ? ", (user_id,))
        guarantee = cursor.fetchone()
        print(guarantee)
        if guarantee[2] >= 1600:
            cursor.execute(f"SELECT wallet, hystory FROM users WHERE user_id = ?", (user_id,))
            current_value = cursor.fetchone()
            new_value = current_value[0] - 1600
            new_hystory = current_value[1] + 10
            cursor.execute("UPDATE users SET wallet = ?, hystory = ? WHERE user_id = ?", (new_value, new_hystory, user_id))
            conn.commit()
            for i in range((10)):
                if guarantee[0] >= 90:
                    if guarantee[1] == 1:
                        banner_name = banner_obj.banner_day()
                        print(banner_name)
                        cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (0, 0, user_id))
                        cursor.execute(f"SELECT {banner_name} FROM characters WHERE user_id_characters = ?", (user_id,))
                        current_value = cursor.fetchone()
                        new_value = current_value[0] + 1
                        cursor.execute(f"UPDATE characters SET {banner_name} = ? WHERE user_id_characters = ?", (new_value, user_id))
                        conn.commit()
                        message_twist.append(banner_name + "⭐⭐⭐⭐⭐")
                        break
                    else:
                        error_day = [7, 8, 15, 16, 24, 26, 31, 1, 1, 1, 1, 1, 1]
                        lega = random.choice(error_day)
                        if error_day == 1:
                            banner_data = banner_obj.banner_day()
                            banner = banner_data[0]
                            banner_name = banner_data[1]
                            cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (0, 0, user_id))
                            cursor.execute(f"SELECT {banner_name} FROM characters WHERE user_id_characters = ?", (user_id,))
                            current_value = cursor.fetchone()
                            new_value = current_value + 1
                            cursor.execute(f"UPDATE characters SET {banner_name} = ? WHERE user_id_characters = ?", (new_value, user_id))
                            conn.commit()
                            message_twist.append(banner_obj.banner_day)
                            current_value = cursor.fetchone()
                            message_twist.append(banner_name + "⭐⭐⭐⭐⭐")
                            break
                        else:
                            cursor.execute('SELECT * FROM characters')
                            column_names = [description[0] for description in cursor.description]
                            lega1 = ["Jean", "Dilyuk", "Ke_Qing", "Mona", "Tignari", "Qiqi"]
                            lega1 = random.choice(lega1)
                            cursor.execute(f"SELECT {lega1} FROM characters WHERE user_id_characters = ?", (user_id,))
                            qq = cursor.fetchone()
                            new_value = qq[0] + 1
                            cursor.execute(f"UPDATE characters SET {lega1} = ? WHERE user_id_characters = ?", (new_value, user_id))
                            cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (1, 0, user_id))
                            conn.commit()
                            message_twist.append(lega1 + "⭐⭐⭐⭐⭐")
                            break
                else:
                    total_chances = 0.99
                    cursor.execute("SELECT hystory FROM users WHERE user_id = ? ", (user_id,))
                    total_rolls = cursor.fetchone()
                    if random.random() * 100 <= total_chances:
                        if guarantee[1] == 1:
                            banner_name = banner_obj.banner_day()
                            cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (0, 0, user_id))
                            cursor.execute(f"SELECT {banner_name} FROM characters WHERE user_id_characters = ?", (user_id,))
                            current_value = cursor.fetchone()[0]
                            new_value = current_value + 1
                            cursor.execute(f"UPDATE characters SET {banner_name} = ? WHERE user_id_characters = ?", (new_value, user_id))
                            conn.commit()
                            message_twist.append(banner_obj.banner_day + "⭐⭐⭐⭐⭐")
                            current_value = cursor.fetchone()
                            break
                        else:
                            error_day = [7, 8, 15, 16, 24, 26, 31, 1, 1, 1, 1, 1, 1]
                            lega = random.choice(error_day)
                            if error_day == 1:
                                banner_data = banner_obj.banner_day()
                                banner = banner_data[0]
                                banner_name = banner_data[1]
                                cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (1, 0, user_id))
                                cursor.execute(f"SELECT {banner_name} FROM characters WHERE user_id_characters = ?", (user_id,))
                                current_value = cursor.fetchone()[0]
                                new_value = current_value[0] + 1
                                cursor.execute(f"UPDATE characters SET {banner_name} = ? WHERE user_id_characters = ?", (new_value, user_id))
                                conn.commit()
                                current_value = cursor.fetchone()
                                message_twist.append(banner_obj.banner_day + "⭐⭐⭐⭐⭐")
                                break
                            else:
                                cursor.execute('SELECT * FROM characters')
                                column_names = [description[0] for description in cursor.description]
                                lega1 = ["Jean", "Dilyuk", "Ke_Qing", "Mona", "Tignari", "Qiqi"]
                                lega1 = random.choice(lega1)
                                cursor.execute(f"SELECT {lega1} FROM characters WHERE user_id_characters = ?", (user_id,))
                                qq = cursor.fetchone()
                                new_value = qq[0] + 1
                                cursor.execute(f"UPDATE characters SET {lega1} = ? WHERE user_id_characters = ?", (new_value, user_id))
                                cursor.execute("UPDATE users SET guarantee = ?, hystory = ? WHERE user_id = ? ", (1, 0, user_id))
                                conn.commit()
                                message_twist.append(lega1 + "⭐⭐⭐⭐⭐")
                                break
                    else:
                        message_twist.append(random.choice(garbage))
                        
        else:
            message_twist.append("У тебя не хватает примогемов!")



    message_banner = "Твоя награда:"
    message_twist_str = ", ".join(message_twist)
    message_banner += f"{message_twist_str}\n"
    return f"{message_banner}"
        
