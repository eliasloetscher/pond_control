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
    :return: Connection object or None
    """
    db_file = '/home/pi/teich.db'
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn


def update_days(conn, time):
    """
    Update the days table. If day already exists, sum up time.
    If not, add day and set time
    """
    
    # sql = SELECT COUNT(*) FROM days WHERE date = date();
    
    cur = conn.cursor()
    sql = "SELECT COUNT(*) FROM days WHERE date = ?"
    var = [str(date.today())]
    cur.execute(sql, var)
    rows = cur.fetchall()
    print(rows[0][0])
    if rows[0][0] == 0:
        with conn:
            sql = "INSERT INTO days (date, secs) VALUES (?,?)"
            update = (str(date.today()), time)
            cur.execute(sql, update)
    else:
        result = cur.execute("SELECT secs FROM days WHERE date = date()")
        result = cur.fetchall()
        print(result)
        print(result[0])
        print(result[0][0])



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
GPIO.setup(21, GPIO.IN)  # Water sensor state

# Open Database connection
conn = create_connection()

# Initialize refill counter
counter = 0

# Set state to OK
time.sleep(5)
with open("state.txt", "w") as file:
    file.write("OK")

add_action(conn, "PROGRAM STARTED")
time.sleep(1)

while True:

    # Detect low water level (GPIO 21 is HIGH)
    if GPIO.input(21) == 1:
        add_action(conn, "WS: Low water level")
        time.sleep(1)
        add_action(conn, "START REFILLING")
        time.sleep(1)
        while GPIO.input(21) == 1:
            # start to refill
            add_action(conn, "VALVE: ON (runtime)")
            GPIO.output(4, GPIO.HIGH)
            time.sleep(30)  # fill time
            GPIO.output(4, GPIO.LOW)
            add_action(conn, "VALVE: OFF (runtime)")
            time.sleep(1)

            # increase refill counter
            counter += 1

            # Safety measure if valve is on for more than 10 times (30 seconds each) and water level is not HIGH again
            if counter >= 10:
                # Set state to ERROR
                with open("state.txt", "w") as file:
                    file.write("ERROR")
                add_action(conn, "ERROR, tried 10 times to refill and WS is not high")

                # Terminate python routine
                sys.exit(0)

            # wait two minutes before checking water level
            time.sleep(120)

        counter = 0
        add_action(conn, "WS: High water level")
        time.sleep(1)
        add_action(conn, "VALVE: ON (final, runtime)")
        GPIO.output(4, GPIO.HIGH)
        time.sleep(30)  # fill time
        GPIO.output(4, GPIO.LOW)
        add_action(conn, "VALVE: OFF (final, runtime)")
        time.sleep(1)
        add_action(conn, "REFILLING COMPLETED")

    # Wait for 5 minutes to recheck for low water level
    time.sleep(300)

