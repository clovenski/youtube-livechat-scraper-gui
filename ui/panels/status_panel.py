
import threading
from tkinter import Frame, Label


class StatusPanel(Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self._status_label = Label(self)
        self._status_label.grid(row=0, column=0, sticky='w')

        self._clear_timer = None

    def __clear_label(self):
        self._status_label.config(text='')

    def __schedule_label_clear(self, after_secs):
        secs = after_secs if after_secs > 0 else 5
        if self._clear_timer is not None:
            self._clear_timer.cancel()
        self._clear_timer = threading.Timer(secs, self.__clear_label)
        self._clear_timer.start()

    def log_info(self, msg, clear_after_secs=5):
        self._status_label.config(text=msg, fg='black')
        self.__schedule_label_clear(clear_after_secs)

    def log_error(self, msg, clear_after_secs=5):
        self._status_label.config(text=msg, fg='red')
        self.__schedule_label_clear(clear_after_secs)
