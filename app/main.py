import telebot

from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI
from database import User, db_user
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    textbtn1 = types.KeyboardButton(text="📝 Генерировать текст", callback_data="generate_text")
    imagebtn2 = types.KeyboardButton(text="🖼 Генерировать изображение", callback_data="generate_image")
    # Добавление кнопок в разметку
    markup.add(textbtn1, imagebtn2)
    # Отправка сообщения с приветствием и добавлением меню
    bot.send_message(message.chat.id, "Добро пожаловать, выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📝 Генерировать текст")
def answer(message):
    bot.reply_to(message, "Какой текст вам нужно сгенерировать?")

@bot.message_handler(func=lambda message: message.text == "🖼 Генерировать изображение")
def answer(message):
    bot.reply_to(message, "Какую картинку вам нужно сгенерировать?")
    prompt = get_ai_gen_image(message.text)
    bot.send_photo(message.from_user, prompt)

def answer_all(message):
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
