import time
import displayio
from button import Button
from page import Page
from page_templates import Templates

# Fade functions using display.brightness
def fade_out_display(display, steps=50, delay=0.01):
    for i in range(steps, -1, -1):
        display.brightness = i / steps
        time.sleep(delay)

def fade_in_display(display, steps=25, delay=0.01):
    for i in range(steps + 1):
        display.brightness = i / steps
        time.sleep(delay)

class PageManager:
    def __init__(self, display, palette, font):
        self.display = display
        self.palette = palette
        self.font = font
        self.template = Templates(normal_color=palette[0], text_color=palette[1], font=font)

        self.pages = []
        self.current_page_index = 0
        self.previous_pages = []

        self.display_group = displayio.Group()
        self._create_pages()

        self.pages[self.current_page_index].get_display_group().hidden = False
        self.pages[self.current_page_index].force_redraw()
        self.pages[self.current_page_index].draw()

    def _create_pages(self):
        button5 = Button("Back", 14, 60, width=200, height=100, normal_color=self.palette[0],
                         text_color=self.palette[1], font=self.font, callback=self.go_back)
        button6 = Button("Back", 14, 20, width=200, height=100, normal_color=self.palette[0],
                         text_color=self.palette[1], font=self.font, callback=self.go_back)
        button7 = Button("WOAH!", 5, 5, width=200, height=100, normal_color=self.palette[0],
                         text_color=self.palette[1], font=self.font, callback=lambda: None)
        button8 = Button("YEA!!!", 5, 150, normal_color=self.palette[0],
                         text_color=self.palette[1], font=self.font, callback=lambda: None)

        page1 = self.template.two_button('PAGE 1', ['First', 'Second'],
                                         [lambda: None, self.print_something])
        last_page = Page([button7, button8], 'LAST PAGE',
                         normal_color=self.palette[0], text_color=self.palette[1], font=self.font)
        temp_page = Page([button5, button6], 'PAGE 2',
                         normal_color=self.palette[0], text_color=self.palette[1], font=self.font)
        home_page = self.template.contents('HOME', [page1, last_page, temp_page], self.switch_page)

        self.pages = [home_page, page1, temp_page, last_page]

        for i, page in enumerate(self.pages):
            if i == 0:
                self.display_group.append(page.get_display_group())
                page.get_display_group().hidden = False
            else:
                page.get_display_group().hidden = True

    def print_something(self):
        print('Button pressed!')

    def switch_page(self, target_page):
        self.display.auto_refresh = False
        fade_out_display(self.display)

        current_page = self.pages[self.current_page_index]
        if current_page != target_page:
            self.previous_pages.append(current_page)
            if target_page == self.pages[0]:
                self.previous_pages.clear()

            current_page.get_display_group().hidden = True
            new_index = self.pages.index(target_page)

            if target_page.get_display_group() not in self.display_group:
                self.display_group.append(target_page.get_display_group())

            target_page.get_display_group().hidden = False
            target_page.force_redraw()
            self.current_page_index = new_index
            target_page.draw()

        self.display.refresh()
        fade_in_display(self.display)

    def go_back(self):
        if self.previous_pages:
            self.display.auto_refresh = False
            fade_out_display(self.display)

            current_page = self.pages[self.current_page_index]
            current_page.get_display_group().hidden = True
            previous_page = self.previous_pages.pop()

            if previous_page.get_display_group() not in self.display_group:
                self.display_group.append(previous_page.get_display_group())

            self.current_page_index = self.pages.index(previous_page)
            previous_page.get_display_group().hidden = False
            previous_page.force_redraw()
            previous_page.draw()

            self.display.refresh()
            fade_in_display(self.display)

    def get_display_group(self):
        return self.display_group

    def get_current_page(self):
        return self.pages[self.current_page_index]

    def has_previous_pages(self):
        return len(self.previous_pages) > 0
