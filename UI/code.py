import board
import displayio
import digitalio
from button import Button  # Import the Button class
import time

# Use built-in display
display = board.DISPLAY

# Buttons
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

# Create button instances
buttons = [
    Button("Start", 14, 20),
    Button("Settings", 14, 60)
]

# UI State
current_selection = 0  # Index of the currently selected button

def draw_ui():
    """Updates the display with the buttons."""
    display_group = displayio.Group()

    for i, button in enumerate(buttons):
        button.selected = (i == current_selection)  # Highlight selected button
        display_group.append(button.create_display_group())

    display.root_group = display_group

# Show initial UI
draw_ui()

while True:
    if not button_a.value:  # Button A pressed (navigate)
        current_selection = (current_selection + 1) % len(buttons)
        draw_ui()
        while not button_a.value:  # Wait for release
            pass
        time.sleep(0.1)

    if not button_b.value:  # Button B pressed (select)
        buttons[current_selection].set_pressed(True)  # Show pressed effect
        draw_ui()
        while not button_b.value:  # Wait for release
            pass
        time.sleep(0.1)
        buttons[current_selection].set_pressed(False)  # Reset after release
        draw_ui()
        print(f"Selected: {buttons[current_selection].text}")
