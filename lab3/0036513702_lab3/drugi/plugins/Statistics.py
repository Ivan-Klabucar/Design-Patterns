# DRUGI
from tkinter import messagebox

class Statistics:
    def getName(self):
        return 'Statistics'
    
    def getDescription(self):
        return 'Counts how many lines, words, and characters there are in the document.'
    
    def execute(self, Txtmodel, undoManager, clipbrd):
        num_of_lines = 0
        num_of_words = 0
        num_of_letters = 0
        for line in Txtmodel.allLines():
            num_of_lines += 1
            words = line.split()
            num_of_words += len(words)
            for word in words: num_of_letters += len(word)
        result = f"There are {num_of_lines} lines,\n {num_of_words} words,\nand {num_of_letters} characters."
        messagebox.showinfo(self.getName(), result)
