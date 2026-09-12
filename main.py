import asyncio
import json
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    WebAppInfo
)

BOT_TOKEN = "8275673607:AAFudImx5QCA1ipSjNJJQhI0yT9jyYmBm3M"
MOVIES_FILE = "movies.json"

# Netlify havolangiz
NETLIFY_URL = "https://etvcinemabeta.netlify.app/"

def load_movies():
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Pastki yozish maydonidagi ko'k WebApp tugmasi
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🚀 Open Web App", 
                web_app=WebAppInfo(url=NETLIFY_URL)
            )
        ]
    ],
    resize_keyboard=True
)

# Inline WebApp tugmasi (xabar ostidagi)
def get_webapp_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Kinolarni ko'rish (Mini App)", 
                    web_app=WebAppInfo(url=NETLIFY_URL)
                )
            ]
        ]
    )

@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandObject):
    movie_code = command.args  # Mini App'dan o'tilganda keladigan kod (masalan: /start 101)
    
    if movie_code:
        movies = load_movies()
        if movie_code in movies:
            movie = movies[movie_code]
            await message.answer_video(
                video=movie["file_id"],
                caption=movie["caption"],
                parse_mode="Markdown"
            )
            return
        else:
            await message.answer("⚠️ **Bunday kodli kino topilmadi!** ❌")
            return

    user_name = message.from_user.first_name
    text = (
        f"👋 **Xush kelibsiz, {user_name}!**\n\n"
        f"🎬 Iltimos, kino kodini kiriting yoki Mini App orqali tanlang:"
    )
    # Endi bu yerda ham inline, ham pastki menyu tugmasi ko'rinadi
    await message.answer(
        text, 
        reply_markup=start_keyboard, 
        parse_mode="Markdown"
    )

# Telegram'ga kino yuklaganda uning file_id'sini olish uchun
@dp.message(F.video)
async def catch_video_id(message: types.Message):
    caption_text = message.caption or "🎬 Kino nomi ko'rsatilmagan"
    response_text = (
        f"📦 **Video ID olindi:**\n`{message.video.file_id}`\n\n"
        f"📌 **Tavsifi:**\n{caption_text}"
    )
    await message.answer(response_text, parse_mode="Markdown")

@dp.message(F.text)
async def get_movie_by_code(message: types.Message):
    movie_code = message.text.strip()
    movies = load_movies()
    
    if movie_code in movies:
        movie = movies[movie_code]
        await message.answer_video(
            video=movie["file_id"],
            caption=movie["caption"],
            parse_mode="Markdown"
        )
    else:
        await message.answer("⚠️ **Bunday kodli kino topilmadi!**\n\nIltimos, kodni to'g'ri kiriting ❌")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())