import board
import displayio
import digitalio
from button import Button  # Import the Button class
from page import Page
import time

display = board.DISPLAY
display.auto_refresh = True

bitmap = displayio.OnDiskBitmap(open("/background.bmp", "rb"))  # Ensure file is on CIRCUITPY
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

display_group = displayio.Group()
display_group.append(tile_grid)

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

# Define the callback function
def print_something():
    print('Button pressed!')

# Create buttons
button1 = Button("Start", 14, 20, normal_color=0xfa3eac, text_color=0x57fa3e, callback=print_something)
button2 = Button("Settings", 14, 60, normal_color=0x5590ED)
button3 = Button("Stop", 14, 100, normal_color=0x5590ED)

# Add buttons to a page (example page handling)
main_page = Page("Main Menu", [button1, button2, button3])
print('here')
# The main loop where button interaction happens

display_group.append(button1.create_display_group())
display_group.append(button2.create_display_group())
display_group.append(button3.create_display_group())

display.root_group = display_group

while True:
    main_page.draw()  # Update button selection and colors

    if not button_a.value:  # Button A pressed (navigate)
        main_page.select_button((main_page.current_selection + 1) % len(main_page.buttons))
        time.sleep(0.1)  # Short delay to avoid bouncing

    if not button_b.value:  # Button B pressed (select)
        main_page.handle_button_press()  # Call the selected button's callback
        time.sleep(0.1)  # Short delay to avoid bouncing

    time.sleep(0.05)  # Small delay to reduce CPU usage
