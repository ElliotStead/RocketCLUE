import time
import board
import busio
import adafruit_bmp280

# Initialize I2C and BMP280 (or BME280) sensor
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Set up sensor settings (optional)
bmp280.sea_level_pressure = bmp280.pressure

# CSV file path (stored in CIRCUITPY internal storage)
csv_file = "/data.csv"

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

class difference:
    def __init__(self):
        self.previous_value = 0
        self.wait = 2

    def update(self, num):
        temp = self.previous_value
        if(self.wait == 2):
            self.previous_value = num
        self.wait += 1
        return num - temp

kalman_filter = KalmanFilter(process_variance=0.1, measurement_variance=1.0, estimated_measurement_variance=1.0)

difference = difference()

# Check if file exists, create header if needed
try:
    with open(csv_file, "x") as f:
        f.write("Time (s),Altitude (m)\n")  # Write CSV header
except OSError:
    pass  # File already exists

# Logging setup
buffer = []  # RAM buffer to store readings
start_time = time.monotonic()  # Start time reference

print("Logging altitude data. Press Ctrl+C to stop.")

while True:
    # Get elapsed time and altitude
    elapsed_time = time.monotonic() - start_time
    altitude = kalman_filter.update(bmp280.altitude)

    alt_difference = difference.update(altitude)

    # Add data to buffer
    buffer.append(f"{elapsed_time:.2f},{altitude:.2f}\n")
    print(f"Time: {elapsed_time:.2f} s, Altitude: {altitude:.2f} m, Difference: {alt_difference:.2f}")

    # Flush to file every 10 entries to improve performance
    '''
    if len(buffer) >= 10:
        with open(csv_file, "a") as f:
            f.writelines(buffer)  # Fast batch writing
        buffer = []  # Clear buffer
    '''
    time.sleep(0.1)  # Adjust for desired logging rate (0.1s = 10Hz)
