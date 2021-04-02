import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
from datetime import date
from pond_control.parameters import Parameters
from pond_control.database_control import DatabaseControl

# Initialize GPIOS
GPIO.setmode(GPIO.BCM)  # BCM is gpio number, BOARD is pin number
GPIO.setup(4, GPIO.OUT)  # Switch Power MOSFET
GPIO.setup(21, GPIO.IN)  # Water sensor state

# Create database instance
db_control = DatabaseControl()

# Init var for system sate file
state_file = Parameters.SYSTEM_STATE_FILE

# Initialize refill counter
counter = 0

# Set system state to OK
time.sleep(5)
with open(state_file, "w") as file:
    file.write("OK")

db_control.add_action("PROGRAM STARTED")

while True:

    # check system state
    with open(state_file, "r") as file:
        system_state = str(file.read())

    # execute runtime only if system state is "OK"
    if system_state == "OK":

        # Detect low water level (GPIO 21 is HIGH)
        if GPIO.input(21) == 1:
            db_control.add_action("WS: Low water level")
            db_control.add_action("START REFILLING")
            while GPIO.input(21) == 1:
                # start to refill
                db_control.add_action("VALVE: ON (runtime)")
                GPIO.output(4, GPIO.HIGH)
                time.sleep(Parameters.FILL_TIME)
                GPIO.output(4, GPIO.LOW)
                db_control.add_action("VALVE: OFF (runtime)")
                db_control.update_refill_time(Parameters.FILL_TIME)
                time.sleep(1)

                # increase refill counter
                counter += 1

                # Safety measure if valve is on for a given number of refilling iterations
                if counter >= Parameters.ERROR_COUNTER:
                    # Set state to ERROR
                    with open(state_file, "w") as file:
                        file.write("ERROR")
                    db_control.add_action("ERROR, water sensor does not recognize the refilling process")

                # wait time until water level sensor is checked again
                time.sleep(Parameters.POLLING_PERIOD_WATER_SENSOR)

            # finish refilling process
            counter = 0
            db_control.add_action("REFILLING COMPLETED")

        # wait time until water level sensor is check again
        time.sleep(Parameters.POLLING_PERIOD_WATER_SENSOR)

    # if system state is in ERROR (i.e. not "OK")
    else:
        # waite time until next iteration with new system state check
        time.sleep(Parameters.SYSTEM_CHECK_TIME)
