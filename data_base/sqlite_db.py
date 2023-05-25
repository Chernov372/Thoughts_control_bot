import sqlite3

# CREATING TABLES
def sql_start():
    global con, cur
    con = sqlite3.connect('tutorial.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT,
        first_name TEXT,
        last_name TEXT,
        gender TEXT);
        """)
    
    cur.execute("""CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_year DATETIME NOT NULL DEFAULT (strftime('%Y', 'now', 'localtime')),
        event_month DATETIME NOT NULL DEFAULT (strftime('%m', 'now', 'localtime')),
        event_day DATETIME NOT NULL DEFAULT (strftime('%d', 'now', 'localtime')),
        good_or_bad TEXT,
        event TEXT,
        physical TEXT,
        feelings TEXT,
        thoughts TEXT,
        current_thoughts TEXT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS achievements (
        achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        achievement TEXT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS bdi_test_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        result INTEGER);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS bai_test_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        result INTEGER);
        """)
    con.commit()

# USER TABLE QUERIES

async def sql_user_add(user_id, first_name, last_name, user_name):
    try:
        cur.execute("""INSERT INTO users (user_id, first_name, last_name, user_name) 
                    VALUES (?, ?, ?, ?)""", (user_id, first_name, last_name, user_name))
        con.commit()
    except:
        pass



# EVENTS QUERIES

# Insert new event
async def sql_add_event(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO events
        (event_id, user_id, good_or_bad, event, physical, feelings, thoughts, current_thoughts) 
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", tuple(data.values()))
        con.commit()


# Get all events
async def sql_get_events_all(user_id):
    cur.execute("SELECT * FROM events WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    return rows

# Get events years
async def sql_get_events_years(user_id):
    cur.execute("SELECT DISTINCT event_year FROM events WHERE user_id=?", (user_id,))
    event_years = cur.fetchall()
    return event_years

# Get events months
async def sql_get_events_months(user_id, year):
    cur.execute("SELECT DISTINCT event_month FROM events WHERE event_year=? AND user_id=?", (year, user_id,))
    months = cur.fetchall()
    return months

#Get good or bad events in a year
async def sql_count_events_year(user_id, good_or_bad, year):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE good_or_bad=?
                    AND event_year=? AND user_id=?""", (good_or_bad, year, user_id,))
    months = cur.fetchall()
    return months

# Get events days
async def sql_get_events_days(user_id, year, month):
    cur.execute("SELECT DISTINCT event_day FROM events WHERE user_id=? AND event_year=? AND event_month=?", (user_id, year, month,))
    days = cur.fetchall()
    return days

#Get good or bad events in a month
async def sql_count_events_month(user_id, good_or_bad, year, month):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE user_id=?
                    AND good_or_bad=?
                    AND event_year=?
                    AND event_month=?""", (user_id, good_or_bad, year, month,))
    events_qty = cur.fetchall()
    return events_qty

# Get events in a day
async def sql_get_events_id(user_id, year, month, day):
    cur.execute("""SELECT good_or_bad, event_id, event 
                FROM events 
                WHERE user_id=?
                AND event_year=? 
                AND event_month=? 
                AND event_day=?""", (user_id, year, month, day,))
    ids = cur.fetchall()
    return ids

#Get good or bad events in a day
async def sql_count_events_day(user_id, good_or_bad, year, month, day):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE user_id=?
                    AND good_or_bad=?
                    AND event_year=? 
                    AND event_month=?
                    AND event_day=?""", (user_id, good_or_bad, year, month, day,))
    events_qty = cur.fetchall()
    return events_qty

# Get chosen event
async def sql_get_chosen_event(user_id, event_id):
    cur.execute("""SELECT event, physical,feelings,thoughts, current_thoughts 
                    FROM events
                    WHERE user_id=?
                    AND event_id=?""", (user_id, event_id,))
    event_description = cur.fetchall()
    return event_description[0]


# ACHIEVEMENT QUERIES

# Insert achievement
async def sql_add_achievement(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO achievements 
            (achievement_id, user_id, achievement) 
            VALUES (NULL, ?, ?)""", tuple(data.values()))
        con.commit()

# Get total qty of achievements
async def sql_count_achievements(user_id):
    cur.execute("SELECT COUNT(*) FROM achievements WHERE user_id=?", (user_id,))
    rows = cur.fetchall()[0][0]
    return rows

# BDI TEST QUERIES

# Insert a new result
async def sql_bditest_insert_result(user_id, result):
    cur.execute("INSERT INTO bdi_test_results (user_id, result) VALUES (?, ?)", (user_id, result))
    con.commit()


# Get last result
async def sql_bditest_last_result(user_id):
    cur.execute("SELECT result FROM bdi_test_results WHERE user_id=? ORDER BY result_id DESC LIMIT 1", (user_id,))
    result = cur.fetchall()
    return result

# Get last week averege
async def sql_bditest_lastweek_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')", (user_id,))
    result = cur.fetchall()
    return result

# Get a week before averege
async def sql_bditest_previousweek_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-13 days') AND datetime('now', '-6 days')", (user_id,))
    result = cur.fetchall()
    return result

# Get a current month averege
async def sql_bditest_currentmonth_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-30 days') AND datetime('now', 'localtime')", (user_id,))
    result = cur.fetchall()
    return result


# BAI TEST QUERIES
# Insert a new result
async def sql_baitest_insert_result(user_id, result):
    cur.execute("INSERT INTO bai_test_results (user_id, result) VALUES (?, ?)", (user_id, result))
    con.commit()


# Get last result
async def sql_baitest_last_result(user_id):
    cur.execute("SELECT result FROM bai_test_results WHERE user_id=? ORDER BY result_id DESC LIMIT 1", (user_id,))
    result = cur.fetchall()
    return result

# Get last week averege
async def sql_baitest_lastweek_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')", (user_id,))
    result = cur.fetchall()
    return result

# Get a week before averege
async def sql_baitest_previousweek_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-13 days') AND datetime('now', '-6 days')", (user_id,))
    result = cur.fetchall()
    return result

# Get a current month averege
async def sql_baitest_currentmonth_result(user_id):
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE user_id=? AND date BETWEEN datetime('now', '-30 days') AND datetime('now', 'localtime')", (user_id,))
    result = cur.fetchall()
    return result