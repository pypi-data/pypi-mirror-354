
class Me:
    def __init__(self):
        self.name = "Radi"
        self.hair = "Brown"
        self.age = 26


def set_string():
    person = Me()
    text = f"My name is {person.name} and I am {person.age} years old with {person.hair} hair"
    return text


def display_me():
    output = set_string()
    print(output)