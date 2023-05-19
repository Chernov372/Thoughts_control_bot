from aiogram import types, Dispatcher
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import bai_test_kb, bai_test_answers_kb, bai_test_start_kb, first_choise, bai_test_dinamics_kb, bai_test_end_kb
from forms import bai_test_questions
# from create_bot import bot


questions = bai_test_questions.bai_questions


# CBI TEST FIRST CHOISE
async def bai_test_first_choise(cbq: types.CallbackQuery):
    await cbq.message.delete()
    await cbq.message.answer("В этом разделе вы можете пройти тест на определения уровня тревоги и отслеживать динамику его результатов.\n\nВажно:\nтест не может быть использован для самостоятельной постановки диагноза! В случае любых сомнений обращайтесь к квалифицированным специалистам.", reply_markup=bai_test_kb)


# TEST PART
class FSM_bai_test_form(StatesGroup):
    q = State()
    result = State()

# Starting a test
async def bai_test_start(cbq: types.CallbackQuery, state=None):
    await FSM_bai_test_form.q.set()
    async with state.proxy() as data:
        data['q_num'] = 1
        data['sum'] = 0
    await cbq.message.delete()
    await cbq.message.answer("""В этом тесте вам будет представлен список, который содержит наиболее распространенные симптомы тревоги.

Пожалуйста, тщательно изучите каждый пункт.

Отметьте, насколько вас беспокоил каждый из этих симптомов в течение последней недели, включая сегодняшний день.""", reply_markup=bai_test_start_kb)


async def bai_test_questions(cbq: types.CallbackQuery, state=FSMContext):
    if cbq.data == 'cancel':
        await state.finish()
        await cbq.message.delete()
        await cbq.message.answer("Прохождение теста отменено.\n\nПродолжим работу\nВыберите раздел:", reply_markup=first_choise)
    else:
        q_num = (await state.get_data())['q_num']
        if cbq.data.startswith('bai_test_answer'):
            answer = int(cbq.data.split('_')[3])
        else:
            answer = 0
        if q_num > 21:
            await state.update_data(sum=(await state.get_data())['sum']+answer)
            await cbq.message.delete()
            await cbq.message.answer("Тест завершён!", reply_markup=bai_test_end_kb)
            await FSM_bai_test_form.next()
        else:
            await cbq.message.answer(f"{questions[f'q{q_num}']}", reply_markup=bai_test_answers_kb)
            await cbq.message.delete()
            await state.update_data(sum=(await state.get_data())['sum']+answer)
            await state.update_data(q_num=q_num+1)

# Recording results
async def bai_test_result_record(cbq: types.CallbackQuery, state=FSMContext):
    result = (await state.get_data())['sum']
    print(await sqlite_db.sql_baitest_last_result())
    try:
        last_result = (await sqlite_db.sql_baitest_last_result())[0][0]
    except:
        last_result = await sqlite_db.sql_baitest_last_result()
    await sqlite_db.sql_baitest_insert_result(result)
    if last_result == [] or result >= last_result:
        if result <= 21:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на то, что уровень вашей тревоги - незначителен.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        elif 22 <= result <= 35:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на среднюю выраженность тревоги\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие очень высокой тревоги\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
    elif result < last_result:
        if result <= 21:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на то, что уровень вашей тревоги незначителен.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        elif 22 <= result <= 35:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на среднюю выраженность тревоги.\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что уровень вашей тревоги снизился. Так держать!\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие очень высокой тревоги.\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что уровень вашей тревоги снизился. Так держать!\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
    await state.finish()
    await cbq.message.delete()


# TEST DINAMIC PART
# asking user what dynamic to choose
async def bai_test_dinamic_choise(cbq: types.CallbackQuery):
    await cbq.message.delete()
    await cbq.message.answer("В этом разделе Вы можете отслеживать изменения своего состояния.\nКакие изменения Вас интересуют?", reply_markup=bai_test_dinamics_kb)

# comparing with a previous week
async def bai_test_dinamics_lastresult(cbq: types.CallbackQuery):
    last_week_results = (await sqlite_db.sql_baitest_lastweek_result())[0][0]
    previous_week_result = (await sqlite_db.sql_baitest_previousweek_result())[0][0]
    await cbq.message.delete()
    if last_week_results == None:
        await cbq.message.answer("Вы не проходили тест за последнюю неделю", reply_markup=bai_test_kb)
    else:
        if previous_week_result == None:
            await cbq.message.answer(f"""Cредний показатель теста за неделю - {int(last_week_results)} из 63\n\nК сожалению сравнить с предыдущей неделей не получится, так как Вы не проходили тест неделю назад\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        else:
            if last_week_results < previous_week_result:
                await cbq.message.answer(f"""Вы делаете успехи!\nCредний показатель теста за неделю - {int(last_week_results)} из 63\n\nПо сравнению с предыдущей неделей средний результат теста стал меньше на {int(previous_week_result-last_week_results)}. Это может означать, что уровень Вашей депрессии снизился!\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
            else:
                await cbq.message.answer(f"""Cредний показатель теста за неделю - {int(last_week_results)} из 63\n\nПо сравнению с предыдущей неделей средний результат теста стал больше на {int(last_week_results-previous_week_result)}. Продолжайте работу над собой и своими чувствами.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)

# comparing last result with last 30 days averege
async def bai_test_dinamic_lastmonth(cbq: types.CallbackQuery):
    current_month_result = (await sqlite_db.sql_baitest_currentmonth_result())[0][0]
    try:
        last_result = (await sqlite_db.sql_baitest_last_result())[0][0]
    except:
        last_result = await sqlite_db.sql_baitest_last_result()
    await cbq.message.delete()
    if last_result == []:
        await cbq.message.answer("Вы ещё ни разу не проходили тест на уровень депрессии", reply_markup=first_choise)
    else:
        if last_result < current_month_result:
            await cbq.message.answer(f"Вы делаете успехи!\nПоследний результат теста - {int(last_result)} из 63\n\nПо сравнению со средним значением за последние 30 дней, результат теста стал меньше на {int(current_month_result-last_result)}. Это может означать, что уровень Вашей тревоги снизился!\n\nНачнём с начала. Выберите раздел", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"Последний результат теста - {int(last_result)} из 63\n\nПо сравнению со средним значением за последние 30 дней, результат теста стал больше на {int(current_month_result-last_result)}. Продолжайте работу над собой и своими чувствами.\n\nНачнём с начала. Выберите раздел", reply_markup=first_choise)


def register_handlers_bai_test(dp: Dispatcher):
    # Starting test handlers
    dp.register_callback_query_handler(
        bai_test_first_choise, lambda c: c.data == 'bai_test')
    dp.register_callback_query_handler(
        bai_test_dinamic_choise, lambda c: c.data == 'bai_test_dynamic')
    # bdi test handlers
    dp.register_callback_query_handler(
        bai_test_start, lambda c: c.data == 'start_bai_test')
    dp.register_callback_query_handler(
        bai_test_questions, state=FSM_bai_test_form.q)
    dp.register_callback_query_handler(
        bai_test_result_record, state=FSM_bai_test_form.result)
    # bdi test dinamics handlers
    dp.register_callback_query_handler(bai_test_dinamics_lastresult, lambda c: c.data == 'bai_test_lastweek_change')
    dp.register_callback_query_handler(bai_test_dinamic_lastmonth, lambda c: c.data == 'bai_test_lastmonth_change')