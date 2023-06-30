from create_bot import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import scheduled
from datetime import datetime, timedelta
from data_base import sqlite_db
from aiogram import types, Dispatcher
from keyboards.buttons import reminder_kb
from aiogram.dispatcher.filters.state import State


async def achievement_reminder():
    users = await sqlite_db.sql_all_user_id_get()
    for user in users:
        name = await sqlite_db.sql_user_first_name_get(user)
        await bot.send_message(user, f"{name}, сегодня вы еще не записывали достижений. Чего вы сегодня достигли? Даже самое маленькое достижение значит очень много!", reply_markup=reminder_kb)


async def event_reminder():
    users = await sqlite_db.sql_all_user_id_get()
    for user in users:
        name = await sqlite_db.sql_user_first_name_get(user)
        await bot.send_message(user, f"{name}, сегодня вы еще не записывали переживаний. Чего вы сегодня достигли? Даже самое маленькое достижение значит очень много!", reply_markup=reminder_kb)


async def bdi_test_reminder():
    users = await sqlite_db.sql_all_user_id_get()
    for user in users:
        last_week_result = (await sqlite_db.sql_bditest_lastweek_result(user))[0][0]
        name = await sqlite_db.sql_user_first_name_get(user)
        print(last_week_result)
        if not last_week_result:
            await bot.send_message(user, f"{name}, Вы уже неделю не проходили тест на уровень депрессии. Рекомендуется проходить тест каждую неделю, чтобы отслеживать своё состояние", reply_markup=reminder_kb)
        else:
            pass

async def bai_test_reminder():
    users = await sqlite_db.sql_all_user_id_get()
    for user in users:
        last_week_result = (await sqlite_db.sql_baitest_lastweek_result(user))[0][0]
        name = await sqlite_db.sql_user_first_name_get(user)
        print(last_week_result)
        if not last_week_result:
            await bot.send_message(user, f"{name}, Вы уже неделю не проходили тест на уровень тревоги. Рекомендуется проходить тест каждую неделю, чтобы отслеживать своё состояние", reply_markup=reminder_kb)
        else:
            pass



# DELITING A REMINDER MESSAGE
async def delete_reminder(cbq: types.CallbackQuery):
    await cbq.message.delete()


def register_handlers_reminder(dp: Dispatcher):
    dp.register_callback_query_handler(delete_reminder, lambda c: c.data=='delete_reminder', state=None)




