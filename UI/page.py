import time
import displayio

class Page:
    def __init__(self, title, buttons):
        self.title = title  # The name of the page (can be used for debugging or navigation)
        self.buttons = buttons
        self.current_selection = 0  # Index of the currently selected button
        
        # Create a display group containing all button display groups
        self.display_group = displayio.Group()
        for button in self.buttons:
            self.display_group.append(button.create_display_group())

    def draw(self):
        """Draws the current state of the page, updating button colors and selections."""
        for i, button in enumerate(self.buttons):
            button.set_selected(i == self.current_selection)  # Highlight selected button
            button.update_color()  # Update button color states

    def select_button(self, index):
        """Select a specific button by index."""
        if 0 <= index < len(self.buttons):
            self.current_selection = index
            self.draw()

    def handle_button_press(self):
        """Handle a button press event on the current selection."""
        if self.buttons:
            self.buttons[self.current_selection].set_pressed(True)
            self.buttons[self.current_selection].update_color()
            if self.buttons[self.current_selection].callback:
                self.buttons[self.current_selection].callback()
            time.sleep(0.2)  # Debounce delay
            self.buttons[self.current_selection].set_pressed(False)
            self.buttons[self.current_selection].update_color()
    
    def get_display_group(self):
        """Return the display group containing all button display groups."""
        return self.display_group
