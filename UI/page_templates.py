import terminalio
from button import Button
from page import Page

class Templates:
    def __init__(self, normal_color=0x444444, text_color=0xFF0000, border=10, font=terminalio.FONT):
        self.normal_color = normal_color
        self.text_color = text_color
        self.border = border
        self.font = font

    def two_button(self, title, button_texts, callbacks):
        button1 = Button(button_texts[0], 20, 60, 200, 50, normal_color=self.normal_color, text_color=self.text_color, font=self.font, callback=callbacks[0])
        button2 = Button(button_texts[1], 20, 120, 200, 50, normal_color=self.normal_color, text_color=self.text_color, font=self.font, callback=callbacks[1])

        page = Page([button1, button2], title, self.normal_color, self.text_color, font=self.font)

        return page

    def contents(self, title, pages, switch_page):
        button1 = Button(pages[0].get_title(), 20, 10, 200, 50, normal_color=self.normal_color, text_color=self.text_color, font=self.font, callback=lambda: switch_page(pages[0]))
        button2 = Button(pages[1].get_title(), 20, 70, 200, 50, normal_color=self.normal_color, text_color=self.text_color, font=self.font, callback=lambda: switch_page(pages[1]))
        button3 = Button(pages[2].get_title(), 20, 130, 200, 50, normal_color=self.normal_color, text_color=self.text_color, font=self.font, callback=lambda: switch_page(pages[2]))

        page = Page([button1, button2, button3], title, self.normal_color, self.text_color, font=self.font)

        return page
