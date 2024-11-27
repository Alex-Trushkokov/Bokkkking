import telebot
from telebot import types
from datetime import datetime


API_TOKEN = '7693394139:AAG0HtUtX8gRDMgwJEiq0J0Y6i48PzvrgaM'
bot = telebot.TeleBot(API_TOKEN)


meetings = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать в Бота для бронирования встреч! Используйте команду /booking для начала.")


@bot.message_handler(commands=['booking'])
def book_meeting(message):
    markup = types.InlineKeyboardMarkup()
    meeting_types = ["Консультация", "Тренировка", "Встреча", "Вебинар"]
    for meeting in meeting_types:
        button = types.InlineKeyboardButton(text=meeting, callback_data=meeting)
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите тип встречи:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    meeting_type = call.data
    bot.answer_callback_query(call.id, f"Вы выбрали: {meeting_type}")


    bot.send_message(call.message.chat.id, "Введите дату и время для встречи (например, 2024 11 30 19:00).")
    bot.register_next_step_handler(call.message, process_date_time, meeting_type, call.from_user)


def process_date_time(message, meeting_type, user):
    date_time_str = message.text
    try:
        date_time = datetime.strptime(date_time_str, '%Y %m %d %H:%M')
        if date_time < datetime.now():
            raise ValueError("Дата не может быть в прошлом.")


        meeting_info = {
            'user_id': user.id,
            'username': user.username,
            'meeting_type': meeting_type,
            'date_time': date_time_str
        }
        meetings.append(meeting_info)

        bot.send_message(message.chat.id, f"Вы успешно забронировали встречу типа '{meeting_type}' на {date_time_str}!")

    except ValueError as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}. Пожалуйста, введите дату и время в формате YYYY MM DD HH:MM.")


@bot.message_handler(commands=['meet'])
def list_meetings(message):
    if meetings:
        response = "Список всех встреч:\n"
        for meeting in meetings:
            response += f"Пользователь: {meeting['username']}, Тип встречи: {meeting['meeting_type']}, Время: {meeting['date_time']}\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Нет запланированных встреч.")


bot.polling(none_stop=True)