import time
import math
import displayio
from adafruit_clue import clue
from adafruit_display_shapes.rect import Rect

# Initialize display
clue_display = clue.display

# Create a Group for display elements
group = displayio.Group()

# Create a rectangle
rect = Rect(x=50, y=50, width=20, height=40, fill=0xFFFFFF)
group.append(rect)
clue_display.root_group = group  # Ensure display updates

# Filter parameters for quaternion (complementary filter constant)
alpha = 0.98

# Initial quaternion values (assuming no rotation initially)
q0, q1, q2, q3 = 1.0, 0.0, 0.0, 0.0

# Time tracking
last_time = time.monotonic()

# Screen center coordinates
screen_center_x = 120
screen_center_y = 80

# Sensitivity factor (larger values mean less movement for the same tilt)
sensitivity = 150  # Increase sensitivity for debugging

def normalize_vector(v):
    norm = math.sqrt(sum(i**2 for i in v))
    return tuple(i / norm for i in v) if norm != 0 else v

def quaternion_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt):
    global q0, q1, q2, q3
    
    # Convert gyro data to radians per second
    gx, gy, gz = math.radians(gx), math.radians(gy), math.radians(gz)
    
    # Normalize accelerometer and magnetometer data
    ax, ay, az = normalize_vector((ax, ay, az))
    mx, my, mz = normalize_vector((mx, my, mz))
    
    # Compute the quaternion derivative
    dq0 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz)
    dq1 = 0.5 * (q0 * gx + q2 * gz - q3 * gy)
    dq2 = 0.5 * (q0 * gy - q1 * gz + q3 * gx)
    dq3 = 0.5 * (q0 * gz + q1 * gy - q2 * gx)
    
    # Integrate to get new quaternion values
    q0 += dq0 * dt
    q1 += dq1 * dt
    q2 += dq2 * dt
    q3 += dq3 * dt
    
    # Normalize quaternion
    q0, q1, q2, q3 = normalize_vector((q0, q1, q2, q3))
    
    return q0, q1, q2, q3

def update_display():
    # Calculate tilt along the X and Y axes from the quaternion
    tilt_y = -100.0 * (q0 * q1 + q2 * q3)
    tilt_x = -100.0 * (q0 * q2 - q1 * q3)
    
    # Use tilt values to move the rectangle in response to tilt (normalize to screen)
    x_pos = int(screen_center_x + tilt_x * sensitivity)
    y_pos = int(screen_center_y - tilt_y * sensitivity)  # Invert Y-axis for correct direction

    # Ensure the rectangle stays within screen bounds
    x_pos = max(0, min(x_pos, 240 - rect.width))  # 240 is the screen width
    y_pos = max(0, min(y_pos, 240 - rect.height))  # 240 is the screen height
    
    # Update rectangle position
    rect.x = x_pos
    rect.y = y_pos

    # Print quaternion and position for debugging
    print(f"Quaternion: q0={q0:.4f}, q1={q1:.4f}, q2={q2:.4f}, q3={q3:.4f}")
    print(f"Updated position: x={x_pos}, y={y_pos}")

while True:
    # Read sensor data
    accel = clue.acceleration
    gyro = clue.gyro
    mag_data = clue.magnetic
    
    # Get time delta
    current_time = time.monotonic()
    dt = current_time - last_time
    last_time = current_time
    
    # Get raw values
    ax, ay, az = accel
    gx, gy, gz = gyro
    mx, my, mz = mag_data
    
    # Compute new quaternion values based on sensor data
    q0, q1, q2, q3 = quaternion_update(ax, ay, az, gx, gy, gz, mx, my, mz, dt)
    
    # Update display with bubble level behavior
    update_display()
    
    # Delay for stability
    time.sleep(0.05)
