class User:
    def __init__(self, id, name, selections):
        self.id = id
        self.name = name
        self.selections = selections
        self.happiness = 1

    def __eq__(self, other):
       return self.id == other.id
    
    ## This might cause problems when we want to inspect the rankings of choices of the user. 
    def remove_first_selection(self):
        new_selections = self.selections
        new_selections.pop(0)
        self.selections = new_selections
        self.happiness += 1