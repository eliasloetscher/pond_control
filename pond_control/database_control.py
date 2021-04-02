import RPi.GPIO as GPIO
import time
import sqlite3
import sys
from sqlite3 import Error
from datetime import datetime
from datetime import date
from pond_control.parameters import Parameters


class DatabaseControl:

    def __init__(self):

        # init database connection
        self.db_connection = None
        try:
            self.db_connection = sqlite3.connect(Parameters.DB_FILE)
        except Error as e:
            print(e)

        # init database cursor
        self.db_cursor = self.db_connection.cursor()

    def update_refill_time(self, time):
        """

        :param time:
        :return:
        """

        # count number of rows for current month
        sql = "SELECT COUNT(*) FROM refill_time WHERE month = ?"
        month = [date.today().month]
        self.db_cursor.execute(sql, month)
        rows = self.db_cursor.fetchall()

        # check if month entry already exists
        if rows[0][0] == 0:
            # if not, insert new entry
            with self.db_connection:
                sql = "INSERT INTO refill_time (year, month, time_in_s) VALUES (?,?,?)"
                update = (str(date.today().year), str(date.today().month), time)
                self.db_cursor.execute(sql, update)
        else:
            # month entry exists
            # get refill time of the current month
            sql = "SELECT time_in_s FROM refill_time WHERE month = ?"
            update = [date.today().month]
            self.db_cursor.execute(sql, update)
            result = self.db_cursor.fetchall()

            # update refill time
            with self.db_connection:
                sum_time = result[0][0] + time
                sql = "UPDATE refill_time SET time_in_s = ? WHERE month = ?"
                update = [sum_time, date.today().month]
                self.db_cursor.execute(sql, update)

    def add_action(self, action):
        """ Add entry to actions table in db. Param action: string with action description

        :param action:
        :return:
        """

        with self.db_connection:
            sql = "INSERT INTO actions (date, time, action) VALUES (?,?,?)"

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            update = (str(date.today()), current_time, action)

            self.db_cursor.execute(sql, update)
