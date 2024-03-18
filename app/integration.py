
from openai import OpenAI

from config import TOKEN_OPENAI

client = OpenAI(
    api_key=TOKEN_OPENAI,
)


def get_ai_gen_text(input_text):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model="gpt-3.5-turbo",
    )
    result = completion.choices[0].message.content
    return result


def get_ai_gen_image(input_text):
    response = client.images.generate(
        model="dall-e-3",
        prompt=input_text,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    photo_url = response.data[0].url
    return photo_url