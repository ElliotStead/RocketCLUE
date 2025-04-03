import board
import displayio
import digitalio
import time
import terminalio
from adafruit_bitmap_font import bitmap_font
from button import Button
from page import Page
from page_templates import Templates

display = board.DISPLAY
display.auto_refresh = True

# Load background image
bitmap = displayio.OnDiskBitmap(open("/tech.bmp", "rb"))  # Ensure file is on CIRCUITPY
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Create root display group
display_group = displayio.Group()
display_group.append(tile_grid)

# Initialize buttons
def print_something():
    print('Button pressed!')

palette = [0x4fccf5, 0x052142]
font = terminalio.FONT
# font = bitmap_font.load_font("/Junction-regular-24.bdf")
font = bitmap_font.load_font("/LeagueSpartan-Bold-16.pcf")
template = Templates(normal_color=palette[0], text_color=palette[1], font=font)

button1 = Button("Start", 14, 20, normal_color=palette[0], text_color=palette[1], font=font, border=10, callback=print_something)
button2 = Button("Settings", 14, 60, normal_color=palette[0], text_color=palette[1], font=font)
button3 = Button("Stop", 14, 100, normal_color=palette[0], text_color=palette[1], font=font)
button4 = Button("Info", 14, 20, normal_color=palette[0], text_color=palette[1], font=font)
button5 = Button("Back", 14, 60, normal_color=palette[0], text_color=palette[1], font=font)
button6 = Button("Back", 14, 20, normal_color=palette[0], text_color=palette[1], font=font)
button7 = Button("WOAH!", 5, 5, width=200, height=100, normal_color=palette[0], text_color=palette[1], font=font)
button8 = Button("YEA!!!", 5, 150, normal_color=palette[0], text_color=palette[1], font=font)

# Create pages
main_page = Page([button1, button2, button3], 'MAIN PAGE', normal_color=palette[0], text_color=palette[1], font=font)
info_page = Page([button4, button5], 'INFO PAGE', normal_color=palette[0], text_color=palette[1], font=font)
other_page = Page([button6])
last_page = Page([button7, button8])
page1 = template.two_button('PAGE 1', ['First', 'Second'], [print_something, print_something])

pages = [page1, main_page, info_page, other_page, last_page]
current_page_index = 0

# Add all pages to the display group but hide non-active ones
for page in pages:
    display_group.append(page.get_display_group())
    page.get_display_group().hidden = True  # Hide after adding

# Show the initial page
pages[current_page_index].get_display_group().hidden = False
display.root_group = display_group

# Initialize physical buttons
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

# Variables for tracking button B long press
button_b_press_start = 0
button_b_long_press_duration = 1.0  # 1 second hold time to change pages
button_b_is_pressed = False
button_b_prev_state = True  # True means not pressed (pulled up)
page_just_changed = False  # Flag to track if we just changed pages

while True:
    # Get the current selected button on the current page
    current_page = pages[current_page_index]
    current_button = None
    
    if current_page.buttons and len(current_page.buttons) > 0:
        if current_page.current_selection < len(current_page.buttons):
            current_button = current_page.buttons[current_page.current_selection]
    
    # Check button B state for visual feedback
    if button_b_prev_state and not button_b.value:  # Button B was just pressed
        button_b_press_start = time.monotonic()
        button_b_is_pressed = True
        page_just_changed = False
        # Set the visual state of the selected button to pressed
        if current_button:
            current_button.set_pressed(True)
            
    elif not button_b_prev_state and button_b.value:  # Button B was just released
        if button_b_is_pressed:
            # Reset the visual state of the selected button
            if current_button:
                #time.sleep(0.05)
                current_button.set_pressed(False)
                
            # Only trigger a button press callback if it was a short press and we didn't just change pages
            if time.monotonic() - button_b_press_start < button_b_long_press_duration and not page_just_changed:
                # Execute the callback on button release
                if current_button and current_button.callback:
                    current_button.callback()
                
            button_b_is_pressed = False
            page_just_changed = False  # Reset the page change flag on release
    
    # Check for long press while button is being held
    if not button_b.value and button_b_is_pressed:
        # Check if we've held the button long enough to change pages
        if time.monotonic() - button_b_press_start >= button_b_long_press_duration and not page_just_changed:
            # Reset the visual state of the current button
            if current_button:
                current_button.set_pressed(False)
                
            # Hide the current page
            pages[current_page_index].get_display_group().hidden = True
            # Move to the next page
            current_page_index = (current_page_index + 1) % len(pages)
            # Show the new page
            pages[current_page_index].get_display_group().hidden = False
            page_just_changed = True  # Set flag to prevent further actions until release
            #time.sleep(0.3)  # Prevent multiple page changes
    
    # Save current button B state for edge detection
    button_b_prev_state = button_b.value
    
    # Button A pressed -> navigate buttons
    if not button_a.value:
        pages[current_page_index].select_button(
            (pages[current_page_index].current_selection + 1) % len(pages[current_page_index].buttons)
        )
    
    # Update the display
    pages[current_page_index].draw()
    
    time.sleep(0.05)  # Small delay to reduce CPU usage
