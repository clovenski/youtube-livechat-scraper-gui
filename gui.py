#!/usr/bin/env python3

"""Main script for the GUI"""

from tkinter import Tk

from livechat_scraper.scrapers import livechat_scraper
from ui.panels.control_panel import ControlPanel
from ui.panels.output_panel import OutputPanel
from ui.panels.status_panel import StatusPanel

# TODO: move below class to a services folder or something

class Engine:
    def __init__(self):
        self._scraped_messages = []

    def scrape(self, video_url, message_type_whitelist = None):
        scraper = livechat_scraper.LiveChatScraper(video_url)
        scraper.scrape()
        self._scraped_messages = scraper.output_messages(message_type_whitelist=message_type_whitelist)

    def get_scraped_messages(self):
        return self._scraped_messages.copy()


if __name__ == '__main__':
    root = Tk()
    root.title('YouTube Live Chat Scraper')

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    x_offset = int(root.winfo_screenwidth() / 3 - root_width / 3)
    y_offset = int(root.winfo_screenheight() / 3 - root_height / 3)
    root.geometry('500x500+{}+{}'.format(x_offset, y_offset))
    root.minsize(550,440)

    output_panel = OutputPanel(master=root)
    status_panel = StatusPanel(master=root)
    control_panel = ControlPanel(master=root, engine=Engine(), status_panel=status_panel, output_panel=output_panel)

    output_panel.pack(fill='y')
    control_panel.pack()
    status_panel.pack()

    root.mainloop()
