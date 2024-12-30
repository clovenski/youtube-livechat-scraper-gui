
import json
from tkinter import END, INSERT, Frame
from tkinter.scrolledtext import ScrolledText


class OutputPanel(Frame):
    def __init__(self, master):
        super().__init__(master=master)

        self._output = ScrolledText(self, state='disabled')
        self._output.pack(fill='x')

    def clear(self):
        self._output.delete(1.0, END)

    def show_results(self, results):
        self.clear()
        # TODO: more user friendly than just pretty json
        # TODO: it inserts nothing, is results empty? or dumps not correct? or not reaching scrolled text properly? need to debug
        self._output.insert(INSERT, json.dumps(results, ensure_ascii=False, indent=4))
