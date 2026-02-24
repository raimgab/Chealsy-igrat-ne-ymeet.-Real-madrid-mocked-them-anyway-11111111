import telebot
from telebot import types
import json

TOKEN = "8122530905:AAHGeg-V29pc8lziHoxoa61kip2sSZHWZ7o"
bot = telebot.TeleBot(TOKEN)

with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

user_question_index = {}
user_score = {}

def send_question(chat_id):
    index = user_question_index.get(chat_id, 0)

    if index >= len(questions):
        score = user_score.get(chat_id, 0)
        bot.send_message(chat_id, f"Тест завершен. Результат: {score} из {len(questions)}", reply_markup=types.ReplyKeyboardRemove())
        return

    q = questions[index]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for option in q["options"]:
        keyboard.add(types.KeyboardButton(option))

    keyboard.add(types.KeyboardButton("Пропустить вопрос"))
    bot.send_message(chat_id, q["question"], reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    user_question_index[chat_id] = 0
    user_score[chat_id] = 0
    send_question(chat_id)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    chat_id = message.chat.id

    if chat_id not in user_question_index:
        return

    index = user_question_index[chat_id]

    if message.text == "Пропустить вопрос":
        user_question_index[chat_id] += 1
        send_question(chat_id)
        return

    if index >= len(questions):
        return

    if message.text == questions[index]["correct"]:
        user_score[chat_id] += 1
        bot.send_message(chat_id, "Верно")
    else:
        bot.send_message(chat_id, f"Неверно. Ответ: {questions[index]['correct']}")

    user_question_index[chat_id] += 1
    send_question(chat_id)

bot.polling(none_stop=True)
