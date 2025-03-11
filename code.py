import time
import board
import storage
import adafruit_bmp280
from adafruit_clue import clue
import displayio
import terminalio
from adafruit_display_text import label

i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = bmp280.pressure

# Kalman filter class
class KalmanFilter:
    def __init__(self, process_variance, measurement_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def update(self, measurement):
        # Kalman gain
        kalman_gain = self.posteri_error_estimate / (self.posteri_error_estimate + self.measurement_variance)

        # Update the estimate with the measurement
        a_priori_estimate = self.posteri_estimate
        self.posteri_estimate = a_priori_estimate + kalman_gain * (measurement - a_priori_estimate)

        # Update the error estimate
        self.posteri_error_estimate = (1 - kalman_gain) * self.posteri_error_estimate + self.process_variance

        return self.posteri_estimate

kalman_filter = KalmanFilter(process_variance=0.1, measurement_variance=1.0, estimated_measurement_variance=1.0)

display = clue.display
mode = True  # True = Filtered, False = Unfiltered

# Create Display Elements
text = displayio.Group(scale=2)

data_text = label.Label(terminalio.FONT, text="Height: ---", color=0xFFFFFF)
data_text.anchor_point = (0.5, 0.5)
data_text.anchored_position = (120 // 2, 120 // 2)
text.append(data_text)

title_text = label.Label(terminalio.FONT, text="FILTERED", color=0xFFFFFF)
title_text.anchor_point = (0.5, 0.5)
title_text.anchored_position = (120 // 2, 50 // 2)
text.append(title_text)

display.root_group = text

while True:
    title_text.color = 0xFFFFFF
    if clue.button_a:
        mode = not mode
        time.sleep(0.2)  # Debounce delay to prevent rapid toggling

    if clue.button_b:
        bmp280.sea_level_pressure = bmp280.pressure
        title_text.color = 0xFF0000
        print("RESET")
        time.sleep(0.2)  # Debounce delay

    if clue.button_a and clue.button_b:
        title_text.text = "CREATING FILE"
        break  # Exit loop to start logging

    raw_height = bmp280.altitude
    print(f"Raw height: {raw_height:.3f} meters")

    if mode:
        filtered_height = kalman_filter.update(raw_height)
    else:
        filtered_height = raw_height

    print(f"Filtered height: {filtered_height:.3f} meters")

    data_text.text = f"Height: {filtered_height:.3f}m"
    title_text.text = "FILTERED" if mode else "UNFILTERED"

    display.root_group = text
    time.sleep(0.1)

# Data Logging
print("Starting data logging...")
storage.remount("/", readonly=False)

file_path = "/altitude.csv"
file_exists = False

# Check if file already exists
try:
    with open(file_path, "r") as check_file:
        file_exists = True
except OSError:
    pass  # File does not exist, will be created

with open(file_path, "a") as fp:
    if not file_exists:
        fp.write("TIME,UNFILTERED,FILTERED\n")

    initial_time = time.monotonic()
    while (the_time := time.monotonic() - initial_time) < 10:
        unfiltered = bmp280.altitude
        filtered = kalman_filter.update(unfiltered)
        fp.write(f"{the_time:.2f},{unfiltered:.3f},{filtered:.3f}\n")
        time.sleep(0.1)

storage.remount("/", readonly=True)
print("Data logging completed.")
