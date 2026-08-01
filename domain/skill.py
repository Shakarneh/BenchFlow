class Skill:
    def __init__(self , name):
        self.name = name
        
    def __repr__(self):
        return f"Skill({self.name!r})"
    
    def __eq__(self, other):
        if not isinstance (other,Skill):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
     