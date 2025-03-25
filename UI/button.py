import displayio
import terminalio
from adafruit_display_text import label
import vectorio

class Button:
    """A simple button class for the UI."""
    def __init__(self, text, x, y, width=100, height=30, border=1):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False  # Highlight state
        self.pressed = False  # Pressed state
        self.border = border

    def set_pressed(self, state):
        """Sets the pressed state of the button."""
        self.pressed = state

    def create_display_group(self):
        """Creates a display group containing the button rectangle and label."""
        group = displayio.Group()

        # Define colors
        normal_color = 0x444444  # Dark gray
        highlight_color = 0xFFFFFF  # White (selected)
        pressed_color = 0x222222  # Darker gray (pressed)
        border_color = 0xFF0000
        
        # Set colors based on state
        if self.pressed:
            button_color = pressed_color
            text_color = 0xFFFFFF
        elif self.selected:
            button_color = highlight_color
            text_color = 0x000000
        else:
            button_color = normal_color
            text_color = 0xFFFFFF

        # Create rectangle
        border_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=self.width,
            height=self.height,
            x=self.x,
            y=self.y
        )
        border_rect.pixel_shader[0] = border_color
        group.append(border_rect)
        
        button_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=self.width - (self.border * 2),
            height=self.height - (self.border * 2),
            x=self.x + self.border,
            y=self.y + self.border
        )
        button_rect.pixel_shader[0] = button_color
        group.append(button_rect)

        # Create text label
        text_area = label.Label(
            terminalio.FONT,
            text=self.text,
            color=text_color
        )
        text_area.anchor_point = (0.5, 0.5)
        text_area.anchored_position = (int(self.x + self.width/2), 
        int(self.y + self.height/2))
        
        group.append(text_area)

        return group
