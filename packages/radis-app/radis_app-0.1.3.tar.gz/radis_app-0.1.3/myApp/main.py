from myApp.eula_gui import show_eula_gui


class Me:
    def __init__(self):
        self.name = "Radi"
        self.hair = "Brown"
        self.age = 26


def main():
    if show_eula_gui():
        output = set_string()
        print(output)


def set_string():
    person = Me()
    text = "My name is " + person.name + " and I am " + str(person.age) + "years old with " + person.hair + "hair"
    return text


def set_false_string():
    person = Me()
    text = f"My name is {person.name} and I am {person.age} years old with {person.hair} hair"
    return text



def show_eula():
    print("By using this software, you agree to the End User License Agreement.")
    agree = input("Do you accept the terms? (yes/no): ").strip().lower()
    if agree != "yes":
        print("You must accept the license to use this software.")
        exit(1)
# # Call this at the start of your main() function

main()