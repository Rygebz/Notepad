from tkinter import filedialog, messagebox, Menu, Text, Tk, BOTH, END
from typing import Optional
from pathlib import Path

current_file: Optional[Path] = None
filetypes = (("Text Files", "*.txt"), ("All Files", "*.*"))

def setTitle(root: Tk, filename: Optional[Path]):
    title = f"{filename.name} - Notepad" if filename else "Notepad"
    root.title(title)

def canContinue(root: Tk, text: Text):
    if text.edit_modified():
        result = messagebox.askyesnocancel(
            title="Unsaved Changes",
            message = "Do you want to save changes?"
        )
        if result is None: # Cancel
            return False
        elif result: # Save
            save(root, text)
        return True
    
    def newFile(root: Tk, text: Text):
        global current_file
        if not canContinue(root, text):
            return
        text.delete("1,0", END)
        current_file = None
        setTitle(root, current_file)

    def openFile(root: Tk, text: Text):
        global current_file
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if not filename or not canContinue(root, text):
            return
        with open(filename, encoding="utf8") as file:
            content = file.read()
        text.delete("1.0", END)
        text.insert("1.0", content)
        text.edit_modified(False)
        current_file = Path(filename)
        setTitle(root, current_file)

    def saveCurrent(text: Text) -> None:
        global current_file
        if current_file:
            current_file.write_text(text.get("1.0", END), encoding="utf8")

    def save(root: Tk, text: Text):
        global current_file
        if current_file is None:
            saveAs(root, text)
        else: 
            saveCurrent(text)

root = Tk()
root.title("Notepad")
root.geometry("800x600")
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0) # Test
filemenu.add_command(label="New", command="")
filemenu.add_command(label="Open", command="")
filemenu.add_command(label="Save", command="")
filemenu.add_command(label="Save As...", command="")
filemenu.add_command(label="Close", command="")

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command="")
editmenu.add_separator()
editmenu.add_command(label="Cut", command="")
editmenu.add_command(label="Copy", command="")
editmenu.add_command(label="Paste", command="")
editmenu.add_command(label="Delete", command="")
editmenu.add_command(label="Select All", command="")
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command="")
helpmenu.add_command(label="About...", command="")
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)


root.mainloop()

