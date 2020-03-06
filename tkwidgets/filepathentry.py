from tkinter import *
from tkinter import filedialog

# types
DIRECTORY = "directory"
FILE = "file"

class FilepathEntry(Frame):
    """Widget to write filepath in entry or use button 'Browse' to open filedialog."""
    def __init__(self, master=None, **kw):
        """Create a new FilepathEntry. Widget-specific options: type - FILE or DIRECTORY - filedialog mode."""
        super().__init__(master=None, **kw)
        self._str_filepath = StringVar(self)
        self._entry = Entry(self, textvariable=self._str_filepath, width=50)
        self._entry.pack(side=LEFT, fill=X, expand=True)
        self._btn_browse = Button(self, text="Browse", command=self.on_browse)
        self._btn_browse.pack(side=RIGHT, fill=X, expand=True)
        if ("type" in kw.keys()):
            self._type = kw["type"]
        else:
            self._type = FILE
        if ("width" in kw.keys()):
            self._entry["width"] = kw["width"]
        
    def on_browse(self):
        if (self._type == DIRECTORY):
            input = filedialog.askdirectory()
        else:
            input = filedialog.askopenfilename()
        if (input):
            self._str_filepath.set(input)