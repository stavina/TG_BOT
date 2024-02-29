import telebot
from telebot import types

from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI

client = OpenAI(
    api_key=TOKEN_OPENAI,
)


bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, что я могу сделать для тебя?")


@bot.message_handler(commands=["image"])
def image(message):
    prompt = message.text.split("/image")[1].strip()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=2,
    )
    photo_url = response.data[0].url
    bot.send_photo(message.chat.id, photo_url)

@bot.message_handler(func=lambda m: True)
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
