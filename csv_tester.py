from csv import csv
import time
import storage
from adafruit_clue import clue

data_names = ['time', 'altitude', 'temperature']
file = csv('altitude', data_names)
while True:
    if clue.button_a:
        storage.remount("/", readonly=False)

        file.create_file()
        
        start_time = time.monotonic()
        elapsed_time = 0
        altitude = 0
        temperature = 0
        clue.sea_level_pressure = clue.pressure
        
        print('logging')
        
        while True:
            if clue.button_b:
                break
            elapsed_time = time.monotonic() - start_time
            altitude = clue.altitude
            temperature = clue.temperature
            data = (elapsed_time, altitude, temperature)
            file.write_file(data)
            time.sleep(0.05)
        storage.remount("/", readonly=True)
    # if clue.button_b:
       # break
