# create a gui window that displays items in a listbox
# and allows the user to select an item
# 

import tkinter as tk
from tkinter import ttk, dnd, filedialog
import pandas as pd

from description_labeler import DescriptionLabeler, DescriptionLabelerGUI

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Listbox')
        self.geometry('400x400')
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill='both', expand=True)
        self.listbox.insert('end', *['item {}'.format(i) for i in range(100)])
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        print('selected item: {}'.format(self.listbox.get(self.listbox.curselection())))

# create a frame which has a file selection button and a listbox
class FileFrame(ttk.Frame):
    def __init__(self):
        super().__init__()

        self.file = tk.StringVar()

        self.file_button = ttk.Button(self, text="Select file", command=self.file_button_clicked)
        self.file_button.pack()

        self.file_label = ttk.Label(self)
        self.file_label.pack()

        # bind file_label to file change event
        self.file.trace_add("write", lambda *args: self.file_label.configure(text=self.path_to_filename(self.file.get())))

        # add a drodown listbox with options "Simplii", "BMO", "Scotia", "TD", "RBC", "CIBC", "Desjardins"
        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        banks = ["Simplii", "BMO", "Scotia", "TD", "RBC", "CIBC", "Desjardins"]
        for bank in banks:
            self.listbox.insert(tk.END, bank)

        # add a "next" button
        self.next_button = ttk.Button(self, text="Next")
        self.next_button.pack()


    def path_to_filename(self, path: str) -> str:
        """Return the filename from a path."""
        return path.split("/")[-1]

    def file_button_clicked(self):
        self.file.set(filedialog.askopenfilename())

    def get_file(self):
        return self.file.get()

    def get_type(self):
        return self.listbox.get(self.listbox.curselection())

    def set_list(self, items: list[str]):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)


# create an application window that displays the file frame

class App(ttk.Frame):
    def __init__(self):
        super().__init__()

        self.file_frame = FileFrame()
        description_labeler = DescriptionLabeler() 
        self.label_frame = DescriptionLabelerGUI(description_labeler, root=self)

        self.file_frame.pack()

        self.file_frame.next_button["command"] = lambda: self.file_frame_next_button_clicked()

        self.label_frame

    def file_frame_next_button_clicked(self):
        file = self.file_frame.get_file()
        type = self.file_frame.get_type()

        df = pd.read_csv(file)
        if type == "Simplii":
            self.simplii(df)
        elif type == "BMO":
            self.bmo(df)
        else:
            self.other(df)

        self.file_frame.pack_forget()
        
        self.label_frame.display_next()
        self.label_frame.pack()

    def simplii(self, df):
        self.label_frame.add_descriptions(df[" Transaction Details"].tolist())
    
    def bmo(self, df):
        self.label_frame.add_descriptions(df["Description"].tolist())
    
    def other(self, df):
        self.label_frame.add_descriptions(df["Description"].tolist())



if __name__ == "__main__":
    app = App()

    app.mainloop()
    