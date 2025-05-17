{\rtf1\ansi\ansicpg1251\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import logging\
from aiogram import Bot, Dispatcher, executor, types\
from aiogram.types import ParseMode\
from aiogram.contrib.fsm_storage.memory import MemoryStorage\
from aiogram.dispatcher import FSMContext\
from aiogram.dispatcher.filters.state import State, StatesGroup\
from apscheduler.schedulers.asyncio import AsyncIOScheduler\
from datetime import datetime, time\
import asyncio\
\
import os
API_TOKEN = os.getenv('API_TOKEN')\
\
logging.basicConfig(level=logging.INFO)\
\
bot = Bot(token=API_TOKEN)\
dp = Dispatcher(bot, storage=MemoryStorage())\
scheduler = AsyncIOScheduler()\
\
class JournalStates(StatesGroup):\
    morning_feeling = State()\
    morning_worry = State()\
    morning_power = State()\
    morning_enough = State()\
    evening_done = State()\
    evening_helped = State()\
    evening_message = State()\
\
# Start command\
@dp.message_handler(commands=['start'])\
async def send_welcome(message: types.Message):\
    await message.reply("\uc0\u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1071  \u1090 \u1074 \u1086 \u1081  \u1090 \u1088 \u1077 \u1074 \u1086 \u1078 \u1085 \u1099 \u1081  \u1077 \u1078 \u1077 \u1076 \u1085 \u1077 \u1074 \u1085 \u1080 \u1082  
\f1 \uc0\u55358 \u56792 \u8205 \u9792 \u65039 
\f0 \\n\uc0\u1071  \u1073 \u1091 \u1076 \u1091  \u1079 \u1072 \u1076 \u1072 \u1074 \u1072 \u1090 \u1100  \u1090 \u1077 \u1073 \u1077  \u1074 \u1086 \u1087 \u1088 \u1086 \u1089 \u1099  \u1091 \u1090 \u1088 \u1086 \u1084  \u1080  \u1074 \u1077 \u1095 \u1077 \u1088 \u1086 \u1084 .\\n\\n\u1050 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099 :\\n/morning \'97 \u1091 \u1090 \u1088 \u1077 \u1085 \u1085 \u1080 \u1077  \u1074 \u1086 \u1087 \u1088 \u1086 \u1089 \u1099 \\n/evening \'97 \u1074 \u1077 \u1095 \u1077 \u1088 \u1085 \u1080 \u1077 \\n/plan \'97 \u1087 \u1083 \u1072 \u1085  \u1085 \u1072  \u1076 \u1077 \u1085 \u1100 \\n/tension \'97 \u1088 \u1072 \u1073 \u1086 \u1090 \u1072  \u1089  \u1090 \u1088 \u1077 \u1074 \u1086 \u1075 \u1086 \u1081 ")\
\
# Morning flow\
@dp.message_handler(commands=['morning'])\
async def morning_start(message: types.Message):\
    await message.answer("
\f1 \uc0\u9728 \u65039 
\f0  \uc0\u1050 \u1072 \u1082  \u1090 \u1099  \u1089 \u1077 \u1073 \u1103  \u1089 \u1077 \u1081 \u1095 \u1072 \u1089  \u1095 \u1091 \u1074 \u1089 \u1090 \u1074 \u1091 \u1077 \u1096 \u1100 ?")\
    await JournalStates.morning_feeling.set()\
\
@dp.message_handler(state=JournalStates.morning_feeling)\
async def morning_worry(message: types.Message, state: FSMContext):\
    await state.update_data(feeling=message.text)\
    await message.answer("\uc0\u1063 \u1090 \u1086  \u1090 \u1077 \u1073 \u1103  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1090 \u1088 \u1077 \u1074 \u1086 \u1078 \u1080 \u1090 ?")\
    await JournalStates.morning_worry.set()\
\
@dp.message_handler(state=JournalStates.morning_worry)\
async def morning_power(message: types.Message, state: FSMContext):\
    await state.update_data(worry=message.text)\
    await message.answer("\uc0\u1053 \u1072 \u1079 \u1086 \u1074 \u1080  3 \u1074 \u1077 \u1097 \u1080 , \u1082 \u1086 \u1090 \u1086 \u1088 \u1099 \u1077  \u1074  \u1090 \u1074 \u1086 \u1080 \u1093  \u1089 \u1080 \u1083 \u1072 \u1093  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103 :")\
    await JournalStates.morning_power.set()\
\
@dp.message_handler(state=JournalStates.morning_power)\
async def morning_enough(message: types.Message, state: FSMContext):\
    await state.update_data(power=message.text)\
    await message.answer("\uc0\u1063 \u1090 \u1086  \u1090 \u1099  \u1089 \u1076 \u1077 \u1083 \u1072 \u1077 \u1096 \u1100  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  *\u1076 \u1086 \u1089 \u1090 \u1072 \u1090 \u1086 \u1095 \u1085 \u1086  \u1093 \u1086 \u1088 \u1086 \u1096 \u1086 *, \u1072  \u1085 \u1077  \u1080 \u1076 \u1077 \u1072 \u1083 \u1100 \u1085 \u1086 ?", parse_mode=ParseMode.MARKDOWN)\
    await JournalStates.morning_enough.set()\
\
@dp.message_handler(state=JournalStates.morning_enough)\
async def morning_done(message: types.Message, state: FSMContext):\
    await state.update_data(enough=message.text)\
    data = await state.get_data()\
    summary = f"\\n
\f1 \uc0\u9728 \u65039 
\f0  \uc0\u1059 \u1090 \u1088 \u1077 \u1085 \u1085 \u1080 \u1081  \u1095 \u1077 \u1082 -\u1080 \u1085 :\\n\u1058 \u1099  \u1095 \u1091 \u1074 \u1089 \u1090 \u1074 \u1091 \u1077 \u1096 \u1100 : \{data['feeling']\}\\n\u1058 \u1088 \u1077 \u1074 \u1086 \u1078 \u1080 \u1090 : \{data['worry']\}\\n\u1042  \u1089 \u1080 \u1083 \u1072 \u1093 : \{data['power']\}\\n\u1044 \u1086 \u1089 \u1090 \u1072 \u1090 \u1086 \u1095 \u1085 \u1086  \u1093 \u1086 \u1088 \u1086 \u1096 \u1086 : \{data['enough']\}"\
    await message.answer(summary)\
    await state.finish()\
\
# Evening flow\
@dp.message_handler(commands=['evening'])\
async def evening_start(message: types.Message):\
    await message.answer("
\f1 \uc0\u55356 \u57113 
\f0  \uc0\u1063 \u1090 \u1086  \u1090 \u1099  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1074 \u1089 \u1105 -\u1090 \u1072 \u1082 \u1080  \u1089 \u1076 \u1077 \u1083 \u1072 \u1083 \u1072 ?")\
    await JournalStates.evening_done.set()\
\
@dp.message_handler(state=JournalStates.evening_done)\
async def evening_helped(message: types.Message, state: FSMContext):\
    await state.update_data(done=message.text)\
    await message.answer("\uc0\u1063 \u1090 \u1086  \u1090 \u1077 \u1073 \u1077  \u1087 \u1086 \u1084 \u1086 \u1075 \u1083 \u1086 ?")\
    await JournalStates.evening_helped.set()\
\
@dp.message_handler(state=JournalStates.evening_helped)\
async def evening_message(message: types.Message, state: FSMContext):\
    await state.update_data(helped=message.text)\
    await message.answer("\uc0\u1063 \u1090 \u1086  \u1090 \u1099  \u1089 \u1082 \u1072 \u1078 \u1077 \u1096 \u1100  \u1089 \u1077 \u1073 \u1077  \u1085 \u1072  \u1085 \u1086 \u1095 \u1100 ?")\
    await JournalStates.evening_message.set()\
\
@dp.message_handler(state=JournalStates.evening_message)\
async def evening_summary(message: types.Message, state: FSMContext):\
    await state.update_data(night_msg=message.text)\
    data = await state.get_data()\
    summary = f"
\f1 \uc0\u55356 \u57113 
\f0  \uc0\u1042 \u1077 \u1095 \u1077 \u1088 \u1085 \u1080 \u1081  \u1080 \u1090 \u1086 \u1075 :\\n\u1057 \u1076 \u1077 \u1083 \u1072 \u1083 \u1072 : \{data['done']\}\\n\u1055 \u1086 \u1084 \u1086 \u1075 \u1083 \u1086 : \{data['helped']\}\\n\u1057 \u1077 \u1073 \u1077  \u1085 \u1072  \u1085 \u1086 \u1095 \u1100 : \{data['night_msg']\}"\
    await message.answer(summary)\
    await state.finish()\
\
# Plan handler\
@dp.message_handler(commands=['plan'])\
async def plan(message: types.Message):\
    await message.answer("
\f1 \uc0\u55357 \u56770 
\f0  \uc0\u1053 \u1072 \u1087 \u1080 \u1096 \u1080  1\'963 \u1086 \u1073 \u1103 \u1079 \u1072 \u1090 \u1077 \u1083 \u1100 \u1085 \u1099 \u1077  \u1079 \u1072 \u1076 \u1072 \u1095 \u1080  \u1085 \u1072  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1080  1\'962 \u1087 \u1086  \u1078 \u1077 \u1083 \u1072 \u1085 \u1080 \u1102 :")\
\
# Tension handler\
@dp.message_handler(commands=['tension'])\
async def tension(message: types.Message):\
    await message.answer("
\f1 \uc0\u55357 \u56863 
\f0  \uc0\u1063 \u1090 \u1086  \u1090 \u1077 \u1073 \u1103  \u1090 \u1088 \u1077 \u1074 \u1086 \u1078 \u1080 \u1090 ?")\
    await asyncio.sleep(5)\
    await message.answer("\uc0\u1040  \u1090 \u1077 \u1087 \u1077 \u1088 \u1100 : \u1095 \u1090 \u1086  \u1090 \u1099  \u1084 \u1086 \u1078 \u1077 \u1096 \u1100  \u1089 \u1076 \u1077 \u1083 \u1072 \u1090 \u1100  \u1087 \u1088 \u1103 \u1084 \u1086  \u1089 \u1077 \u1081 \u1095 \u1072 \u1089 ?")\
    await asyncio.sleep(5)\
    await message.answer("\uc0\u1063 \u1090 \u1086  \u1090 \u1099  \u1089 \u1082 \u1072 \u1078 \u1077 \u1096 \u1100  \u1089 \u1077 \u1073 \u1077  \u1074 \u1084 \u1077 \u1089 \u1090 \u1086  \u1090 \u1088 \u1077 \u1074 \u1086 \u1078 \u1085 \u1086 \u1081  \u1084 \u1099 \u1089 \u1083 \u1080 ?\\n
\f1 \uc0\u55357 \u56492 
\f0  \uc0\u1069 \u1090 \u1086  \u1087 \u1088 \u1086 \u1089 \u1090 \u1086  \u1084 \u1099 \u1089 \u1083 \u1100 , \u1085 \u1077  \u1092 \u1072 \u1082 \u1090 . \u1058 \u1099  \u1089 \u1087 \u1088 \u1072 \u1074 \u1083 \u1103 \u1077 \u1096 \u1100 \u1089 \u1103  
\f1 \uc0\u55357 \u56473 
\f0 ")\
\
# Schedule daily messages (optional)\
async def schedule_messages():\
    scheduler.add_job(send_morning_prompt, 'cron', hour=9)\
    scheduler.add_job(send_evening_prompt, 'cron', hour=20)\
    scheduler.start()\
\
async def send_morning_prompt():\
    await bot.send_message(CHAT_ID, "/morning")\
\
async def send_evening_prompt():\
    await bot.send_message(CHAT_ID, "/evening")\
\
if __name__ == '__main__':\
    # asyncio.create_task(schedule_messages())  # enable if you know your chat_id\
    executor.start_polling(dp, skip_updates=True)\
}
