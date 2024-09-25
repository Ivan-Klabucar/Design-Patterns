# DRUGI
class Velikoslovo:
    def getName(self):
        return 'Velikoslovo'
    
    def getDescription(self):
        return 'prolazi kroz dokument i svako prvo slovo riječi mijenja u veliko ("ovo je tekst" ==> "Ovo Je Tekst").'
    
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
