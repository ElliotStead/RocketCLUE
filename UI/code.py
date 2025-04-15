import board
import displayio
import digitalio
import time
import terminalio
from adafruit_bitmap_font import bitmap_font
from pages import PageManager

# Initialize the display with auto refresh disabled for better control
display = board.DISPLAY
display.auto_refresh = False  # Disable auto refresh for manual control

# Load background image
bitmap = displayio.OnDiskBitmap(open("/tech.bmp", "rb"))
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Create root display group
root_group = displayio.Group()
root_group.append(tile_grid)

# Set up styling
palette = [0x4fccf5, 0x052142]

# Use terminal font for better performance or load bitmap font
font = bitmap_font.load_font("/LeagueSpartan-Bold-16.pcf")

# Create the page manager
page_manager = PageManager(display, palette, font)

# Add the page manager's display group to the root group
root_group.append(page_manager.get_display_group())

# Set the root group as the display's root
display.root_group = root_group
display.refresh()  # Initial full refresh

# Initialize physical buttons
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

# Button state tracking variables
button_a_prev_state = True
button_a_was_pressed = False

button_b_press_start = 0
button_b_long_press_duration = 1.0  # 1 second hold time to change pages
button_b_is_pressed = False
button_b_prev_state = True  # True means not pressed (pulled up)
page_just_changed = False  # Flag to track if we just changed pages

# UI update tracking
last_ui_change = time.monotonic()
ui_needs_update = True  # Force initial update

# Main loop with optimized refreshes
while True:
    current_time = time.monotonic()
    current_page = page_manager.get_current_page()
    ui_changed = False
    refresh_needed = False

    # --- Button A: Next button handling ---
    button_a_current = button_a.value
    if button_a_prev_state and not button_a_current:  # Just pressed
        if current_page.next_button():
            ui_changed = True
            refresh_needed = True
    button_a_prev_state = button_a_current

    # --- Button B: Short/long press handling ---
    button_b_current = button_b.value
    if button_b_prev_state and not button_b_current:  # Just pressed
        button_b_press_start = current_time
        button_b_is_pressed = True
        page_just_changed = False
        if current_page.press_current_button():
            ui_changed = True
            refresh_needed = True
    elif not button_b_prev_state and button_b_current:  # Just released
        if button_b_is_pressed:
            if current_page.release_current_button():
                ui_changed = True
                refresh_needed = True
            # Short press -> trigger button action
            if current_time - button_b_press_start < button_b_long_press_duration and not page_just_changed:
                if current_page.trigger_current_button():
                    ui_changed = True
            button_b_is_pressed = False
            page_just_changed = False

    # Long press -> go back to the previous page
    if not button_b_current and button_b_is_pressed:
        if current_time - button_b_press_start >= button_b_long_press_duration and not page_just_changed:
            if page_manager.has_previous_pages():
                current_page.release_current_button()
                page_manager.go_back()
                page_just_changed = True
                ui_changed = True
                refresh_needed = True

    button_b_prev_state = button_b_current

    # Update UI and refresh display if needed
    if ui_changed:
        current_page.draw()
        if refresh_needed:
            display.refresh()
        last_ui_change = current_time
        ui_needs_update = False

    # Small delay to reduce CPU usage
    time.sleep(0.02)
