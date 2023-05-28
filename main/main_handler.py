from aiogram import types, Dispatcher
from keyboards import first_choise, gender_choice_kb
from create_bot import dp, bot
from data_base import sqlite_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import scheduled
from datetime import datetime, timedelta



async def command_start(message: types.Message):
    await sqlite_db.sql_user_add(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username)
    await message.answer('"Несчастным или счастливым человека делают только его мысли, а не внешние обстоятельства. Управляя своими мыслями, он управляет своим счастьем."\n\n—  Фридрих Вильгельм Ницше')
    await message.answer(f"Выберите пол:", reply_markup=gender_choice_kb)
    await message.delete()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(scheduled.achievement_reminder, trigger='date', run_date=datetime.now() + timedelta(seconds=10))
    scheduler.add_job(scheduled.event_reminder, trigger='date', hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now())
    scheduler.start()

# Choosing a gender
async def user_gender_choice(cbq: types.CallbackQuery):
    await sqlite_db.sql_user_gender_add(cbq.message.chat.id, cbq.data.split('_')[1])
    await cbq.message.answer(f"Привет, {cbq.message.chat.first_name}!\n\nВыберите раздел:", reply_markup=first_choise)
    await cbq.message.delete()


async def canceling(cbq: types.CallbackQuery):
    await cbq.message.answer("Вы вернулись в главное меню.\n\nВыберите раздел:", reply_markup=first_choise)
    await cbq.message.delete()

# Deliting random messages from user
async def any_message(message: types.Message):
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=[
                                'start', 'help'])
    dp.register_callback_query_handler(canceling, lambda c: c.data == 'cancel')
    dp.register_callback_query_handler(user_gender_choice, lambda c: c.data.startswith('gender_'))
    dp.register_message_handler(any_message, lambda m: m.text, state=None)