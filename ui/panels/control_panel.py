from tkinter import Button, Checkbutton, Entry, Frame, Label, IntVar

from livechat_scraper.messages.membership_gifted_message import MembershipGiftedMessage
from livechat_scraper.messages.superchat_message import SuperChatMessage


class ControlPanel(Frame):
    def __init__(self, master, engine, status_panel, output_panel):
        super().__init__(master=master)

        self._engine = engine
        self._status_panel = status_panel
        self._output_panel = output_panel

        self._message_types_selected = [
            ('Super chat message', SuperChatMessage, IntVar()),
            ('Membership gifted message', MembershipGiftedMessage, IntVar()),
        ]

        # first row
        video_url_entry_label = Label(self, text='Enter YouTube video URL:')
        video_url_entry_label.grid(row=0, column=0, padx=5, pady=5)
        self._video_url_entry = Entry(self) # TODO: the text box needs to be wider
        self._video_url_entry.grid(row=0, column=1, columnspan=len(self._message_types_selected), padx=5, pady=5)
        
        # second row
        m_types_selection_label = Label(self, text='What type of messages to fetch?')
        m_types_selection_label.grid(row=1, column=0, padx=5, pady=5)
        col_idx = 1
        for (m_type_name, _, variable) in self._message_types_selected:
            cb = Checkbutton(self, text=m_type_name, variable=variable, onvalue=1, offvalue=0)
            cb.grid(row=1, column=col_idx, padx=5, pady=5)
            col_idx += 1

        # third row
        start_scraping_btn = Button(self, text='Start', command=self.__start_scraping)
        start_scraping_btn.grid(row=2, column=0, sticky='e')
        
    def __start_scraping(self):
        video_url = self._video_url_entry.get()
        if video_url == '':
            self._status_panel.log_error('Please enter the video URL')
            return

        self._output_panel.clear()

        self._status_panel.log_info('Fetching messages...')
        m_type_whitelist = tuple(m_type for (_, m_type, variable) in self._message_types_selected if variable.get() == 1)
        # TODO: this blocks the UI while scraping is running
        self._engine.scrape(video_url, message_type_whitelist=m_type_whitelist)
        self._status_panel.log_info('Done fetching messages')

        self._output_panel.show_results(self._engine.get_scraped_messages())
        
