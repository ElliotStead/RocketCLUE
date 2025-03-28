import displayio
import terminalio
from adafruit_display_text import label
import vectorio

class Button:
    def __init__(self, text, x, y, width=100, height=30, border=5, normal_color=0x444444, text_color=0xFF0000, callback=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False  # Highlight state
        self.pressed = False  # Pressed state
        self.border = border
        self.pressed_color_scale = 0.7
        self.highlighted_color_scale = 1.5
        self.callback = callback

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

        r = (normal_color >> 16) & 0xFF  # Extract red
        g = (normal_color >> 8) & 0xFF   # Extract green
        b = normal_color & 0xFF
        r = int(r * self.highlighted_color_scale)
        g = int(g * self.highlighted_color_scale)
        b = int(b * self.highlighted_color_scale)
        if(r > 255):
            r = 255
        if(g > 255):
            g = 255
        if(b > 255):
            b = 255
        self.highlight_normal_color = int(hex((r << 16) | (g << 8) | b))
        
        r = (text_color >> 16) & 0xFF  # Extract red
        g = (text_color >> 8) & 0xFF   # Extract green
        b = text_color & 0xFF
        r = int(r * self.highlighted_color_scale)
        g = int(g * self.highlighted_color_scale)
        b = int(b * self.highlighted_color_scale)
        if(r > 255):
            r = 255
        if(g > 255):
            g = 255
        if(b > 255):
            b = 255
        self.highlight_text_color = int(hex((r << 16) | (g << 8) | b))

        r = (self.highlight_normal_color >> 16) & 0xFF  # Extract red
        g = (self.highlight_normal_color >> 8) & 0xFF   # Extract green
        b = self.highlight_normal_color & 0xFF
        r = int(r * self.pressed_color_scale)
        g = int(g * self.pressed_color_scale)
        b = int(b * self.pressed_color_scale)
        self.pressed_normal_color = int(hex((r << 16) | (g << 8) | b))

        r = (text_color >> 16) & 0xFF  # Extract red
        g = (text_color >> 8) & 0xFF   # Extract green
        b = text_color & 0xFF
        r = int(r * self.pressed_color_scale)
        g = int(g * self.pressed_color_scale)
        b = int(b * self.pressed_color_scale)
        self.pressed_text_color = int(hex((r << 16) | (g << 8) | b))

        # Set initial color
        self.border_rect.pixel_shader[0] = self.text_color
        self.button_rect.pixel_shader[0] = self.normal_color

        # Create the text label
        self.label = label.Label(terminalio.FONT, text=self.text, color=self.text_color)

        self.label.anchor_point = (0.5, 0.5)
        self.label.anchored_position = (int(self.x + self.width/2),
        int(self.y + self.height/2))


    def set_pressed(self, state):
        self.pressed = state
        self.update_color()
        if self.pressed and self.callback:
            self.callback()

    def set_selected(self, state):
        self.selected = state
        self.update_color()

    def update_color(self):
        if self.pressed:
            self.border_rect.pixel_shader[0] = self.pressed_text_color
            self.button_rect.pixel_shader[0] = self.pressed_normal_color
            self.label.color = self.pressed_text_color  # Text color when pressed
        elif self.selected:
            self.border_rect.pixel_shader[0] = self.highlight_text_color
            self.button_rect.pixel_shader[0] = self.highlight_normal_color
            self.label.color = self.highlight_text_color  # Dark text when selected
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
