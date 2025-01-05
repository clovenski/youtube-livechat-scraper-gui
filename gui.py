#!/usr/bin/env python3

"""Main script for the GUI"""

from tkinter import Tk

from livechat_scraper.constants.scraper_constants import MESSAGE_TYPE_MEMBERSHIP_GIFT, MESSAGE_TYPE_SUPER_CHAT
from livechat_scraper.scrapers import livechat_scraper
from ui.models.message import Message
from ui.panels.control_panel import ControlPanel
from ui.panels.output_panel import OutputPanel
from ui.panels.status_panel import StatusPanel

# TODO: move below classes to a services folder or something

class Engine:
    def __init__(self):
        self._scraper = None
        self.scraped_video = False

    def initialize_scraper(self, video_url, on_progress_update=None):
        self._scraper = livechat_scraper.LiveChatScraper(video_url, on_progress_update=on_progress_update)
        self.scraped_video = False

    def scrape(self):
        if self._scraper is None:
            raise Exception('scraper not initialized')
        self._scraper.scrape()
        self.scraped_video = True

    def get_scraped_messages(self, message_type_whitelist = None):
        return self._scraper.output_messages(message_type_whitelist=message_type_whitelist).copy()

class MessageMapper:
    def map(self, message) -> Message:
        # common props
        m_type = message['message_type']
        timestamp = '' if message['occurence_timestamp'] is None else message['occurence_timestamp']
        user = message['author']

        # specific props
        amount = ''
        message_text = ''
        if m_type == MESSAGE_TYPE_SUPER_CHAT:
            m_type = 'Superchat'
            amount_txt = message['content']['purchaseAmount']['simpleText'],
            amount = amount_txt[0] # for some reason simpleText value is a tuple
            message_text = message['content']['message']
        if m_type == MESSAGE_TYPE_MEMBERSHIP_GIFT:
            m_type = 'Gifted members'
            gift_text = message['content']['giftText']
            amount = gift_text.split(sep=None, maxsplit=3)[1] # expecting format of message to be "Gifted N {streamer_name} memberships"
            message_text = gift_text
        
        return Message(
                timestamp=timestamp,
                type=m_type,
                user=user,
                amount=amount,
                message=message_text
            )


if __name__ == '__main__':
    root = Tk()
    root.title('YouTube Live Chat Scraper')

    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    x_offset = int(root.winfo_screenwidth() / 3 - root_width / 3)
    y_offset = int(root.winfo_screenheight() / 3 - root_height / 3)
    root.geometry('500x500+{}+{}'.format(x_offset, y_offset))
    root.minsize(800,550)

    output_panel = OutputPanel(master=root)
    status_panel = StatusPanel(master=root)
    control_panel = ControlPanel(master=root, engine=Engine(), msg_mapper=MessageMapper(), status_panel=status_panel, output_panel=output_panel)

    output_panel.pack(fill='both', expand=True)
    control_panel.pack(pady=3)
    status_panel.pack()

    root.mainloop()
