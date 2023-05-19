import sqlite3

# CREATING TABLES
def sql_start():
    global con, cur
    con = sqlite3.connect('tutorial.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        achievement_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        achievement TEXT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS bdi_test_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        result INTEGER);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS bai_test_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
        result INTEGER);
        """)
    con.commit()


# EVENTS QUERIES

# Insert new event
async def sql_add_event(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO events 
        (event_id, good_or_bad, event, physical, feelings, thoughts, current_thoughts) 
        VALUES (NULL, ?, ?, ?, ?, ?, ?)""", tuple(data.values()))
        con.commit()


# Get all events
async def sql_get_events_all():
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    return rows

# Get events years
async def sql_get_events_years():
    cur.execute("SELECT DISTINCT event_year FROM events")
    event_years = cur.fetchall()
    return event_years

# Get events months
async def sql_get_events_months(year):
    cur.execute("SELECT DISTINCT event_month FROM events WHERE event_year=?", (year,))
    months = cur.fetchall()
    return months

#Get good or bad events in a year
async def sql_count_events_year(good_or_bad, year):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE good_or_bad=?
                    AND event_year=?""", (good_or_bad, year,))
    months = cur.fetchall()
    return months

# Get events days
async def sql_get_events_days(year, month):
    cur.execute("SELECT DISTINCT event_day FROM events WHERE event_year=? AND event_month=?", (year, month,))
    days = cur.fetchall()
    return days

#Get good or bad events in a month
async def sql_count_events_month(good_or_bad, year, month):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE good_or_bad=?
                    AND event_year=? AND event_month=?""", (good_or_bad, year, month,))
    events_qty = cur.fetchall()
    return events_qty

# Get events in a day
async def sql_get_events_id(year, month, day):
    cur.execute("""SELECT good_or_bad, event_id, event 
                FROM events 
                WHERE event_year=? 
                AND event_month=? 
                AND event_day=?""", (year, month, day,))
    ids = cur.fetchall()
    return ids

#Get good or bad events in a day
async def sql_count_events_day(good_or_bad, year, month, day):
    cur.execute("""SELECT COUNT(*) 
                    FROM events 
                    WHERE good_or_bad=?
                    AND event_year=? 
                    AND event_month=?
                    AND event_day=?""", (good_or_bad, year, month, day,))
    events_qty = cur.fetchall()
    return events_qty

# Get chosen event
async def sql_get_chosen_event(event_id):
    cur.execute("""SELECT event, physical,feelings,thoughts, current_thoughts 
                    FROM events
                    WHERE event_id=?""", (event_id,))
    event_description = cur.fetchall()
    return event_description[0]


# ACHIEVEMENT QUERIES

# Insert achievement
async def sql_add_achievement(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO achievements 
            (achievement_id, achievement) 
            VALUES (NULL, ?)""", tuple(data.values()))
        con.commit()

# Get total qty of achievements
async def sql_count_achievements():
    cur.execute("SELECT COUNT(*) FROM achievements")
    rows = cur.fetchall()[0][0]
    return rows

# BDI TEST QUERIES

# Insert a new result
async def sql_bditest_insert_result(result):
    cur.execute("INSERT INTO bdi_test_results (result) VALUES (?)", tuple([result]))
    con.commit()


# Get last result
async def sql_bditest_last_result():
    cur.execute("SELECT result FROM bdi_test_results ORDER BY result_id DESC LIMIT 1")
    result = cur.fetchall()
    return result

# Get last week averege
async def sql_bditest_lastweek_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')")
    result = cur.fetchall()
    return result

# Get a week before averege
async def sql_bditest_previousweek_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE date BETWEEN datetime('now', '-13 days') AND datetime('now', '-6 days')")
    result = cur.fetchall()
    return result

# Get a current month averege
async def sql_bditest_currentmonth_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bdi_test_results WHERE date BETWEEN datetime('now', '-30 days') AND datetime('now', 'localtime')")
    result = cur.fetchall()
    return result


# BAI TEST QUERIES
# Insert a new result
async def sql_baitest_insert_result(result):
    cur.execute("INSERT INTO bai_test_results (result) VALUES (?)", tuple([result]))
    con.commit()


# Get last result
async def sql_baitest_last_result():
    cur.execute("SELECT result FROM bai_test_results ORDER BY result_id DESC LIMIT 1")
    result = cur.fetchall()
    return result

# Get last week averege
async def sql_baitest_lastweek_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime')")
    result = cur.fetchall()
    return result

# Get a week before averege
async def sql_baitest_previousweek_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE date BETWEEN datetime('now', '-13 days') AND datetime('now', '-6 days')")
    result = cur.fetchall()
    return result

# Get a current month averege
async def sql_baitest_currentmonth_result():
    cur.execute("SELECT ROUND(AVG(result)) FROM bai_test_results WHERE date BETWEEN datetime('now', '-30 days') AND datetime('now', 'localtime')")
    result = cur.fetchall()
    return result