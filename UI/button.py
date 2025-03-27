import displayio
import terminalio
from adafruit_display_text import label
import vectorio

class Button:
    def __init__(self, text, x, y, width=100, height=30, border=5, normal_color=0x444444, text_color=0xFF0000, pressed_normal_color=0x222222, pressed_text_color=0xFFF000, highlight_color=0xFFFFFF):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False  # Highlight state
        self.pressed = False  # Pressed state
        self.border = border

        self.border_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=self.width,
            height=self.height,
            x=self.x,
            y=self.y,
        )
        self.button_rect = vectorio.Rectangle(
            pixel_shader=displayio.Palette(1),
            width=self.width-self.border,
            height=self.height-self.border,
            x=int(self.x+self.border/2),
            y=int(self.y+self.border/2),
        )

        # Set default colors
        self.normal_color = normal_color
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.pressed_normal_color = pressed_normal_color
        self.pressed_text_color = pressed_text_color
        
        # Set initial color
        self.border_rect.pixel_shader[0] = self.text_color
        self.button_rect.pixel_shader[0] = self.normal_color

        # Create the text label
        self.label = label.Label(terminalio.FONT, text=self.text, color=self.text_color)
        self.label.x = self.x + 10
        self.label.y = self.y + 10
        '''
        text_area.anchor_point = (0.5, 0.5)
        text_area.anchored_position = (int(self.x + self.width/2), 
        int(self.y + self.height/2))
        '''

    def set_pressed(self, state):
        self.pressed = state
        self.update_color()

    def set_selected(self, state):
        self.selected = state
        self.update_color()

    def update_color(self):
        if self.pressed:
            self.border_rect.pixel_shader[0] = self.pressed_text_color
            self.button_rect.pixel_shader[0] = self.pressed_normal_color
            self.label.color = self.pressed_text_color  # Text color when pressed
        elif self.selected:
            self.border_rect.pixel_shader[0] = self.text_color
            self.button_rect.pixel_shader[0] = self.highlight_color
            self.label.color = self.text_color  # Dark text when selected
        else:
            self.border_rect.pixel_shader[0] = self.text_color
            self.button_rect.pixel_shader[0] = self.normal_color
            self.label.color = self.text_color  # Normal white text

    def create_display_group(self):
        group = displayio.Group()
        group.append(self.border_rect)
        group.append(self.button_rect)
        group.append(self.label)
        return group
