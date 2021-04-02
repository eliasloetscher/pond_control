from datetime import date
import sqlite3

with open("state.txt", "r") as file:
    print(file.read())

"""

db_file = '/home/pi/teich.db'
conn = sqlite3.connect(db_file)

time = 5

cur = conn.cursor()
# count number of rows for current month
sql = "SELECT COUNT(*) FROM refill_time WHERE month = ?"
month = [date.today().month]
cur.execute(sql, month)
rows = cur.fetchall()

# check if month entry already exists
if rows[0][0] == 0:
    # if not, insert new entry
    with conn:
        sql = "INSERT INTO refill_time (year, month, time_in_s) VALUES (?,?,?)"
        update = (str(date.today().year), str(date.today().month), time)
        cur.execute(sql, update)
else:
    # month entry exists
    # get refill time of the current month
    sql = "SELECT time_in_s FROM refill_time WHERE month = ?"
    update = [date.today().month]
    cur.execute(sql, update)
    result = cur.fetchall()

    # update refill time
    with conn:
        sum_time = result[0][0] + time
        sql = "UPDATE refill_time SET time_in_s = ? WHERE month = ?"
        update = [sum_time, date.today().month]
        cur.execute(sql, update)
"""