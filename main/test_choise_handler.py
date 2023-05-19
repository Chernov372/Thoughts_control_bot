from aiogram import types, Dispatcher
from keyboards import test_kb



async def tests_choise(cbq: types.CallbackQuery):
    await cbq.message.answer("Этот раздел поможет Вам узнать о своём состоянии, отслеживая уровни депрессии и тревоги.\n\nВыберете подраздел", reply_markup=test_kb)
    await cbq.message.delete()



def regisetr_handlers_test_choise(dp: Dispatcher):
    dp.register_callback_query_handler(tests_choise, lambda c: c.data == 'tests')