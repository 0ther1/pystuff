from tkinter import *

_FRAMEKEYS = ['pady', 'colormap', 'class', 'padx', 'visual', 'height', 'container']
_LABELKEYS = ['foreground', 'disabledforeground', 'justify', 'activeforeground', 'pady', 'activebackground', 'state', 'padx', 'textvariable', 'font', 'anchor', 'compound', 'bitmap', 'wraplength', 'image', 'text', 'height', 'fg', 'underline']
_ENTRYKEYS = ['foreground', 'disabledforeground', 'justify', 'show', 'state', 'textvariable', 'selectbackground', 'insertofftime', 'exportselection', 'font', 'invalidcommand', 'readonlybackground', 'selectforeground', 'validatecommand', 'validate', 'insertwidth', 'insertborderwidth', 'insertontime', 'selectborderwidth', 'disabledbackground', 'vcmd', 'xscrollcommand', 'insertbackground', 'invcmd', 'fg']
_SPINBOXKEYS = ['foreground', 'disabledforeground', 'justify', 'activebackground', 'repeatdelay', 'state', 'textvariable', 'selectbackground', 'from_', 'insertofftime', 'values', 'exportselection', 'font', 'invalidcommand', 'repeatinterval', 'format', 'buttoncursor', 'readonlybackground', 'selectforeground', 'wrap', 'validatecommand', 'buttonuprelief', 'validate', 'command', 'insertwidth', 'buttonbackground', 'insertborderwidth', 'insertontime', 'selectborderwidth', 'disabledbackground', 'vcmd', 'increment', 'xscrollcommand', 'insertbackground', 'buttondownrelief', 'to', 'invcmd', 'fg']

class LabelEntry(Frame):
    def __init__(self, master=None, **kw):
        kwcopy = kw.copy()
        for k in _LABELKEYS:
            if (k in _FRAMEKEYS):
                continue
            try:
                kw.pop(k)
            except:
                pass
        for k in _ENTRYKEYS:
            if (k in _FRAMEKEYS):
                continue            
            try:
                kw.pop(k)
            except:
                pass
        super().__init__(master, kw)        
        
        kw = kwcopy.copy()
        for k in _FRAMEKEYS:
            if (k in _LABELKEYS):
                continue            
            try:
                kw.pop(k)
            except:
                pass
        for k in _ENTRYKEYS:
            if (k in _LABELKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        if ("textvariable" in kw):
            kw.pop("textvariable")
        if ("width" in kw):
            kw.pop("width")
        if ("state" in kw and kw["state"] == "readonly"):
            kw["state"] = NORMAL
        self._label = Label(self, kw)
        self._label.pack(side=LEFT, fill=X, expand=True)
        
        kw = kwcopy.copy()
        for k in _FRAMEKEYS:
            if (k in _ENTRYKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        for k in _LABELKEYS:
            if (k in _ENTRYKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        self._entry = Entry(self, kw)
        self._entry.pack(side=RIGHT, fill=X, expand=True)
        
class LabelSpinbox(Frame):
    def __init__(self, master=None, **kw):
        kwcopy = kw.copy()
        for k in _LABELKEYS:
            if (k in _FRAMEKEYS):
                continue
            try:
                kw.pop(k)
            except:
                pass
        for k in _SPINBOXKEYS:
            if (k in _FRAMEKEYS):
                continue            
            try:
                kw.pop(k)
            except:
                pass
        super().__init__(master, kw)        
        
        kw = kwcopy.copy()
        for k in _FRAMEKEYS:
            if (k in _LABELKEYS):
                continue            
            try:
                kw.pop(k)
            except:
                pass
        for k in _SPINBOXKEYS:
            if (k in _LABELKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        if ("textvariable" in kw):
            kw.pop("textvariable")
        if ("width" in kw):
            kw.pop("width")
        if ("state" in kw and kw["state"] == "readonly"):
            kw["state"] = NORMAL            
        self._label = Label(self, kw)
        self._label.pack(side=LEFT, fill=X, expand=True)
        
        kw = kwcopy.copy()
        for k in _FRAMEKEYS:
            if (k in _SPINBOXKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        for k in _LABELKEYS:
            if (k in _SPINBOXKEYS):
                continue              
            try:
                kw.pop(k)
            except:
                pass
        self._spinbox = Spinbox(self, kw)
        self._spinbox.pack(side=RIGHT, fill=X, expand=True)