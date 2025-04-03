import time
import displayio
import vectorio
from adafruit_display_text import label
import terminalio
from adafruit_bitmap_font import bitmap_font

class Page:
    def __init__(self, buttons, title='', normal_color=0x444444, text_color=0xFF0000, height=50, border=10, font=terminalio.FONT):
        self.title = title  # Name of the page for debugging or navigation
        self.buttons = buttons
        self.current_selection = 0  # Index of the currently selected button
        self.height = height
        self.border = border
        self.font = font

        # Create a display group containing all button display groups
        self.display_group = displayio.Group()

        if(self.title != ''):
            self.border_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=240,
            height=self.height,
            x=0,
            y=0,
            )
            self.title_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=240 - self.border,
            height=self.height - self.border,
            x=int(self.border/2),
            y=int(self.border/2),
            )

            self.normal_color = normal_color
            self.text_color = text_color

            self.border_rect.pixel_shader[0] = self.text_color
            self.title_rect.pixel_shader[0] = self.normal_color

            self.label = label.Label(self.font, text=self.title, color=self.text_color)

            self.label.anchor_point = (0.5, 0.5)
            self.label.anchored_position = (120,
            int(self.height/2))

            self.display_group.append(self.border_rect)
            self.display_group.append(self.title_rect)
            self.display_group.append(self.label)

        for button in self.buttons:
            self.display_group.append(button.create_display_group())

    def draw(self):
        """Updates button colors and selections."""
        for i, button in enumerate(self.buttons):
            button.set_selected(i == self.current_selection)  # Highlight selected button

    def select_button(self, index):
        """Select a button by index."""
        if 0 <= index < len(self.buttons):
            self.current_selection = index
            self.draw()

    def handle_button_press(self):
        """Handles button press on the selected button."""
        if self.buttons:
            selected_button = self.buttons[self.current_selection]
            selected_button.set_pressed(True)

            time.sleep(0.2)  # Debounce delay
            selected_button.set_pressed(False)

    def get_display_group(self):
        """Returns the display group containing all button display groups."""
        return self.display_group
