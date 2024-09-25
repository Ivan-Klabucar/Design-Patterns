# DRUGI
class Capitalize:
    def getName(self):
        return 'Capitalize'
    
    def getDescription(self):
        return 'Capitalizes every word ("ovo je tekst" ==> "Ovo Je Tekst").'
    
    def execute(self, Txtmodel, undoManager, clipbrd):
        result = ''
        for line in Txtmodel.allLines():
            new_line = []
            words = line.split()
            for word in words: new_line += [word.capitalize()]
            new_line = ' '.join(new_line)
            new_line += '\n'
            result += new_line
        result = result[:-1]
        Txtmodel.all_new_lines(result)
