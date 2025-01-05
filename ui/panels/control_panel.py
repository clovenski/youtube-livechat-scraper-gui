import csv
import threading
from tkinter import Button, Checkbutton, Entry, Frame, Label, IntVar, messagebox
from tkinter.filedialog import asksaveasfilename

from livechat_scraper.messages.membership_gifted_message import MembershipGiftedMessage
from livechat_scraper.messages.superchat_message import SuperChatMessage


class ControlPanel(Frame):
    def __init__(self, master, engine, msg_mapper, status_panel, output_panel):
        super().__init__(master=master)

        self._engine = engine
        self._msg_mapper = msg_mapper
        self._status_panel = status_panel
        self._output_panel = output_panel

        self._message_types_selected = [
            ('Super chat messages', SuperChatMessage, IntVar()),
            ('Membership gifted messages', MembershipGiftedMessage, IntVar()),
            # other message types can be added below
        ]

        # first row
        video_url_entry_label = Label(self, text='Enter YouTube video URL:')
        video_url_entry_label.grid(row=0, column=0, padx=2, pady=2)
        self._video_url_entry = Entry(self, width=50)
        self._video_url_entry.grid(row=0, column=1, padx=2, pady=2)
        self._start_scraping_btn = Button(self, text='Scrape', command=self.__on_start_scrape_btn_click)
        self._start_scraping_btn.grid(row=0, column=2, padx=2, pady=2)
        
        # second row
        m_types_selection_label = Label(self, text='What type of messages to display?')
        m_types_selection_label.grid(row=1, column=0, padx=2, pady=2)
        m_types_checkbuttons_group = Frame(self)
        cb_row = cb_col = 0
        cb_max_cols = 2
        for (m_type_name, _, variable) in self._message_types_selected:
            cb = Checkbutton(m_types_checkbuttons_group, text=m_type_name, variable=variable, onvalue=1, offvalue=0)
            cb.grid(row=cb_row, column=cb_col, padx=2, pady=2)
            cb_col += 1
            if cb_col == cb_max_cols:
                cb_row += 1
                cb_col = 0
        m_types_checkbuttons_group.grid(row=1, column=1, padx=2, pady=2)

        self._display_messages_btn = Button(self, text='Display', command=self.__on_display_messages_btn_click, state='disabled')
        self._display_messages_btn.grid(row=1, column=2, padx=2, pady=2)

        # third row
        self._save_to_csv_btn = Button(self, text='Save to CSV', command=self.__on_save_to_csv_btn_click, state='disabled')
        self._save_to_csv_btn.grid(row=2, column=2, padx=2, pady=2)
        
    def __on_start_scrape_btn_click(self):
        video_url = self._video_url_entry.get()
        if video_url == '':
            self._status_panel.log_error('Please enter the video URL')
            return
        if self._engine.scraped_video and not messagebox.askokcancel('Confirm', 'Are you sure you want to scrape a new video?\nThe previous video would need to be scraped again.'):
            return

        self._engine.initialize_scraper(video_url=video_url, on_progress_update=lambda progress_str: self._status_panel.log_info(progress_str, clear_after_secs=None))
        # use separate thread to not block UI
        thread = threading.Thread(target=self.__start_scraping)
        thread.daemon = True
        thread.start()

    def __start_scraping(self):
        self._status_panel.log_info('Scraping...', clear_after_secs=None)
        self._start_scraping_btn.configure(state='disabled')
        self._display_messages_btn.configure(state='disabled')
        self._save_to_csv_btn.configure(state='disabled')
        self._engine.scrape()
        self._status_panel.log_info('Done scraping video', clear_after_secs=None)
        self._start_scraping_btn.configure(state='normal')
        self._display_messages_btn.configure(state='normal')

    def __on_display_messages_btn_click(self):
        m_type_whitelist = tuple(m_type for (_, m_type, variable) in self._message_types_selected if variable.get() == 1)

        if m_type_whitelist == ():
            self._status_panel.log_error('Please select at least one message type')
            return

        self._output_panel.show_results(
            list(self._msg_mapper.map(result) for result in self._engine.get_scraped_messages(message_type_whitelist=m_type_whitelist))
        )

        self._save_to_csv_btn.configure(state='normal')

    def __on_save_to_csv_btn_click(self):
        filename = asksaveasfilename(filetypes=[('CSV', '*.csv'), ('All Files', '*.*')], defaultextension='csv')
        if filename == '':
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as out_file:
            csvwriter = csv.writer(out_file, delimiter=',')
            for line in self._output_panel.get_output_as_csv():
                csvwriter.writerow(line)

        self._status_panel.log_info(f'Done saving results to a CSV file')
