
import json
from tkinter import END, INSERT, Frame
from tkinter.scrolledtext import ScrolledText
from typing import List

from ui.models.message import Message


class OutputPanel(Frame):
    def __init__(self, master):
        super().__init__(master=master)

        self._output = ScrolledText(self, state='disabled', font='Roboto')
        self._output.pack(fill='both', expand=True)

    def clear(self):
        self._output.configure(state='normal')
        self._output.delete(1.0, END)
        self._output.configure(state='disabled')

    def __set_text(self, text):
        self._output.configure(state='normal')
        self._output.insert(INSERT, text)
        self._output.configure(state='disabled')

    def show_results(self, results: List[Message]):
        self.clear()
        # TODO: more user friendly than just pretty json
        json_serializable_results = list(x.to_json() for x in results)
        self.__set_text(json.dumps(json_serializable_results, ensure_ascii=False, indent=4))

