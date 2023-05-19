from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import event_choise, event_finish, event_start, first_choise
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import sqlite_db
from create_bot import bot


# EVENTS STARTING MESSAGE WITH BUTTONS
async def events_start(cbq: types.CallbackQuery):
    await cbq.message.delete()
    await cbq.message.answer("Этот раздел посвящён переживаниям. Здесь можно записать новое переживание. Что ты хочешь сделать?", reply_markup=event_start)


# INSERTING NEW EVENT BUTTON

# making FSM for inserting new event
class FSM_event_form(StatesGroup):
    good_or_bad = State()
    event = State()
    physical = State()
    feelings = State()
    thoughts = State()
    current_thoughts = State()

# starting a dialog about an event
async def event_record(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await FSM_event_form.good_or_bad.set()
    await callback_query.message.answer("Это было приятное или неприятное переживание?", reply_markup=event_choise)

# catching first answer and writing it into a dict
async def load_good_or_bad(callback_query: types.CallbackQuery, state=FSMContext):
    answer = callback_query.data
    await callback_query.message.delete()
    if answer == 'cancel':
        await state.finish()
        await callback_query.message.answer("Переживание не было записано.\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    else:
        async with state.proxy() as data:
            if answer == 'good':
                data['good_or_bad'] = answer
            elif answer == 'bad':
                data['good_or_bad'] = answer
            await FSM_event_form.next()
            await callback_query.message.answer("Опишите, что произошло? Что это было за переживание?")


# catching second answer and writing it into a dict
async def load_event(message: types.message, state=FSMContext):
    async with state.proxy() as data:
        data['event'] = message.text
    await FSM_event_form.next()
    await message.reply("Опишите подробно, что именно вы ощущали в теле в момент этого переживания?")


# catching third answer and writing it into a dict
async def load_physical(message: types.message, state=FSMContext):
    async with state.proxy() as data:
        data['physical'] = message.text
    await FSM_event_form.next()
    await message.reply("Какое настроение и чувства сопровождали это событие?")


# catching fourth answer and writing it into a dict
async def load_feelings(message: types.message, state=FSMContext):
    async with state.proxy() as data:
        data['feelings'] = message.text
    await FSM_event_form.next()
    await message.reply("Какие мысли возникали у вас в голове?")


# catching fifth answer and writing it into a dict
async def load_thoughts(message: types.message, state=FSMContext):
    async with state.proxy() as data:
        data['thoughts'] = message.text
    await FSM_event_form.next()
    await message.reply("Какие мысли к вам приходят сейчас, когда вы делаете эти записи?")


# catching sixth answer and writing it into a dict
async def load_current_thoughts(message: types.message, state=FSMContext):
    async with state.proxy() as data:
        data['current_thoughts'] = message.text
    for i in range(10):
        await bot.delete_message(message.chat.id, message.message_id-(i))
    await message.answer("Переживание сформировано. Записать данное переживание?", reply_markup=event_finish)


#Asking to save or to cancel an event
async def finishing_event(callback_query: types.CallbackQuery, state=FSMContext):
    answer = callback_query.data
    if answer == 'cancel':
        await state.finish()
        await callback_query.message.answer("Переживание не было записано.\n\nВы вернулись в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    elif answer == 'load':
        await sqlite_db.sql_add_event(state)
        await state.finish()
        await callback_query.message.answer("Отлично! Вы записали переживание.\n\nВернёмся в главное меню.\nВыберите раздел:", reply_markup=first_choise)
    await callback_query.message.delete()



# GET EVENTS BUTTON

class FSM_event_date(StatesGroup):
    event_year_state = State()
    event_month_state = State()
    event_day_state = State()
    event_id_state = State()



# Getting years from DB and making buttons to choose from

async def choose_event_year(cbq: types.CallbackQuery):
    year_buttons = []
    years = await sqlite_db.sql_get_events_years()
    if years == []:
        await cbq.message.answer("Вы ещё не записали ни одного переживания. Начнём с начала", reply_markup=first_choise)
    else:
        for year in years:
            year_buttons.append(InlineKeyboardButton(text=year[0], callback_data=f"event_year_{year[0]}"))
        events_years_kb = InlineKeyboardMarkup(row_width=1)
        events_years_kb.add(*year_buttons)
        await FSM_event_date.event_year_state.set()
        await cbq.message.answer("Выберите год из которго вы хотите вспомнить переживание:", reply_markup=events_years_kb)
    await cbq.message.delete()


# Recording a year for the quiery
async def load_event_date_year(cbq: types.CallbackQuery, state=FSMContext):
    year = str(cbq.data.split('_')[2])
    #recording chosen year in a dict
    async with state.proxy() as data:
        data['event_year'] = year
    #creating keyboard for months
    months_buttons = []
    months = await sqlite_db.sql_get_events_months(data['event_year'])
    months_dict = {
        '1': 'Январь',
        '2': 'Февраль',
        '3': 'Март',
        '4': 'Апрель',
        '5': 'Май',
        '6': 'Июнь',
        '7': 'Июль',
        '8': 'Август',
        '9': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь',
    }
    for month in months:
        months_buttons.append(InlineKeyboardButton(text=months_dict[str(month[0])], callback_data=f"event_month_{month[0]}"))
    events_months_kb = InlineKeyboardMarkup(row_width=4)
    events_months_kb.add(*months_buttons)
    # quiering qty of good and bad events in a chosen year
    good_events_qty_year = await sqlite_db.sql_count_events_year('good', data['event_year'])
    bad_events_qty_year = await sqlite_db.sql_count_events_year('bad', data['event_year'])
    await FSM_event_date.next()
    await cbq.message.answer(f"Количество переживаний в этом году:\nХороших: {good_events_qty_year[0][0]}\nПлохих: {bad_events_qty_year[0][0]}\nВыберите месяц из которго вы хотите вспомнить переживание:", reply_markup=events_months_kb)
    await cbq.message.delete()


# Recording a month for the quiery:
async def load_event_date_month(cbq: types.CallbackQuery, state=FSMContext):
    month = str(cbq.data.split('_')[2])
    #recording chosen month into a dict
    async with state.proxy() as data:
        data['event_month'] = month
    #making a keyboard of days
    days_buttons = []
    days = await sqlite_db.sql_get_events_days(data['event_year'], data['event_month'])
    for day in days:
        days_buttons.append(InlineKeyboardButton(text=day[0], callback_data=f"event_day_{day[0]}"))
    events_days_kb = InlineKeyboardMarkup(row_width=6)
    events_days_kb.add(*days_buttons)
    # quiering qty of good and bad events in a chosen month
    good_events_qty_month = await sqlite_db.sql_count_events_month('good', data['event_year'], data['event_month'])
    bad_events_qty_month = await sqlite_db.sql_count_events_month('bad', data['event_year'], data['event_month'])
    await FSM_event_date.next()
    await cbq.message.answer(f"Количество переживаний в этом месяце:\nХороших: {good_events_qty_month[0][0]}\nПлохих: {bad_events_qty_month[0][0]}\nВыберите день из которго вы хотите вспомнить переживание:", reply_markup=events_days_kb)
    await cbq.message.delete()


# Recording a day for a quiery
async def load_event_date_day(cbq: types.CallbackQuery, state=FSMContext):
    day = str(cbq.data.split('_')[2])
    #recording chosen month into a dict
    async with state.proxy() as data:
        data['event_day'] = day
    #making a keyboard of events
    events_buttons = []
    events = await sqlite_db.sql_get_events_id(data['event_year'], data['event_month'], data['event_day'])
    for event in events:
        if event[0] == "good":
            events_buttons.append(InlineKeyboardButton(text=f"(приятное) \n{event[2][:25]}...", callback_data=f"event_id_{event[1]}"))
        elif event[0] == "bad":
            events_buttons.append(InlineKeyboardButton(text=f"(неприятное) \n{event[2][:25]}...", callback_data=f"event_id_{event[1]}"))
    events_kb = InlineKeyboardMarkup(row_width=1)
    events_kb.add(*events_buttons)
    # quiering qty of good and bad events in a chosen day
    good_events_qty_day = await sqlite_db.sql_count_events_day('good', data['event_year'], data['event_month'], data['event_day'])
    bad_events_qty_day = await sqlite_db.sql_count_events_day('bad', data['event_year'], data['event_month'], data['event_day'])
    await FSM_event_date.next()
    await cbq.message.answer(f"Количество переживаний в этот день:\nХороших: {good_events_qty_day[0][0]}\nПлохих: {bad_events_qty_day[0][0]}\nВыберите какое имнно переживание вы хотите вспомнить:", reply_markup=events_kb)
    await cbq.message.delete()


# showing a chosen event to a user

async def get_chosen_event(cbq: types.CallbackQuery, state=FSMContext):
    event_id = str(cbq.data.split('_')[2])
    event = await sqlite_db.sql_get_chosen_event(event_id)
    await state.finish()
    await cbq.message.answer(f"""Ваше переживание:

***
Вот этот день: {event[0]}\n
В этот момент вы ощущали в теле: {event[1]}\n
Это переживание сопровождали следующее настроение и чувства: {event[2]}\n
В момент этого переживания Вас посещали следующие мысли: {event[3]}\n
А когда делали эту запись Вас посещали следующие мысли: {event[4]}
***



Вы в главном меню.
Выберите раздел:""", reply_markup=first_choise)
    await cbq.message.delete()



# EVENTS HANDLERS
def register_handlers_event(dp: Dispatcher):
    # starting events handlers
    dp.register_callback_query_handler(
        events_start, lambda c: c.data == 'events')
    # inserting new event handlers
    dp.register_callback_query_handler(
        event_record, lambda c: c.data == 'record_event', state=None)
    dp.register_callback_query_handler(
        load_good_or_bad, state=FSM_event_form.good_or_bad)
    dp.register_message_handler(load_event, state=FSM_event_form.event)
    dp.register_message_handler(load_physical, state=FSM_event_form.physical)
    dp.register_message_handler(load_feelings, state=FSM_event_form.feelings)
    dp.register_message_handler(load_thoughts, state=FSM_event_form.thoughts)
    dp.register_message_handler(
        load_current_thoughts, state=FSM_event_form.current_thoughts)
    dp.register_callback_query_handler(
        finishing_event, state=FSM_event_form.current_thoughts)
    # get events handlers
    dp.register_callback_query_handler(
        choose_event_year, lambda c: c.data == 'events_get', state=None)
    dp.register_callback_query_handler(load_event_date_year, lambda c: c.data.startswith('event_year_'), state=FSM_event_date.event_year_state)
    dp.register_callback_query_handler(load_event_date_month, lambda c: c.data.startswith('event_month_'), state=FSM_event_date.event_month_state)
    dp.register_callback_query_handler(load_event_date_day, lambda c: c.data.startswith('event_day_'), state=FSM_event_date.event_day_state)
    dp.register_callback_query_handler(get_chosen_event, lambda c: c.data.startswith('event_id_'), state=FSM_event_date.event_id_state)

    
    
    
