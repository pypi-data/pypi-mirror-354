import re

from rich import print
from rich.table import Table
from rich.text import Text

from app.core.errors import NoteAppError
from app.core.models import NoteWithStatus, Status

NO_TEXT = Text("-", style="italic black")

def parse_tags(tags: str):
    result = re.match("^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$", tags)
    if result is None:
        raise NoteAppError("Note was not added because of an error. Tags " \
        "should be comma separated list of strings containing only " \
        "letters and numbers.")
    return tags.split(",")

def print_notes(notes: list[NoteWithStatus]):
    table = Table(title="Your Notes")
    table.add_column("ID", width=6)
    table.add_column("Content", width=50)
    table.add_column("Status", width=16)
    table.add_column("Tags", style="violet", width=16)

    for note_with_status in notes:
        idx, note, status = note_with_status.idx, note_with_status.note, note_with_status.status
        tags = " ".join(f"#{tag}" for tag in note.tags) if note.tags else NO_TEXT
        status = Text(note.status, status.style) if note.status else NO_TEXT
        table.add_row(str(idx + 1), note.content, status, tags)
    
    print(table)

def print_tags(tags: list[str]):
    tags_list = " ".join(f"#{tag}" for tag in set(tags))
    tags_list = Text(tags_list, style="bold violet")
    print(tags_list)

def print_statuses(statuses: list[tuple[str, Status]]):
    for name, status in statuses:
        styled_status = Text(name, status.style)
        print(styled_status, " priority: ", status.priority)
