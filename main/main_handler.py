from aiogram import types, Dispatcher
from keyboards import first_choise
from create_bot import dp
from data_base import sqlite_db



async def command_start(message: types.Message):
    print(message)
    await sqlite_db.sql_user_add(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username)
    await message.answer("Начало")
    await message.answer(f'Привет, {message.from_user.first_name}! Выбери раздел:', reply_markup=first_choise)
    await message.delete()

async def canceling(cbq: types.CallbackQuery):
    await cbq.message.answer("Вы вернулись в главное меню.\n\nВыберите раздел:", reply_markup=first_choise)
    await cbq.message.delete()

async def any_message(message: types.Message):
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=[
                                'start', 'help'])
    dp.register_callback_query_handler(canceling, lambda c: c.data == 'cancel')
    dp.register_message_handler(any_message, lambda m: m.text, state=None)