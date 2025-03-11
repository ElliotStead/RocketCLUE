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
        self.posteri_error_estimate = (1 - kalman_gain) * self.posteri_error_estimate + abs(a_priori_estimate - self.posteri_estimate) * self.process_variance

        return self.posteri_estimate

kalman_filter = KalmanFilter(process_variance=0.1, measurement_variance=1.0, estimated_measurement_variance=1.0)

display = clue.display

# Main loop

mode = True

text = displayio.Group()
text.scale = 2
data_text = label.Label(terminalio.FONT, text=" "*10)
data_text.anchor_point = (0.5, 0.5)
data_text.anchored_position = (120/text.scale, 120/text.scale)
text.append(data_text)
title_text = label.Label(terminalio.FONT, text=" "*10)
title_text.anchor_point = (0.5, 0.5)
title_text.anchored_position = (120/text.scale, 50/text.scale)
text.append(title_text)

while True:

    title_text.color = 0xFFFFFF
    if clue.button_a:
        temp = not mode
        mode = temp
    if clue.button_b:
        bmp280.sea_level_pressure = bmp280.pressure
        title_text.color = 0xFF0000
        print("RESET")
    if clue.button_b and clue.button_a:
        title_text.text = "CREATING FILE"
        break

    raw_height = bmp280.altitude
    print(f"Raw height: {raw_height:.3f} meters")

    if mode:
        filtered_height = kalman_filter.update(raw_height)
    else:
        filtered_height = raw_height
    print(f"Filtered height: {filtered_height:.3f} meters")

    data_text.text = f"Height: {filtered_height:.3f}m"

    if mode:
        title_text.text = "FILTERED"
    else:
        title_text.text = "UNFILTERED"

    display.root_group = text

    time.sleep(0.1)

print("loading")

storage.remount("/", readonly=False)
with open("/altitude.csv", "a") as fp:
    fp.write("TIME,UNFILTERED,FILTERED\n")
    initial_time = time.monotonic()
    the_time = 0.0
    while the_time < 10:
        fp.write(f"{the_time}")
        fp.write(",")
        fp.write(f"{bmp280.altitude}")
        fp.write(",")
        fp.write(f"{kalman_filter.update(bmp280.altitude)}")
        fp.write("\n")
        time.sleep(0.1)
        the_time = time.monotonic() - initial_time
storage.remount("/", readonly=True)
print("completed")

