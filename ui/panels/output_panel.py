from tkinter import Frame, Scrollbar
from tkinter.ttk import Treeview
from typing import Any, Iterable, List

from ui.models.message import Message


class OutputPanel(Frame):
    def __init__(self, master):
        super().__init__(master=master)

        tree = Treeview(self, columns=('Timestamp', 'Type', 'User', 'Amount', 'Message'), show='headings', selectmode='none')
        tree.pack(side='left', fill='both', expand=True)

        scrollbar = Scrollbar(self, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)
        tree.tag_configure('oddrow', background='white')
        tree.tag_configure('evenrow', background='gray95')

        tree.heading('Timestamp', text='Timestamp')
        tree.column('Timestamp', minwidth=70, width=70, stretch=False)
        
        tree.heading('Type', text='Type')
        tree.column('Type', minwidth=100, width=100, stretch=False)
        
        tree.heading('User', text='User')
        tree.column('User', minwidth=100, width=100, stretch=False)
        
        tree.heading('Amount', text='Amount')
        tree.column('Amount', minwidth=60, width=60, stretch=False)
        
        tree.heading('Message', text='Message')
        tree.column('Message', minwidth=400, width=400)

        self._tree = tree

    def clear(self):
        for i in self._tree.get_children():
            self._tree.delete(i)

    def show_results(self, results: List[Message]):
        self.clear()

        for idx, msg in enumerate(results):
            self._tree.insert('', 'end', values=(
                msg.timestamp,
                msg.type,
                msg.user,
                msg.amount,
                msg.message
            ), tags=('evenrow' if idx % 2 == 0 else 'oddrow'))

    def get_output_as_csv(self) -> Iterable[List[Any]]:
        yield ['Timestamp', 'Type', 'User', 'Amount', 'Message']
        for child in self._tree.get_children():
            yield self._tree.item(child)['values']

