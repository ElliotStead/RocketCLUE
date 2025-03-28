import board
import displayio
import digitalio
from button import Button
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

# Create buttons for each page
button1 = Button("Start", 14, 20, normal_color=0x5590ED, callback=print_something)
button2 = Button("Settings", 14, 60, normal_color=0x5590ED)
button3 = Button("Stop", 14, 100, normal_color=0x5590ED)

button4 = Button("Info", 14, 20, normal_color=0x5590ED)
button5 = Button("Back", 14, 60, normal_color=0x5590ED)

button6 = Button("Back", 14, 20, normal_color=0x5590ED)

# Create pages
main_page = Page("Main Menu", [button1, button2, button3])
info_page = Page("Info", [button4, button5])
other_page = Page("stuff", [button6])


pages = [main_page, info_page, other_page]
current_page_index = 0

display.root_group = display_group
display.root_group.append(pages[current_page_index].get_display_group())

while True:
    pages[current_page_index].draw()  # Update button selection and colors

    if not button_a.value and not button_b.value:  # Both buttons pressed -> switch page
        while (len(display.root_group) > 1):
            display.root_group.pop()
        current_page_index = (current_page_index + 1) % len(pages)
        display.root_group.append(pages[current_page_index].get_display_group())
        for i in display.root_group:
            print(i)



    elif not button_a.value:  # Button A pressed -> navigate buttons
        pages[current_page_index].select_button(
            (pages[current_page_index].current_selection + 1) % len(pages[current_page_index].buttons)
        )
        time.sleep(0.1)  # Prevent bouncing

    elif not button_b.value:  # Button B pressed -> select button
        pages[current_page_index].handle_button_press()
        time.sleep(0.1)  # Prevent bouncing

    time.sleep(0.05)  # Small delay to reduce CPU usage
