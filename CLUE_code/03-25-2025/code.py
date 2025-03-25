from CSV_Maker import CSV_Maker
from Filter import SMA
from Detect_Max import Detect_Max
import random
import time
import board
import adafruit_bmp280
import storage

storage.remount("/", readonly=False)

i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = bmp280.pressure

data_names = ['Time', 'Raw', 'SMA']

f = CSV_Maker('Altitude', data_names, 'w')
sma = SMA(0, 5)
apogee = Detect_Max('Apogee')

f.create_file()

print('File created')

start_time = time.monotonic()

print('Writing file')

for i in range (100):
    elapsed_time = time.monotonic() - start_time
    raw = bmp280.altitude
    sma_value = sma.update(raw)
    apogee.update((sma_value, elapsed_time))
    data = (elapsed_time, raw, sma_value)
    f.write_file(data)
    time.sleep(0.05)
apogee.write_max(f.get_file_name())

print('File completed')

storage.remount("/", readonly=True)
