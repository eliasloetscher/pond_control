import RPi.GPIO as GPIO
import time
import sqlite3
import sys
from sqlite3 import Error
from datetime import datetime
from datetime import date


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file = '/home/pi/teich.db'

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def add_action(conn, action):
    """
    Add entry to actions table in db. Param action: string with action description
    """
    with conn:
        sql = "INSERT INTO actions (date, time, action) VALUES (?,?,?)"

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        update = (str(date.today()), current_time, action)

        cur = conn.cursor()
        cur.execute(sql, update)


########################
" PROGRAM STARTS HERE "
########################

# Initialize GPIOS
GPIO.setmode(GPIO.BCM)  # BCM is gpio number, BOARD is pin number
GPIO.setup(4, GPIO.OUT)  # Switch Power MOSFET

# Open Database connection
conn = create_connection()

add_action(conn, "VALVE: ON (web)")
GPIO.output(4, GPIO.HIGH)
time.sleep(60)
# Check if valve is still on, if yes switch it off
if GPIO.input(4) == 1:
    GPIO.output(4, GPIO.LOW)
    add_action(conn, "VALVE: OFF (timeout)")


