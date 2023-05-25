from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


first_choise = InlineKeyboardMarkup(row_width=1)
first_choise.add(InlineKeyboardButton(text="Переживания", callback_data="events"), 
                 InlineKeyboardButton(text="Достижения", callback_data="achievements"), 
                 InlineKeyboardButton(text="Отслеживание состояния", callback_data="tests"), 
                 InlineKeyboardButton(text="Теория", callback_data="theory"))

# ACHIEVEMENTS KEYBOARD
achievements_choise = InlineKeyboardMarkup(row_width=1)
achievements_choise.add(InlineKeyboardButton(text="Записать достижение",
                            callback_data="record_achievement"),
                        InlineKeyboardButton(
                            text="Узнать количество достижений", callback_data="count_achievements"),
                        InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# EVENTS KEYBOARDS
# Starting events muttons
event_start = InlineKeyboardMarkup(row_width=1)
event_start.add(InlineKeyboardButton(text="Записать переживание",
                          callback_data="record_event"),
                InlineKeyboardButton(text="Описание", callback_data="events_description"),
                InlineKeyboardButton(text="Вспомнить события", callback_data="events_get"),
                InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# record events keyboards
event_choise = InlineKeyboardMarkup(row_width=1)
event_choise.add(InlineKeyboardButton(text="Приятное", callback_data="good"),
                 InlineKeyboardButton(text="Неприятное", callback_data="bad"),
                 InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# finishing record events keyboards
event_finish = InlineKeyboardMarkup(row_width=1)
event_finish.add(InlineKeyboardButton(text="Записать", callback_data="load"),
                 InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


#BDI TEST KEYBOARDS
# answers
bdi_test_answers_kb = InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)
bdi_test_answers_kb.add(InlineKeyboardButton(text="а", callback_data="bdi_test_answer_0"),
                        InlineKeyboardButton(text="б", callback_data="bdi_test_answer_1"),
                        InlineKeyboardButton(text="в", callback_data="bdi_test_answer_2"),
                        InlineKeyboardButton(text="г", callback_data="bdi_test_answer_3")
                        ).row(InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# test first choise
bdi_test_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_kb.add(InlineKeyboardButton(text="Пройти тест", callback_data="start_bdi_test"),
                InlineKeyboardButton(text="Отследить динамику", callback_data="bdi_test_dynamic"),
                InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# starting the test
bdi_test_start_kb = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
bdi_test_start_kb.add(InlineKeyboardButton(text="Начать", callback_data="begin_bdi_test"),
                      InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


# bdi test dinamics keyboard
bdi_test_dinamics_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_dinamics_kb.add(InlineKeyboardButton(text="Сравнить с предыдущей неделей", callback_data="bdi_test_lastweek_change"),
                         InlineKeyboardButton(text="Изменения за последний месяц", callback_data="bdi_test_lastmonth_change"),
                         InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# end of the bdi test
bdi_test_end_kb = InlineKeyboardMarkup(row_width=1)
bdi_test_end_kb.add(InlineKeyboardButton(text="Записать и перейти к результатам", callback_data="bdi_test_end"),
                    InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

#BAI TEST KEYBOARDS
bai_test_answers_kb = InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)
bai_test_answers_kb.add(InlineKeyboardButton(text="а", callback_data="bai_test_answer_0"),
                        InlineKeyboardButton(text="б", callback_data="bai_test_answer_1"),
                        InlineKeyboardButton(text="в", callback_data="bai_test_answer_2"),
                        InlineKeyboardButton(text="г", callback_data="bai_test_answer_3")
                        ).row(InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# first choise
bai_test_kb = InlineKeyboardMarkup(row_width=1)
bai_test_kb.add(InlineKeyboardButton(text="Пройти тест", callback_data="start_bai_test"),
                InlineKeyboardButton(text="Отследить динамику", callback_data="bai_test_dynamic"),
                InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


# starting the test
bai_test_start_kb = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
bai_test_start_kb.add(InlineKeyboardButton(text="Начать", callback_data="begin_bai_test"),
                      InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


# bai test dinamics keyboard
bai_test_dinamics_kb = InlineKeyboardMarkup(row_width=1)
bai_test_dinamics_kb.add(InlineKeyboardButton(text="Сравнить с предыдущей неделей", callback_data="bai_test_lastweek_change"),
                         InlineKeyboardButton(text="Изменения за последний месяц", callback_data="bai_test_lastmonth_change"),
                         InlineKeyboardButton(text="В главное меню", callback_data="cancel"))

# end of the bai test
bai_test_end_kb = InlineKeyboardMarkup(row_width=1)
bai_test_end_kb.add(InlineKeyboardButton(text="Записать и перейти к результатам", callback_data="bai_test_end"),
                    InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


# TEST CHOISE KEYBOARD
test_kb = InlineKeyboardMarkup(row_width=1)
test_kb.add(InlineKeyboardButton(text="Уровень депрессии", callback_data="bdi_test"),
            InlineKeyboardButton(text="Уровень тревоги", callback_data="bai_test"),
            InlineKeyboardButton(text="В главное меню", callback_data="cancel"))


