# the backend of the label classifier

import os
import tkinter
from tkinter import ttk
from typing import Union

class DescriptionLabeler:
    """A class for labeling charge descriptions."""
    categories = []
    current = 0

    def __init__(self, charge_description_list: list[str], categories: list[str]=[]):
        """Initialize the LabelClassifier class."""
        self.charge_description_list = charge_description_list
        self.labels = [""] * len(charge_description_list)
        
        if categories:
            self.categories = categories
 
    def get_current_description(self) -> str:
        """Return the current description."""
        if self.current < len(self.charge_description_list):
            return self.charge_description_list[self.current]
        else:
            return ""

    def label(self, label: str):
        """Label the current description. Move to the next description."""
        self.labels[self.current] = label
        self.current += 1

    def get_categories(self) -> list[str]:
        """Return the categories."""
        return self.categories

    def get_labels(self) -> list[str]:
        """Return a list of labels for the given descriptions."""
        return self.labels

    def get_labeled_descriptions(self) -> list[tuple[str, str]]:
        """Return a list of labeled descriptions."""
        return list(zip(self.labels, self.charge_description_list))


class AutocompleteEntry(ttk.Entry):
    """A class for autocorrecting charge descriptions."""
    def __init__(self, label_list: list[str], root: Union[ttk.Widget, None] = None, **kwargs):
        """Initialize the Autocorrect class."""
        self.label_list = label_list

        self.var = tkinter.StringVar()
        self.var.trace('w', self.changed)
        self.var.set("")
        self.listbox = None
        self.complete_list = []

        super().__init__(root, textvariable=self.var)
        self.bind("<Down>", self.down)
        self.bind("<Up>", self.up)

    def set_label_list(self, label_list: list[str]):
        """Set the list of charge descriptions."""
        self.label_list = label_list

    def add_label(self, label: str):
        """Add a label to the list of labels."""
        if label not in self.label_list:
            self.label_list.append(label)

    def get_label_list(self) -> list[str]:
        """Return the list of labels."""
        return self.label_list

    def down(self, event):
        """Move down the listbox."""
        if self.listbox:
            self.listbox.focus_set()
            self.listbox.select_set(0)

    def up(self, event):
        """Move up the listbox."""
        if self.listbox:
            self.listbox.focus_set()
            self.listbox.select_set(tkinter.END)

    def focus(self):
        """Set the focus to the entry."""
        self.focus_set()

    def changed(self, name, index, mode):
        """Update the list of possible completions."""
        if self.var.get():
            matches = [word for word in self.label_list if word.lower().startswith(self.var.get().lower())]
            if matches:
                self.complete_list = matches
                self.listbox_update()
            else:
                if self.listbox:
                    self.listbox.destroy()
                    self.listbox = None
        else:
            if self.listbox:
                self.listbox.destroy()
                self.listbox = None

    def listbox_update(self):
        """Update the listbox."""
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

        if self.var.get():
            self.listbox = tkinter.Listbox(self.master, height=int(1.2*len(self.complete_list)))
            self.listbox.bind("<Double-Button-1>", self.selection)
            self.listbox.bind("<Return>", self.selection)
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

            for item in self.complete_list:
                self.listbox.insert(tkinter.END, item)

    def selection(self, event):
        """Select the item from the listbox."""
        if self.listbox:
            self.var.set(self.listbox.get(tkinter.ACTIVE))
            self.listbox.destroy()
            self.listbox = None

    def get(self):
        """Return the current text."""
        return self.var.get()

    def set(self, value):
        """Set the current text."""
        self.var.set(value)


class DescriptionLabelerGUI(ttk.Frame):
    """A class for classifying labels for a list of descriptions."""

    def __init__(self,  description_labeler: DescriptionLabeler, root: Union[ttk.Widget, None] = None):
        """Initialize the DescriptionLabelerGUI class."""
        super().__init__(root)

        self.description_labeler = description_labeler

        self.description = ttk.Label(self, text="")
        self.description.pack()

        self.label = tkinter.StringVar()
        self.auto_complete_entry = AutocompleteEntry(self.description_labeler.get_categories())
        # self.auto_complete_entry = tkinter.Entry(self, textvariable=self.label)
        self.auto_complete_entry.pack()

        self.button = ttk.Button(self, text="confirm label", command=self.enter_label)
        self.button.pack()

        self.update_description()

    def enter_label(self):
        """Enter the label."""
        label = self.auto_complete_entry.get()
        if label not in self.auto_complete_entry.get_label_list():
            self.auto_complete_entry.add_label(label)
        if label not in self.description_labeler.get_categories():
            self.description_labeler.categories.append(label)
        self.description_labeler.label(self.auto_complete_entry.get())
        self.auto_complete_entry.set("")
        self.auto_complete_entry.focus_set()
        
        if not self.update_description():
            self.on_complete()

    def update_description(self):
        """Update the description."""
        description = self.description_labeler.get_current_description()
        if description:
            self.description["text"] = description
            return True
        else:
            return False

    # an event for when the labels are complete
    def on_complete(self):
        # remove button and text entry
        self.button.destroy()
        self.auto_complete_entry.destroy()

        self.description["text"] = "Labels complete!"
    
if __name__ == "__main__":
    root = ttk.Frame(width=500, height=5000, padding=10, relief=tkinter.RIDGE, borderwidth=5, takefocus=True, name="root", class_="root", style="root.TFrame", cursor="arrow")
    # title of the window is the name of the file
    root.master.title(os.path.basename(__file__))
    root.pack()

    root.setvar("tkThemeName", "clam")
    root.setvar("tkFont", "TkDefaultFont 12")
    
    

    label_classifier = DescriptionLabeler(["hello", "world", "foo", "bar"])
    label_classifier_gui = DescriptionLabelerGUI(label_classifier, root=root)
    label_classifier_gui.pack()

    root.mainloop()
    # label_classifier_gui.mainloop()
