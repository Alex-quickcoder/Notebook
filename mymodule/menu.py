"""Work with a notebook with an interface."""
import sys
from notebook import Notebook, Note
from time import sleep
from os.path import isfile


class Menu:
    """Display a menu and respond to choices when run.

    :var file_name: a file name where to store notes.
    """
    file_name = "notes.txt"

    def __init__(self):
        """Initialize a notebook and menu choices."""
        self.notebook = Notebook()
        self.choices = {"1": self.show_notes,
                        "2": self.search_notes,
                        "3": self.add_note,
                        "4": self.modify_note,
                        "5": self.clear,
                        "6": self.save,
                        "7": self.quit}

    def display_menu(self):
        """Display the choices to the user."""
        print("Menu Choices:")
        for key in self.choices:
            choice = self.choices[key].__name__
            choice = choice.replace("_", " ").title()
            print(f"{key}: {choice}")

    def run(self):
        """Display the menu and respond to the choices."""
        choice_quant = len(self.choices)

        if isfile(self.file_name):
            notes = self.notebook.notes
            with open("notes.txt") as file:
                for line in file:
                    line = line.split("\t\t")
                    line[1] = line[1][1:-1].replace("'", "")
                    line[1] = line[1].split(", ")
                    if line[1][0] == "":
                        notes.append(Note(line[0], []))
                    else:
                        notes.append(Note(line[0], line[1]))
                    notes[-1].creation_date = line[2][:-1]
            print("Added saved notes.")
            self.show_notes()
            sleep(0.5)

        while True:
            self.display_menu()
            choice = input(f"Enter a valid option(1-{choice_quant}): ")
            action = self.choices.get(choice)
            if action:
                action()
                sleep(0.5)
            else:
                print(f"'{choice}' is invalid, try again...")

    def show_notes(self, notes: list =None):
        """Show all stored notes.

        :param notes: notes to show if available
        (if None shows all notes)
        """
        if notes is None:
            notes = self.notebook.notes
        elif not notes:
            print("Search didn't return anything.")
        for note in notes:
            print(note)

    def search_notes(self):
        """Search for a note by memo and tags."""
        search_filter = input("Search for (enter separated tags "
                              "or memo fragment): ")
        notes = self.notebook.search(search_filter)
        self.show_notes(notes)

    def add_note(self):
        """Add a note to the notebook."""
        memo = input("Enter a memo: ")
        tags = input("Enter comma-separated tags or press Enter to skip: ")
        if tags:
            self.notebook.new_note(memo, tags.split(","))
        else:
            self.notebook.new_note(memo)
        print("Your note has been added.")

    def modify_note(self):
        """Modify a note."""
        try:
            n_id = int(input("Enter a note id: "))
        except (TypeError, ValueError):
            print("Operation has failed.")
            return None

        while True:
            delete = input("Enter whether to delete a note(y/n): ").lower()
            if delete in {"y", "yes", "1", "true"}:
                if self.notebook.modify(n_id, delete=True):
                    print("Operation successful.")
                else:
                    print("Note with this id doesn't exist.")
                return None
            elif delete in {"n", "no", "0", "false"}:
                break
            print("Response unclear, try again...")

        memo = input("Enter a memo (press Enter to skip): ")
        tags = input("Enter tags (press Enter to skip): ")
        oper1, oper2 = None, None
        if memo:
            oper1 = self.notebook.modify(n_id, n_memo=memo)
        if tags:
            oper2 = self.notebook.modify(n_id, n_tags=tags.split(","))

        if oper1 or oper2:
            print("Operation successful.")
        else:
            print("Note with this id not found or not modified.")

    def clear(self):
        """Delete all notes."""
        while True:
            clear = input("Are you sure you want "
                          "to clear all notes(y/n): ").lower()
            if clear in {"y", "yes", "1", "true"}:
                self.notebook.notes = []
                Note._id = 1
                break
            elif clear in {"n", "no", "0", "false"}:
                break
            else:
                print("Response unclear, try again...")

    def save(self):
        """Save notes into a file."""
        with open(self.file_name, mode="w+") as file:
            for note in self.notebook.notes:
                file.write(f"{note.memo}\t\t{note.tags}"
                           f"\t\t{note.creation_date}\n")
        print("Notes saved in notes.txt.")

    def quit(self):
        """Quit the program."""
        print("Thank you for using your notebook today.")
        sys.exit(0)


if __name__ == "__main__":
    Menu().run()
