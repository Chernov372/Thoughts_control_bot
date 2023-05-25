from aiogram import types, Dispatcher
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import bdi_test_kb, bdi_test_answers_kb, bdi_test_start_kb, first_choise, bdi_test_dinamics_kb, bdi_test_end_kb
from forms import bdi_test_questions
# from create_bot import bot


questions = bdi_test_questions.male_questions


# CBI TEST FIRST CHOISE
async def bdi_test_first_choise(cbq: types.CallbackQuery):
    await cbq.message.delete()
    await cbq.message.answer("В этом разделе вы можете пройти тест на определения уровня депрессии и отслеживать динамику его результатов.\n\nВажно:\nтест не может быть использован для самостоятельной постановки диагноза! В случае любых сомнений обращайтесь к квалифицированным специалистам.", reply_markup=bdi_test_kb)


# TEST PART
class FSM_bdi_test_form(StatesGroup):
    q = State()
    result = State()

# Starting a test
async def bdi_test_start(cbq: types.CallbackQuery, state=None):
    await FSM_bdi_test_form.q.set()
    async with state.proxy() as data:
        data['q_num'] = 1
        data['sum'] = 0
    await cbq.message.delete()
    await cbq.message.answer("""В этом опроснике содержатся группы утверждений.

Внимательно прочитайте каждую группу утверждений.

Затем определите в каждой группе одно утверждение, которое лучше всего соответствует тому, как вы себя чувствовали на этой неделе и сегодня.""", reply_markup=bdi_test_start_kb)


async def bdi_test_questions(cbq: types.CallbackQuery, state=FSMContext):
    if cbq.data == 'cancel':
        await state.finish()
        await cbq.message.delete()
        await cbq.message.answer("Прохождение теста отменено.\n\nПродолжим работу\nВыберите раздел:", reply_markup=first_choise)
    else:
        q_num = (await state.get_data())['q_num']
        if cbq.data.startswith('bdi_test_answer'):
            answer = int(cbq.data.split('_')[3])
        else:
            answer = 0
        if q_num > 21:
            await state.update_data(sum=(await state.get_data())['sum']+answer)
            await cbq.message.delete()
            await cbq.message.answer("Тест завершён!", reply_markup=bdi_test_end_kb)
            await FSM_bdi_test_form.next()
        else:
            await cbq.message.answer(f"{questions[f'q{q_num}']}", reply_markup=bdi_test_answers_kb)
            await cbq.message.delete()
            await state.update_data(sum=(await state.get_data())['sum']+answer)
            await state.update_data(q_num=q_num+1)

# Recording results
async def bdi_test_result_record(cbq: types.CallbackQuery, state=FSMContext):
    result = (await state.get_data())['sum']
    try:
        last_result = (await sqlite_db.sql_bditest_last_result(cbq.message.chat.id))[0][0]
    except:
        last_result = await sqlite_db.sql_bditest_last_result(cbq.message.chat.id)
    await sqlite_db.sql_bditest_insert_result(cbq.message.chat.id, result)
    if last_result == [] or result >= last_result:
        if result <= 9:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на то, что у Вас отсутствуют депрессивыне симптомы.\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 10 <= result <= 15:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие лёгкой депрессии\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 16 <= result <= 19:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие умеренной депрессии\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 20 <= result <= 29:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие выраженной депрессии средней тяжести\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие тяжёлой депрессии\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
    elif result < last_result:
        if result <= 9:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на то, что у Вас отсутствуют депрессивыне симптомы.\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 10 <= result <= 15:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие лёгкой депрессии\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что у Вас наблюдается улучшение состояния. Так держать!\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 16 <= result <= 19:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие умеренной депрессии\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что у Вас наблюдается улучшение состояния. Так держать!\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        elif 20 <= result <= 29:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие выраженной депрессии средней тяжести\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что у Вас наблюдается улучшение состояния. Так держать!\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"""Вы прошли тест!\nВаш результат: {result} из 63\n\nЭтот результат указывает на наличие тяжёлой депрессии\n\nТем не менее, этот результат на {last_result-result} меньше, чем предыдущий, что говорит о том, что у Вас наблюдается улучшение состояния. Так держать!\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём с начала. Выберите раздел""", reply_markup=first_choise)
    await state.finish()
    await cbq.message.delete()

# TEST DINAMIC PART
# asking user what dynamic to choose
async def bdi_test_dinamic_choise(cbq: types.CallbackQuery):
    await cbq.message.delete()
    await cbq.message.answer("В этом разделе Вы можете отслеживать изменения своего состояния.\nКакие изменения Вас интересуют?", reply_markup=bdi_test_dinamics_kb)

# comparing with a previous week
async def bdi_test_dinamics_lastresult(cbq: types.CallbackQuery):
    last_week_results = (await sqlite_db.sql_bditest_lastweek_result(cbq.message.chat.id))[0][0]
    previous_week_result = (await sqlite_db.sql_bditest_previousweek_result(cbq.message.chat.id))[0][0]
    if last_week_results == None:
        await cbq.message.delete()
        await cbq.message.answer("Вы не проходили тест за последнюю неделю", reply_markup=bdi_test_kb)
    else:
        if previous_week_result == None:
            await cbq.message.delete()
            await cbq.message.answer(f"""Cредний показатель теста за неделю - {int(last_week_results)} из 63\n\nК сожалению сравнить с предыдущей неделей не получится, так как Вы не проходили тест неделю назад\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        else:
            if last_week_results < previous_week_result:
                await cbq.message.delete()
                await cbq.message.answer(f"""Вы делаете успехи!\nCредний показатель теста за неделю - {int(last_week_results)} из 63\n\nПо сравнению с предыдущей неделей средний результат теста стал меньше на {int(previous_week_result-last_week_results)}. Это может означать, что уровень Вашей депрессии снизился\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
            else:
                await cbq.message.delete()
                await cbq.message.answer(f"""Cредний показатель теста за неделю - {int(last_week_results)} из 63\n\nПо сравнению с предыдущей неделей средний результат теста стал больше на {int(last_week_results-previous_week_result)}. Продолжайте работу над собой и своими чувствами.\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)

# comparing last result with last 30 days averege
async def bdi_test_dinamic_lastmonth(cbq: types.CallbackQuery):
    current_month_result = (await sqlite_db.sql_bditest_currentmonth_result(cbq.message.chat.id))[0][0]
    try:
        last_result = (await sqlite_db.sql_bditest_last_result(cbq.message.chat.id))[0][0]
    except:
        last_result = await sqlite_db.sql_bditest_last_result(cbq.message.chat.id)
    if last_result == []:
        await cbq.message.answer("Вы ещё ни разу не проходили тест на уровень депрессии")
    else:
        await cbq.message.delete()
        if last_result < current_month_result:
            await cbq.message.answer(f"""Вы делаете успехи!\nПоследний результат теста - {int(last_result)} из 63\n\nПо сравнению со средним значением за последние 30 дней, результат теста стал меньше на {int(current_month_result-last_result)}. Это может означать, что уровень Вашей депрессии снизился!\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        elif last_result == current_month_result:
            await cbq.message.answer(f"""Последний результат теста - {int(last_result)} из 63\n\nПо сравнению со средним значением за последние 30 дней, результат теста не изменился. Продолжайте работу над собой и своими чувствами.\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)
        else:
            await cbq.message.answer(f"""Последний результат теста - {int(last_result)} из 63\n\nПо сравнению со средним значением за последние 30 дней, результат теста стал больше на {int(current_month_result-last_result)}. Продолжайте работу над собой и своими чувствами.\n\n
ВАЖНО\nНапоминаем, что результат этого теста сам по себе не может быть критерием для постановки диагноза депрессии. Диагноз может поставить только специалист по совокупности факторов.\n\n
Начнём сначала. Выберите раздел""", reply_markup=first_choise)


def register_handlers_bdi_test(dp: Dispatcher):
    # Starting test handlers
    dp.register_callback_query_handler(
        bdi_test_first_choise, lambda c: c.data == 'bdi_test')
    dp.register_callback_query_handler(
        bdi_test_dinamic_choise, lambda c: c.data == 'bdi_test_dynamic')
    # bdi test handlers
    dp.register_callback_query_handler(
        bdi_test_start, lambda c: c.data == 'start_bdi_test')
    dp.register_callback_query_handler(
        bdi_test_questions, state=FSM_bdi_test_form.q)
    dp.register_callback_query_handler(
        bdi_test_result_record, state=FSM_bdi_test_form.result)
    # bdi test dinamics handlers
    dp.register_callback_query_handler(bdi_test_dinamics_lastresult, lambda c: c.data == 'bdi_test_lastweek_change')
    dp.register_callback_query_handler(bdi_test_dinamic_lastmonth, lambda c: c.data == 'bdi_test_lastmonth_change')