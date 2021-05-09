class ClipboardStack:
    def __init__(self):
        self.stack_texts = []
        self.stack_obeservers = []
    
    def add_stack_obeserver(self, o):
        self.stack_obeservers.append(o)
        self.notify()

    def notify(self):
        for o in self.stack_obeservers:
            o.clipstack_empty(not self.stack_texts)
    
    def push(self, x):
        self.stack_texts.append(x)
        self.notify()
    
    def is_empty(self):
        return not self.stack_texts
    
    def pop(self):
        res = self.stack_texts.pop()
        self.notify()
        return res
    
    def peek(self):
        return self.stack_texts[-1]
    
    def clear(self):
        self.stack_texts = []
        self.notify()
    
