import displayio
import vectorio
from adafruit_display_text import label
import terminalio
from adafruit_bitmap_font import bitmap_font

class Page:
    def __init__(self, buttons, title='', normal_color=0x444444, text_color=0xFF0000, height=50, border=10, font=terminalio.FONT):
        self.title = title
        self.buttons = buttons
        self.current_selection = 0
        self._previous_selection = 0
        self.height = height
        self.border = border
        self.font = font
        self.normal_color = normal_color
        self.text_color = text_color
        self.needs_full_redraw = True
        
        # Create the display group
        self.display_group = displayio.Group()
        
        # Create title elements if title is provided
        if self.title:
            # Border rect
            border_bitmap = displayio.Bitmap(240, self.height, 1)
            border_palette = displayio.Palette(1)
            border_palette[0] = self.text_color
            
            for x in range(240):
                for y in range(self.height):
                    border_bitmap[x, y] = 0
                    
            self.border_grid = displayio.TileGrid(
                border_bitmap, 
                pixel_shader=border_palette,
                x=0, y=240-self.height
            )
            
            # Inner rect
            inner_bitmap = displayio.Bitmap(240-self.border, self.height-self.border, 1)
            inner_palette = displayio.Palette(1)
            inner_palette[0] = self.normal_color
            
            for x in range(240-self.border):
                for y in range(self.height-self.border):
                    inner_bitmap[x, y] = 0
                    
            self.inner_grid = displayio.TileGrid(
                inner_bitmap, 
                pixel_shader=inner_palette,
                x=self.border//2, y=240-self.height+self.border//2
            )
            
            # Title label
            self.title_label = label.Label(
                self.font, 
                text=self.title, 
                color=self.text_color,
                anchor_point=(0.5, 0.5),
                anchored_position=(120, 240-self.height//2)
            )
            
            self.display_group.append(self.border_grid)
            self.display_group.append(self.inner_grid)
            self.display_group.append(self.title_label)
        
        # Add all buttons to the display group
        for button in self.buttons:
            self.display_group.append(button.create_display_group())

    def draw(self):
        """Updates button selection states"""
        if self.needs_full_redraw:
            # First time drawing - set all button states
            for i, button in enumerate(self.buttons):
                button.set_selected(i == self.current_selection)
            self.needs_full_redraw = False
        else:
            # Only update buttons that changed
            if self._previous_selection != self.current_selection:
                # Deselect previous button if valid
                if 0 <= self._previous_selection < len(self.buttons):
                    self.buttons[self._previous_selection].set_selected(False)
                
                # Select current button if valid
                if 0 <= self.current_selection < len(self.buttons):
                    self.buttons[self.current_selection].set_selected(True)
            
        # Update previous selection
        self._previous_selection = self.current_selection

    # Rest of the methods remain the same as in your original class...
    def select_button(self, index):
        """Select a button by index."""
        if 0 <= index < len(self.buttons):
            self._previous_selection = self.current_selection
            self.current_selection = index
            return True
        return False

    def next_button(self):
        """Move to the next button. Returns True if selection changed."""
        if self.buttons and len(self.buttons) > 0:
            next_selection = (self.current_selection + 1) % len(self.buttons)
            return self.select_button(next_selection)
        return False

    def get_current_button(self):
        """Returns the currently selected button or None if no buttons."""
        if self.buttons and 0 <= self.current_selection < len(self.buttons):
            return self.buttons[self.current_selection]
        return None

    def press_current_button(self):
        """Set the visual state of current button to pressed. Returns True if visual state changed."""
        current_button = self.get_current_button()
        if current_button:
            return current_button.set_pressed(True)
        return False

    def release_current_button(self):
        """Set the visual state of current button to released. Returns True if visual state changed."""
        current_button = self.get_current_button()
        if current_button:
            return current_button.set_pressed(False)
        return False

    def trigger_current_button(self):
        """Execute the callback of the currently selected button if it exists."""
        current_button = self.get_current_button()
        if current_button and current_button.callback:
            current_button.callback()
            return True
        return False

    def get_display_group(self):
        """Returns the display group containing all button display groups."""
        return self.display_group

    def get_title(self):
        return self.title

    def force_redraw(self):
        """Forces a complete redraw of all buttons on next draw() call."""
        self.needs_full_redraw = True
