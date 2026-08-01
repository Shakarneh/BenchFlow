class Request:
    def __init__(self, client_name, required_skills, headcount, starts_on, max_bill_rate):
        self.client_name = client_name
        self.required_skills = required_skills
        self.headcount = headcount
        self.starts_on = starts_on
        self.max_bill_rate = max_bill_rate

    def is_satisfied_by(self, specialist):
        return(
            all(specialist.covers(required) for required in self.required_skills)
            and specialist.available_from <= self.starts_on
        )
    def __repr__(self):
        return f"Request({self.client_name!r}, {self.headcount}x, from {self.starts_on})"
