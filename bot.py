import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=7533510582:AAG57QLCTjCNVzSs6kc00YgeH1sWLbrY9QA)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

# === 🔹 Команды ===

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Я бот-помощник. Напиши /id, чтобы узнать свой chat_id.")

@dp.message_handler(commands=['id'])
async def id_cmd(message: types.Message):
    await message.reply(f"Твой chat_id: {message.chat.id}")

# === 🔹 Рассылка по времени ===

CHAT_ID = int(os.getenv('CHAT_ID', ''))  # сюда нужно подставить свой chat_id в Render

async def send_morning_message():
    try:
        await bot.send_message(CHAT_ID, "☀️ Доброе утро! Как ты себя чувствуешь сегодня?")
    except Exception as e:
        print(f"[Ошибка утреннего сообщения] {e}")

async def send_evening_message():
    try:
        await bot.send_message(CHAT_ID, "🌙 Добрый вечер! Что ты почувствовала сегодня?")
    except Exception as e:
        print(f"[Ошибка вечернего сообщения] {e}")

# Запланировать напоминания
scheduler.add_job(send_morning_message, 'cron', hour=9, minute=0)
scheduler.add_job(send_evening_message, 'cron', hour=20, minute=0)

scheduler.start()

# === 🔹 Запуск ===

if __name__ == '__main__':
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
