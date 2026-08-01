class Specialist:
    def __init__(self, full_name, cost_rate, available_from, skills):
        self.full_name = full_name
        self.cost_rate = cost_rate
        self.available_from = available_from
        self.skills = skills

    def covers(self, required):
        return any(skill_level.covers(required) for skill_level in self.skills)
        
    def __repr__(self):
        return f"Specialist({self.full_name!r})"
