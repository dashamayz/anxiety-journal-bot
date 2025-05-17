import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
import asyncio

API_TOKEN = '7533510582:AAG57QLCTjCNVzSs6kc00YgeH1sWLbrY9QA'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()

class JournalStates(StatesGroup):
    morning_feeling = State()
    morning_worry = State()
    morning_power = State()
    morning_enough = State()
    evening_done = State()
    evening_helped = State()
    evening_message = State()

# Start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой тревожный ежедневник 🧘‍♀️\nЯ буду задавать тебе вопросы утром и вечером.\n\nКоманды:\n/morning — утренние вопросы\n/evening — вечерние\n/plan — план на день\n/tension — работа с тревогой")

# Morning flow
@dp.message_handler(commands=['morning'])
async def morning_start(message: types.Message):
    await message.answer("☀️ Как ты себя сейчас чувствуешь?")
    await JournalStates.morning_feeling.set()

@dp.message_handler(state=JournalStates.morning_feeling)
async def morning_worry(message: types.Message, state: FSMContext):
    await state.update_data(feeling=message.text)
    await message.answer("Что тебя сегодня тревожит?")
    await JournalStates.morning_worry.set()

@dp.message_handler(state=JournalStates.morning_worry)
async def morning_power(message: types.Message, state: FSMContext):
    await state.update_data(worry=message.text)
    await message.answer("Назови 3 вещи, которые в твоих силах сегодня:")
    await JournalStates.morning_power.set()

@dp.message_handler(state=JournalStates.morning_power)
async def morning_enough(message: types.Message, state: FSMContext):
    await state.update_data(power=message.text)
    await message.answer("Что ты сделаешь сегодня *достаточно хорошо*, а не идеально?", parse_mode=ParseMode.MARKDOWN)
    await JournalStates.morning_enough.set()

@dp.message_handler(state=JournalStates.morning_enough)
async def morning_done(message: types.Message, state: FSMContext):
    await state.update_data(enough=message.text)
    data = await state.get_data()
    summary = f"\n☀️ Утренний чек-ин:\nТы чувствуешь: {data['feeling']}\nТревожит: {data['worry']}\nВ силах: {data['power']}\nДостаточно хорошо: {data['enough']}"
    await message.answer(summary)
    await state.finish()

# Evening flow
@dp.message_handler(commands=['evening'])
async def evening_start(message: types.Message):
    await message.answer("🌙 Что ты сегодня всё-таки сделала?")
    await JournalStates.evening_done.set()

@dp.message_handler(state=JournalStates.evening_done)
async def evening_helped(message: types.Message, state: FSMContext):
    await state.update_data(done=message.text)
    await message.answer("Что тебе помогло?")
    await JournalStates.evening_helped.set()

@dp.message_handler(state=JournalStates.evening_helped)
async def evening_message(message: types.Message, state: FSMContext):
    await state.update_data(helped=message.text)
    await message.answer("Что ты скажешь себе на ночь?")
    await JournalStates.evening_message.set()

@dp.message_handler(state=JournalStates.evening_message)
async def evening_summary(message: types.Message, state: FSMContext):
    await state.update_data(night_msg=message.text)
    data = await state.get_data()
    summary = f"🌙 Вечерний итог:\nСделала: {data['done']}\nПомогло: {data['helped']}\nСебе на ночь: {data['night_msg']}"
    await message.answer(summary)
    await state.finish()

# Plan handler
@dp.message_handler(commands=['plan'])
async def plan(message: types.Message):
    await message.answer("🗂 Напиши 1–3 обязательные задачи на сегодня и 1–2 по желанию:")

# Tension handler
@dp.message_handler(commands=['tension'])
async def tension(message: types.Message):
    await message.answer("😟 Что тебя тревожит?")
    await asyncio.sleep(5)
    await message.answer("А теперь: что ты можешь сделать прямо сейчас?")
    await asyncio.sleep(5)
    await message.answer("Что ты скажешь себе вместо тревожной мысли?\n💬 Это просто мысль, не факт. Ты справляешься 💙")

# Schedule daily messages (optional)
async def schedule_messages():
    scheduler.add_job(send_morning_prompt, 'cron', hour=9)
    scheduler.add_job(send_evening_prompt, 'cron', hour=20)
    scheduler.start()

async def send_morning_prompt():
    await bot.send_message(CHAT_ID, "/morning")

async def send_evening_prompt():
    await bot.send_message(CHAT_ID, "/evening")

if __name__ == '__main__':
    # asyncio.create_task(schedule_messages())  # enable if you know your chat_id
    executor.start_polling(dp, skip_updates=True)
