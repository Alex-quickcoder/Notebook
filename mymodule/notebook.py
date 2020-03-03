"""Work with Note and Notebook classes."""
from datetime import datetime as dtime
import re


class Note:
    """Represent a note in a notebook."""
    _id = 1

    def __init__(self, memo: str, tags=[]):
        """Create a note with a certain id.

        :param memo: a message of the note
        :param tags: tags of the note like [str, ..]
        """
        self.memo = memo
        self.creation_date = dtime.today()
        self.tags = tags
        self.id = Note._id
        Note._id += 1

    def match(self, search_filter: str) -> bool:
        """Match the note with the search filter.

        Tags in the filter should be separated by any
        non-alphanumeric character and not by _.
        :param search_filter: a string to match
        :return: True if match is successful, otherwise False
        """
        return ((search_filter in self.memo) or
                any([re.search(f"(\\W|^){tag}(\\W|$)", search_filter)
                     for tag in self.tags]))

    def __str__(self):
        final = f"[{self.creation_date}] - {self.id}: {self.memo}"

        if self.tags:
            final += f"  (+{', +'.join(self.tags)})"
        return final

    def __repr__(self):
        return (f"Note({self.id}, {self.memo}, "
                f"{self.tags}, {self.creation_date})")


class Notebook:
    """Store notes and search for them."""

    def __init__(self):
        """Initialize an empty list of notes."""
        self.notes = []

    def new_note(self, memo: str, tags=[]):
        """Initialize a new note in the notebook.

        :param memo: a note's content
        :param tags: a note's tags (optional)
        """
        self.notes.append(Note(memo, tags))

    def modify(self, note_id: int, delete: bool = False,
               n_memo: str = "", n_tags: list = []):
        """Modify a note with memo or tags by id, or delete it.

        :param note_id: id of the note to modify.
        :param n_memo: new memo
        :param n_tags: new tags
        :param delete: whether to delete this note
        :return: True if operation successful, else None
        """
        for note in self.notes:
            if note.id == note_id:
                if delete:
                    self.notes.remove(note)
                    return True
                if n_memo:
                    note.memo = n_memo
                if n_tags:
                    note.tags = n_tags
                return True
        return None

    def search(self, search_filter: str) -> list:
        """Search a note by memo or tags.

        :param search_filter: a string to search the note by
        :return: a list of all found notes
        """
        return [note for note in self.notes if note.match(search_filter)]
