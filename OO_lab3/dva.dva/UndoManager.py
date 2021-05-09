class UndoManager:
    __instance = None

    @staticmethod 
    def getInstance():
        if UndoManager.__instance == None:
            UndoManager()
        return UndoManager.__instance

    def __init__(self):
        if UndoManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            UndoManager.__instance = self

        self.undo_stack = []
        self.redo_stack = []
        self.undo_stack_observers = []
        self.redo_stack_observers = []
    
    def add_undo_stack_observer(self, o):
        self.undo_stack_observers.append(o)
        self.notify_undo_obs()
    
    def add_redo_stack_observer(self, o):
        self.redo_stack_observers.append(o)
        self.notify_redo_obs()
    
    def notify_redo_obs(self):
        for o in self.redo_stack_observers: o.redo_stack_empty(not self.redo_stack)
    
    def notify_undo_obs(self):
        for o in self.undo_stack_observers: o.undo_stack_empty(not self.undo_stack)
    
    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            action.execute_undo()
            self.redo_stack.append(action)
            self.notify_redo_obs()
            self.notify_undo_obs()
    
    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            action.execute_do()
            self.undo_stack.append(action)
            self.notify_redo_obs()
            self.notify_undo_obs()
    
    def push(self, action):
        self.redo_stack = []
        self.undo_stack.append(action)
        self.notify_redo_obs()
        self.notify_undo_obs()
    
    def reset(self):
        self.undo_stack = []
        self.redo_stack = []
        self.notify_redo_obs()
        self.notify_undo_obs()