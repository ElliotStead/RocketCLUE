import displayio
import vectorio
from adafruit_display_text import label

class Button:
    def __init__(self, text, x, y, width=50, height=100, callback=None,
                 normal_color=0x444444, text_color=0xFFFFFF,
                 border=10, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.border = border
        self.font = font
        
        # Store colors directly
        self.normal_color = normal_color
        self.text_color = text_color
        self.selected_color = self._scale_color(normal_color, 1.5)
        self.pressed_color = self._scale_color(normal_color, 0.7)
        
        self.is_selected = False
        self.is_pressed = False
        self.display_group = None
        
    def _scale_color(self, color, scale):
        r = min(255, int(((color >> 16) & 0xFF) * scale))
        g = min(255, int(((color >> 8) & 0xFF) * scale))
        b = min(255, int((color & 0xFF) * scale))
        return (r << 16) | (g << 8) | b
        
    def create_display_group(self):
        if self.display_group is not None:
            return self.display_group
            
        self.display_group = displayio.Group(x=self.x, y=self.y)
        
        # Create a single bitmap for the button background
        bg_bitmap = displayio.Bitmap(self.width, self.height, 3)
        bg_palette = displayio.Palette(3)
        
        # Set palette colors
        bg_palette[0] = self.normal_color     # Inner fill
        bg_palette[1] = self.text_color       # Border
        bg_palette[2] = 0x000000              # Transparent (unused)
        
        # Fill the bitmap
        for x in range(self.width):
            for y in range(self.height):
                # Simple border without dithering
                if (x < self.border//2 or x >= self.width - self.border//2 or 
                    y < self.border//2 or y >= self.height - self.border//2):
                    bg_bitmap[x, y] = 1  # Border
                else:
                    bg_bitmap[x, y] = 0  # Inner area
        
        # Create the tilegrid from the bitmap
        self.bg_grid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.bg_palette = bg_palette  # Store reference to palette
        self.display_group.append(self.bg_grid)
        
        # Create the text label
        self.label = label.Label(
            self.font,
            text=self.text,
            color=self.text_color,
            anchor_point=(0.5, 0.5),
            anchored_position=(self.width // 2, self.height // 2)
        )
        self.display_group.append(self.label)
        
        return self.display_group
        
    def set_selected(self, selected):
        if self.is_selected != selected:
            self.is_selected = selected
            self._update_appearance()
            return True
        return False
        
    def set_pressed(self, pressed):
        if self.is_pressed != pressed:
            self.is_pressed = pressed
            self._update_appearance()
            return True
        return False
        
    def _update_appearance(self):
        if not hasattr(self, 'bg_palette'):
            return  # Display group hasn't been created yet
            
        # Update colors based on state
        if self.is_pressed:
            self.bg_palette[0] = self.pressed_color
        elif self.is_selected:
            self.bg_palette[0] = self.selected_color
        else:
            self.bg_palette[0] = self.normal_colorimport displayio
import vectorio
from adafruit_display_text import label

class Button:
    def __init__(self, text, x, y, width=50, height=100, callback=None,
                 normal_color=0x444444, text_color=0xFFFFFF,
                 border=10, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.border = border
        self.font = font
        
        # Store colors directly
        self.normal_color = normal_color
        self.text_color = text_color
        self.selected_color = self._scale_color(normal_color, 1.5)
        self.pressed_color = self._scale_color(normal_color, 0.7)
        
        self.is_selected = False
        self.is_pressed = False
        self.display_group = None
        
    def _scale_color(self, color, scale):
        r = min(255, int(((color >> 16) & 0xFF) * scale))
        g = min(255, int(((color >> 8) & 0xFF) * scale))
        b = min(255, int((color & 0xFF) * scale))
        return (r << 16) | (g << 8) | b
        
    def create_display_group(self):
        if self.display_group is not None:
            return self.display_group
            
        self.display_group = displayio.Group(x=self.x, y=self.y)
        
        # Create a single bitmap for the button background
        bg_bitmap = displayio.Bitmap(self.width, self.height, 3)
        bg_palette = displayio.Palette(3)
        
        # Set palette colors
        bg_palette[0] = self.normal_color     # Inner fill
        bg_palette[1] = self.text_color       # Border
        bg_palette[2] = 0x000000              # Transparent (unused)
        
        # Fill the bitmap
        for x in range(self.width):
            for y in range(self.height):
                # Simple border without dithering
                if (x < self.border//2 or x >= self.width - self.border//2 or 
                    y < self.border//2 or y >= self.height - self.border//2):
                    bg_bitmap[x, y] = 1  # Border
                else:
                    bg_bitmap[x, y] = 0  # Inner area
        
        # Create the tilegrid from the bitmap
        self.bg_grid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.bg_palette = bg_palette  # Store reference to palette
        self.display_group.append(self.bg_grid)
        
        # Create the text label
        self.label = label.Label(
            self.font,
            text=self.text,
            color=self.text_color,
            anchor_point=(0.5, 0.5),
            anchored_position=(self.width // 2, self.height // 2)
        )
        self.display_group.append(self.label)
        
        return self.display_group
        
    def set_selected(self, selected):
        if self.is_selected != selected:
            self.is_selected = selected
            self._update_appearance()
            return True
        return False
        
    def set_pressed(self, pressed):
        if self.is_pressed != pressed:
            self.is_pressed = pressed
            self._update_appearance()
            return True
        return False
        
    def _update_appearance(self):
        if not hasattr(self, 'bg_palette'):
            return  # Display group hasn't been created yet
            
        # Update colors based on state
        if self.is_pressed:
            self.bg_palette[0] = self.pressed_color
        elif self.is_selected:
            self.bg_palette[0] = self.selected_color
        else:
            self.bg_palette[0] = self.normal_color
