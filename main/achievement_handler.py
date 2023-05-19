from aiogram import types, Dispatcher
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import achievements_choise, first_choise
from create_bot import bot

# ACHIEVEMENTS STARTING MESSAGE WITH BUTTONS

async def achievements_start(cbq: types.CallbackQuery):
    await cbq.message.answer("Это раздел про достижения. Здесь можно записать новое достижение и узнать сколько у тебя уже достижений!", reply_markup=achievements_choise)
    await cbq.message.delete()


# INSERTING NEW ACHIEVEMENT BUTTON
class FSM_achievements_form(StatesGroup):
    achievement_text = State()

async def achievements_record(cbq: types.CallbackQuery, state=None):
    await FSM_achievements_form.achievement_text.set()
    await cbq.message.answer(
        "Какое достижение вы сегодня сделали? Оно может быть даже самым маленьким.\n\nОпишите его:")
    await cbq.message.delete()


# Describing new achievement
async def load_achievement(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['achievement'] = message.text
    await sqlite_db.sql_add_achievement(state)
    await state.finish()
    await bot.delete_message(message.chat.id, message.message_id-1)
    print(message.chat.id)
    await message.delete()
    await message.answer("Отлично! Достижение добавлено!\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)


# COUNTING ACHIEVEMENTS BUTTON
async def count_achievemnts(cbq: types.CallbackQuery):
    answer = await sqlite_db.sql_count_achievements()
    last_digits = ('2', '3', '4')
    if str(answer).endswith(last_digits):
        await cbq.message.answer(f"У тебя уже {answer} достижения!\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    elif str(answer).endswith('1'):
        await cbq.message.answer(f"У тебя уже {answer} достижение!\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    else:
        await cbq.message.answer(f"У тебя уже {answer} достижений!\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    await cbq.message.delete()



# ACHIEVEMENTS HANDLER
def register_handlers_achievement(dp: Dispatcher):
    # starting message achievements handlers
    dp.register_callback_query_handler(achievements_start, lambda c: c.data == 'achievements')
    # insert achievements handlers
    dp.register_callback_query_handler(
        achievements_record, lambda c: c.data == 'record_achievement', state=None)
    dp.register_message_handler(
        load_achievement, state=FSM_achievements_form.achievement_text)
    # count achievements handlers
    dp.register_callback_query_handler(
        count_achievemnts, lambda c: c.data == 'count_achievements')
