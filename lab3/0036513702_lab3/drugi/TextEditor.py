# DRUGI
from tkinter import Tk, Canvas, Frame, BOTH, W, YES, Menu, RAISED, FLAT, LEFT, TOP, Button, X, Label, BOTTOM, SUNKEN, filedialog
from TextEditorModel import *
from Location import *
from ClipboardStack import *
import os
from importlib import import_module

class TextEditor(Tk):
    def __init__(self, TextEditorModel):
        super().__init__()
        self.TextEditorModel = TextEditorModel
        self.canvas = None
        self.lines = []
        self.clipbrd = ClipboardStack()
        self.filename = None

        self.TextEditorModel.add_cursor_observer(self)
        self.TextEditorModel.add_text_observer(self)

        self.load_plugins()
        self.initUI()

        self.TextEditorModel.undoManager.add_undo_stack_observer(self)
        self.TextEditorModel.undoManager.add_redo_stack_observer(self)
        self.clipbrd.add_stack_obeserver(self)
        
    
    
    def load_plugins(self):
        def plugin_factory(module):
            m = import_module('.'+module, package='plugins')
            return getattr(m, module.capitalize())
        
        self.plugins=[]
        for mymodule in os.listdir('plugins'):
            moduleName, moduleExt = os.path.splitext(mymodule)
            if moduleExt=='.py':
                self.plugins.append(plugin_factory(moduleName)())

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select a File")
        try: 
            with open(filename, 'r') as f:
                content = f.read()
                self.TextEditorModel.all_new_lines(content)
                self.filename = filename
        except:
            return
    
    def save_file(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if not f: return
        f.write('\n'.join([x for x in self.TextEditorModel.allLines()]))
        f.close()
    
    def clipstack_empty(self, val):
        if val:
            self.editmenu.entryconfig("Paste", state="disabled")
            self.editmenu.entryconfig("Paste and Take", state="disabled")
            self.paste_button['state'] = 'disabled'
        else:
            self.editmenu.entryconfig("Paste", state="normal")
            self.editmenu.entryconfig("Paste and Take", state="normal")
            self.paste_button['state'] = 'normal'

    def redo_stack_empty(self, val):
        if val:
            self.editmenu.entryconfig("Redo", state="disabled")
            self.redo_button['state'] = 'disabled'
        else:
            self.editmenu.entryconfig("Redo", state="normal")
            self.redo_button['state'] = 'normal'
    
    def undo_stack_empty(self, val):
        if val:
            self.editmenu.entryconfig("Undo", state="disabled")
            self.undo_button['state'] = 'disabled'
        else:
            self.editmenu.entryconfig("Undo", state="normal")
            self.undo_button['state'] = 'normal'
    
    def check_if_selection(self):
        if self.TextEditorModel.selectionRange:
            self.editmenu.entryconfig("Cut", state="normal")
            self.editmenu.entryconfig("Copy", state="normal")
            self.cut_button['state'] = 'normal'
            self.copy_button['state'] = 'normal'
            self.editmenu.entryconfig("Delete selection", state="normal")
        else:
            self.editmenu.entryconfig("Cut", state="disabled")
            self.editmenu.entryconfig("Copy", state="disabled")
            self.cut_button['state'] = 'disabled'
            self.copy_button['state'] = 'disabled'
            self.editmenu.entryconfig("Delete selection", state="disabled")

    
    def initMenu(self):
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Exit", command=lambda: self.destroy())
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=lambda: self.TextEditorModel.undoManager.undo())
        self.editmenu.add_command(label="Redo", command=lambda: self.TextEditorModel.undoManager.redo())
        self.editmenu.add_command(label="Cut", command=self.copy_erase_to_clipbrd)
        self.editmenu.add_command(label="Copy", command=self.copy_to_clipbrd)
        self.editmenu.add_command(label="Paste", command=self.paste_top_of_clipbrd)
        self.editmenu.add_command(label="Paste and Take", command=self.paste_from_clipbrd)
        self.editmenu.add_command(label="Delete selection", command=self.TextEditorModel.deleteBefore)
        self.editmenu.add_command(label="Clear document", command=lambda: self.TextEditorModel.all_new_lines(''))
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.movemenu = Menu(self.menubar, tearoff=0)
        self.movemenu.add_command(label="Cursor to document start", command=lambda: self.TextEditorModel.set_cursor(Location(0,0)))
        self.movemenu.add_command(label="Cursor to document end", command=lambda: self.TextEditorModel.set_cursor(self.TextEditorModel.get_last_loc()))
        self.menubar.add_cascade(label="Move", menu=self.movemenu)
        self.pluginmenu = Menu(self.menubar, tearoff=0)
        for plugin in self.plugins:
            cmd = lambda plugin=plugin: plugin.execute(self.TextEditorModel, self.TextEditorModel.undoManager, self.clipbrd)
            self.pluginmenu.add_command(label=plugin.getName(), command=cmd)
        self.menubar.add_cascade(label="Plugins", menu=self.pluginmenu)
        self.config(menu=self.menubar)
    
    def initToolbar(self):
        self.toolbar = Frame(self, bd=1, relief=RAISED, bg='azure')
        self.undo_button = Button(self.toolbar, text="Undo", relief=FLAT, command=lambda: self.TextEditorModel.undoManager.undo())
        self.redo_button = Button(self.toolbar, text="Redo", relief=FLAT, command=lambda: self.TextEditorModel.undoManager.redo())
        self.cut_button = Button(self.toolbar, text="Cut", relief=FLAT, command=self.copy_erase_to_clipbrd)
        self.copy_button = Button(self.toolbar, text="Copy", relief=FLAT, command=self.copy_to_clipbrd)
        self.paste_button = Button(self.toolbar, text="Paste", relief=FLAT, command=self.paste_top_of_clipbrd)
        self.undo_button.pack(side=LEFT, padx=2, pady=2)
        self.redo_button.pack(side=LEFT, padx=2, pady=2)
        self.cut_button.pack(side=LEFT, padx=2, pady=2)
        self.copy_button.pack(side=LEFT, padx=2, pady=2)
        self.paste_button.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack(side=TOP, fill=X)
    
    def initStatusbar(self):
        self.statusbar = Label(self, text="", bd=1, relief=RAISED, anchor=W, bg='azure')
        self.statusbar.pack(side=BOTTOM, fill=X)
        def updateCursorLocation(loc):
            self.statusbar['text'] = f'Cursor: row: {loc.row + 1}, column: {loc.col}'
        self.statusbar.updateCursorLocation = updateCursorLocation
        self.TextEditorModel.add_cursor_observer(self.statusbar)
        self.statusbar.updateCursorLocation(self.TextEditorModel.cursorLocation)


    def initUI(self):
        self.title('Text Editor')
        self.geometry("600x700")
        self.initMenu()
        self.initToolbar()
        self.initStatusbar()
        self.canvas = Canvas(self, bd=0, bg='light goldenrod yellow', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.update_text()
        self.canvas.focus_set()

        self.bind('<Left>', lambda e: self.TextEditorModel.moveCursorLeft())
        self.bind('<Up>', lambda e: self.TextEditorModel.moveCursorUp())
        self.bind('<Down>', lambda e: self.TextEditorModel.moveCursorDown())
        self.bind('<Right>', lambda e: self.TextEditorModel.moveCursorRight())
        self.bind('<Shift-Left>', lambda e: self.mov_sel_left())
        self.bind('<Shift-Up>', lambda e: self.mov_sel_up())
        self.bind('<Shift-Down>', lambda e: self.mov_sel_down())
        self.bind('<Shift-Right>', lambda e: self.mov_sel_right())
        self.bind('<BackSpace>', lambda e: self.TextEditorModel.deleteBefore())
        self.bind('<Shift-BackSpace>', lambda e: self.TextEditorModel.deleteAfter())
        self.bind('<Delete>', lambda e: self.TextEditorModel.deleteAfter())
        self.bind('<Key>', self.myb_insert)
        self.bind('<Control-Key-c>', lambda e: self.copy_to_clipbrd())
        self.bind('<Control-Key-x>', lambda e: self.copy_erase_to_clipbrd())
        self.bind('<Control-Key-v>', lambda e: self.paste_top_of_clipbrd())
        self.bind('<Control-Shift-Key-V>', lambda e: self.paste_from_clipbrd())
        self.bind('<Control-Key-z>', lambda e: self.TextEditorModel.undoManager.undo())
        self.bind('<Control-Key-y>', lambda e: self.TextEditorModel.undoManager.redo())
    
    def paste_from_clipbrd(self):
        if self.clipbrd.is_empty(): return
        self.TextEditorModel.insert(self.clipbrd.pop())

    def paste_top_of_clipbrd(self):
        if self.clipbrd.is_empty(): return
        self.TextEditorModel.insert(self.clipbrd.peek())

    def copy_to_clipbrd(self):
        if not self.TextEditorModel.selectionRange: return
        text_list = [line for line in self.TextEditorModel.linesRange(self.TextEditorModel.selectionRange.start.row, self.TextEditorModel.selectionRange.end.row + 1)]
        text = '\n'.join(text_list)
        text = text[self.TextEditorModel.selectionRange.start.col:]
        skip_at_end = len(self.TextEditorModel.lines[self.TextEditorModel.selectionRange.end.row]) - self.TextEditorModel.selectionRange.end.col
        if skip_at_end > 0: text = text[:-skip_at_end]
        self.clipbrd.push(text)
    
    def copy_erase_to_clipbrd(self):
        if not self.TextEditorModel.selectionRange: return
        self.copy_to_clipbrd()
        self.TextEditorModel.deleteRange(self.TextEditorModel.selectionRange)

    def myb_insert(self, event):
        if event.char != '' and (event.char.isprintable() or ord(event.char) == 32):
            self.TextEditorModel.insert(event.char)
        
        if event.char == '\r' or event.char == '\n':
            self.TextEditorModel.insert('\n')
        elif event.keysym == 'Return':
            self.TextEditorModel.insert('\n')


    def mov_sel_left(self):
        r = self.TextEditorModel.getSelectionRange()
        if r:
            old_loc = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorLeft(selection=True)
            new_loc = copy_Location(self.TextEditorModel.cursorLocation)
            if old_loc == new_loc: return
            new_r = copy_Range(r)
            if new_loc < r.end and new_loc >= r.start:
                new_r.end = new_loc
            elif new_loc < r.start:
                new_r.start = new_loc
            else:
                return
            self.TextEditorModel.setSelectionRange(new_r)
        else:
            new_end = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorLeft(selection=True)
            new_start = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.setSelectionRange(LocationRange(new_start, new_end))
    
    def mov_sel_right(self):
        r = self.TextEditorModel.getSelectionRange()
        if r:
            old_loc = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorRight(selection=True)
            new_loc = copy_Location(self.TextEditorModel.cursorLocation)
            if old_loc == new_loc: return
            new_r = copy_Range(r)
            if new_loc > r.start and new_loc <= r.end:
                new_r.start = new_loc
            elif new_loc > r.end:
                new_r.end = new_loc
            else:
                return
            self.TextEditorModel.setSelectionRange(new_r)
        else:
            new_start = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorRight(selection=True)
            new_end = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.setSelectionRange(LocationRange(new_start, new_end))
    
    def mov_sel_up(self):
        r = self.TextEditorModel.getSelectionRange()
        if r:
            old_loc = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorUp(selection=True)
            new_loc = copy_Location(self.TextEditorModel.cursorLocation)
            if old_loc == new_loc: return
            new_r = copy_Range(r)
            if new_loc < r.end and new_loc >= r.start:
                new_r.end = new_loc
            elif new_loc < r.start:
                new_r.start = new_loc
            else:
                return
            self.TextEditorModel.setSelectionRange(new_r)
        else:
            new_end = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorUp(selection=True)
            new_start = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.setSelectionRange(LocationRange(new_start, new_end))
    
    def mov_sel_down(self):
        r = self.TextEditorModel.getSelectionRange()
        if r:
            old_loc = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorDown(selection=True)
            new_loc = copy_Location(self.TextEditorModel.cursorLocation)
            if old_loc == new_loc: return
            new_r = copy_Range(r)
            if new_loc < r.start and new_loc <= r.end:
                new_r.start = new_loc
            elif new_loc > r.end:
                new_r.end = new_loc
            else:
                return
            self.TextEditorModel.setSelectionRange(new_r)
        else:
            new_start = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.moveCursorDown(selection=True)
            new_end = copy_Location(self.TextEditorModel.cursorLocation)
            self.TextEditorModel.setSelectionRange(LocationRange(new_start, new_end))

    def update_selection(self):
        r = self.TextEditorModel.getSelectionRange()
        self.canvas.delete('selection')
        if r:
            curr_row = r.start.row
            while curr_row <= r.end.row:
                s_col = 0
                e_col = len(self.TextEditorModel.lines[curr_row])
                if curr_row == r.start.row: s_col = r.start.col
                if curr_row == r.end.row: e_col = r.end.col
                s_id = self.canvas.create_rectangle(3 +7*s_col, 3+15*curr_row, 3 + 7*e_col,  15*(curr_row+1), fill='deep sky blue', tags='selection', outline='')
                self.canvas.tag_lower(s_id, "line")
                curr_row += 1
    
    def updateCursorLocation(self, loc):
        self.canvas.delete('cursor')
        self.canvas.create_line(3 + 7 * loc.col, 3+15*loc.row, 3 + 7 * loc.col, 15*(loc.row + 1), tags="cursor")

    def update_text(self):
        self.check_if_selection()
        self.canvas.delete('all')
        idx = 0
        self.lines = []
        for textLine in self.TextEditorModel.allLines():
            self.lines.append(self.canvas.create_text(4, 8 + 15 * idx, anchor=W, text=textLine, font='TkFixedFont', tags="line"))
            idx += 1
        self.updateCursorLocation(self.TextEditorModel.cursorLocation)
        self.update_selection()


tem = TextEditorModel("This text editor was developed by me,\nIvan Klabucar!")
te = TextEditor(tem)
te.mainloop()