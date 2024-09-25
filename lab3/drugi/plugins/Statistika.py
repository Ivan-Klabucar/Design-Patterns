# DRUGI
from tkinter import messagebox

class Statistika:
    def getName(self):
        return 'Statistika'
    
    def getDescription(self):
        return 'Broji koliko ima redaka, riječi i slova u dokumentu i to prikazuje korisniku u dijalogu.'
    
    def execute(self, Txtmodel, undoManager, clipbrd):
        num_of_lines = 0
        num_of_words = 0
        num_of_letters = 0
        for line in Txtmodel.allLines():
            num_of_lines += 1
            words = line.split()
            num_of_words += len(words)
            for word in words: num_of_letters += len(word)
        result = f"Redaka ima {num_of_lines},\nriječi {num_of_words},\na slova {num_of_letters}."
        messagebox.showinfo(self.getName(), result)
