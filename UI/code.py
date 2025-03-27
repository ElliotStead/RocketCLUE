import board
import displayio
import digitalio
import time
from button import Button  # Import the Button class

# Use built-in display
display = board.DISPLAY
display.auto_refresh = True  # Let display handle updates automatically

# Load bitmap background
bitmap = displayio.OnDiskBitmap(open("/background.bmp", "rb"))  # Ensure file is on CIRCUITPY
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Buttons on the Clue
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

# Create UI buttons
buttons = [
    Button("Start", 14, 20),
    Button("Settings", 14, 60)
]

# UI State
current_selection = 0  # Index of the currently selected button

# Create display group
display_group = displayio.Group()

# Add the background bitmap once (never redraw it)
display_group.append(tile_grid)

# Add buttons to the display group
for button in buttons:
    display_group.append(button.create_display_group())

# Show everything on screen
display.root_group = display_group

# Function to update UI **without refreshing the whole screen**
def draw_ui():
    """Only updates button colors without redrawing the whole screen."""
    for i, button in enumerate(buttons):
        button.set_selected(i == current_selection)  # Highlight selected button
        button.update_color()  # Change only colors (no full refresh)

# Show initial UI
draw_ui()

# Main loop
while True:
    if not button_a.value:  # Button A pressed (navigate)
        current_selection = (current_selection + 1) % len(buttons)
        draw_ui()
        while not button_a.value:  # Wait for release
            pass  

    if not button_b.value:  # Button B pressed (select)
        buttons[current_selection].set_pressed(True)  # Show pressed effect
        draw_ui()
        time.sleep(0.2)  # Short delay (200ms)
        buttons[current_selection].set_pressed(False)  # Reset after delay
        draw_ui()
        print(f"Selected: {buttons[current_selection].text}")

        while not button_b.value:  # Wait for release
            pass
