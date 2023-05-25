from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import sqlite_db

#ALL BUTTONS
b1 = InlineKeyboardButton(text="Записать переживание",
                          callback_data="record_event")
b2 = InlineKeyboardButton(text="Записать достижение",
                          callback_data="record_achievement")
b3 = InlineKeyboardButton(text="Приятное", callback_data="good")
b4 = InlineKeyboardButton(text="Неприятное", callback_data="bad")
b5 = InlineKeyboardButton(text="В главное меню", callback_data="cancel")
b6 = InlineKeyboardButton(text="Записать", callback_data="load")
b7 = InlineKeyboardButton(
    text="Узнать количество достижений", callback_data="count_achievements")
b8 = InlineKeyboardButton(text="Переживания", callback_data="events")
b9 = InlineKeyboardButton(text="Достижения", callback_data="achievements")
b10 = InlineKeyboardButton(text="Теория", callback_data="theory")
b11 = InlineKeyboardButton(text="Описание", callback_data="events_description")
b12 = InlineKeyboardButton(text="Вспомнить события", callback_data="events_get")
b13 = InlineKeyboardButton(text="Отслеживание состояния", callback_data="tests")
b14 = InlineKeyboardButton(text="Пройти тест", callback_data="start_bdi_test")
b15 = InlineKeyboardButton(text="Отследить динамику", callback_data="bdi_test_dynamic")
b16 = InlineKeyboardButton(text="а", callback_data="bdi_test_answer_0")
b17 = InlineKeyboardButton(text="б", callback_data="bdi_test_answer_1")
b18 = InlineKeyboardButton(text="в", callback_data="bdi_test_answer_2")
b19 = InlineKeyboardButton(text="г", callback_data="bdi_test_answer_3")
b20 = InlineKeyboardButton(text="Начать", callback_data="begin_bdi_test")
b21 = InlineKeyboardButton(text="Сравнить с предыдущей неделей", callback_data="bdi_test_lastweek_change")
b22 = InlineKeyboardButton(text="Изменения за последний месяц", callback_data="bdi_test_lastmonth_change")
b23 = InlineKeyboardButton(text="Записать и перейти к результатам", callback_data="bdi_test_end")
b24 = InlineKeyboardButton(text="а", callback_data="bai_test_answer_0")
b25 = InlineKeyboardButton(text="б", callback_data="bai_test_answer_1")
b26 = InlineKeyboardButton(text="в", callback_data="bai_test_answer_2")
b27 = InlineKeyboardButton(text="г", callback_data="bai_test_answer_3")
b28 = InlineKeyboardButton(text="Пройти тест", callback_data="start_bai_test")
b29 = InlineKeyboardButton(text="Отследить динамику", callback_data="bai_test_dynamic")
b30 = InlineKeyboardButton(text="Начать", callback_data="begin_bai_test")
b31 = InlineKeyboardButton(text="Сравнить с предыдущей неделей", callback_data="bai_test_lastweek_change")
b32 = InlineKeyboardButton(text="Изменения за последний месяц", callback_data="bai_test_lastmonth_change")
b33 = InlineKeyboardButton(text="Записать и перейти к результатам", callback_data="bai_test_end")
b34 = InlineKeyboardButton(text="Уровень депрессии", callback_data="bdi_test")
b35 = InlineKeyboardButton(text="Уровень тревоги", callback_data="bai_test")


# FIRST CHOISE KEYBOARDS
# first_choise = InlineKeyboardMarkup(row_width=1)
# first_choise.row(b8, b9).add(b13).add(b10)





first_choise = InlineKeyboardMarkup(row_width=1)
first_choise.row(InlineKeyboardButton(text="Переживания", callback_data="events"), 
                 InlineKeyboardButton(text="Достижения", callback_data="achievements"), 
                 InlineKeyboardButton(text="Отслеживание состояния", callback_data="tests"), 
                 InlineKeyboardButton(text="Теория", callback_data="theory"))

# ACHIEVEMENTS KEYBOARD
achievements_choise = InlineKeyboardMarkup(row_width=1)
achievements_choise.add(b2).add(b7).add(b5)

# EVENTS KEYBOARDS
# Starting events muttons
event_start = InlineKeyboardMarkup(row_width=1)
event_start.add(b1).add(b11).add(b12).add(b5)

# record events buttons
event_choise = InlineKeyboardMarkup(row_width=1)
event_choise.add(b3).add(b4).add(b5)

event_finish = InlineKeyboardMarkup(row_width=1)
event_finish.add(b6).add(b5)


#BDI TEST KEYBOARDS
# answers
bdi_test_answers_kb = InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)
bdi_test_answers_kb.add(b16, b17, b18, b19).row(b5)

# test first choise
bdi_test_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_kb.add(b14, b15).add(b5)


# starting the test
bdi_test_start_kb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
bdi_test_start_kb.add(b20).row(b5)


# bdi test dinamics keyboard
bdi_test_dinamics_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_dinamics_kb.add(b21, b22).row(b5)

# end of the bdi test
bdi_test_end_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_end_kb.add(b23, b5)

#BAI TEST KEYBOARDS
bai_test_answers_kb = InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)
bai_test_answers_kb.add(b24, b25, b26, b27).row(b5)

# first choise
bai_test_kb = InlineKeyboardMarkup(row_width=1)
bai_test_kb.add(b28, b29).row(b5)


# starting the test
bai_test_start_kb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
bai_test_start_kb.add(b30).row(b5)


# bai test dinamics keyboard
bai_test_dinamics_kb = InlineKeyboardMarkup(row_width=1)
bai_test_dinamics_kb.add(b31, b32).row(b5)

# end of the bai test
bai_test_end_kb = InlineKeyboardMarkup(row_width=1)
bai_test_end_kb.add(b33, b5)


# TEST CHOISE KEYBOARD
test_kb = InlineKeyboardMarkup(row_width=1)
test_kb.add(b34, b35, b5)


