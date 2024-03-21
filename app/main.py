import telebot

from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI
from database import User, db_user
from log import log_decorator 
from telebot import types
from integration import get_ai_gen_text, get_ai_gen_image

client = OpenAI(
    api_key=TOKEN_OPENAI,
)

bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # user = User(message.from_user.username, message.from_user.id)
    # db_user.add_user(user)
    log_decorator('Start bot', message.from_user.id, message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    greetings = ("Добро пожаловать! Я - нейросеть, созданная для того чтобы помогать. В мои возможности входят ответы на различные вопросы, "
                 "поиск информации, решение задач, генерация картинок и многое другое. Буду рад помочь в любых вопросах и задачах!")
    bot.send_message(message.chat.id, greetings, reply_markup=markup)


pattern_text = [
      "текст",
      "сообщение",
      "предложение",
      "описание",
      "описания",
      "напиши",
]

pattern_image = [
      "картинка",
      "картинку",
      "изображение",
      "фото",
      "пикчу",
      "покажи",
      "нарисуй",
]

def check_text(message):
    text = message.text.lower()
    for i in pattern_text:
        if i in text:
            return True
    return False

def check_image(message):
    text = message.text.lower()
    for i in pattern_image:
        if i in text:
            return True
    return False

@bot.message_handler(func=check_text)
def bot_answer_text(message):
    log_decorator('Text request', message.from_user.id, message)
    answer = get_ai_gen_text(message.text)
    bot.reply_to(message, answer)


@bot.message_handler(func=check_image)
def bot_answer_image(message):
    log_decorator('Image request', message.from_user.id, message)
    answer = get_ai_gen_image(message.text)
    bot.send_photo(message.chat.id, answer)


@bot.message_handler(func=lambda m: True)
def answer_all(message):
    log_decorator('Other request', message.from_user.id, message)
    print(message.from_user)
    completion = client.chat.completions.create(
        messages=[
            { 
                "role": "user",
                "content": message.text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    result = completion.choices[0].message.content
    bot.reply_to(message, result)


if __name__ == "__main__":
    bot.polling()
