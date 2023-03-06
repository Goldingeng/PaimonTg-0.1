import telebot

# Создаем экземпляр бота
bot = telebot.TeleBot('5409304847:AAGtNYiN8p_GtHzvYZLQB6S6oGG2sMAwHv0')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Получаем информацию о пользователе
    user = message.from_user
    user_id = user.id
    user_name = user.username

    # Получаем аватарку пользователя
    user_avatar = bot.get_user_profile_photos(user_id).photos[0][-1]

    # Загружаем байты фотографии
    file_info = bot.get_file(user_avatar.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Отправляем байты фотографии в ответ на сообщение
    bot.send_photo(message.chat.id, downloaded_file)

# Запускаем бота
bot.polling(none_stop=True)
