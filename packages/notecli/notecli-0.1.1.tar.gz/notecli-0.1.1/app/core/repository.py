"""
Provides high-level operations on the note repository, such as creating the repository
and adding notes. This module separates core logic from low-level file storage operations.
"""
from copy import deepcopy

import typer

from app.core import storage
from app.core.models import Note, Status, NoteWithStatus
from app.core.errors import RepositoryCorruptedError, NotesNotFoundError, NoteAppError, StatusDoesNotExistError
from app.core.utils import print_notes, print_tags, print_statuses

class Repository:
    def __enter__(self):
        self.repository = storage.load_repository()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        storage.save_repository(self.repository)

    @property
    def _notes(self):
        if "notes" not in self.repository.keys():
            raise RepositoryCorruptedError("Notes repository does not contain field 'notes'.")
        return self.repository["notes"]
    
    @property
    def _statuses(self):
        if "config" not in self.repository.keys():
            raise RepositoryCorruptedError("Notes repository does not contain field 'config'.")
        
        if "statuses" not in self.repository["config"].keys():
            raise RepositoryCorruptedError("Notes repository configuration does not contain field 'statuses'.")
        
        return self.repository["config"]["statuses"]

    @property
    def _indexed_notes(self):
        return [
            NoteWithStatus(
                idx, 
                Note(**note), 
                Status(**self._statuses[note["status"]]) if note["status"] else Status.create()
            ) 
            for idx, note in enumerate(self._notes)
        ]

    @property
    def _notes_sorter(self):
        return lambda note_dict: 0 if note_dict["status"] is None else -self._statuses[note_dict["status"]]["priority"]

    @staticmethod
    def init_repository():
        """
        Initializes a new note repository by delegating to the storage layer.

        Returns:
            Path: The absolute path to the newly created repository file.
        """
        return storage.create_repository()

    def add_note(self, note: Note):
        """
        Adds a new note to the notes repository.

        This function loads the existing repository, verifies that it contains a
        'notes' field, appends the new note, and saves the updated repository 
        back to disk.

        Args:
            note (Note): The Note object to be added to the repository.

        Raises:
            RepositoryCorruptedError: If the loaded repository does not contain a 'notes' field,
                                    indicating it is improperly structured or corrupted.
            StatusDoesNotExistErrorl: If note is being created with non-existing status.
        """
        if note.status and note.status not in self._statuses.keys():
            raise StatusDoesNotExistError(f"There is no status {note.status} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")

        self._notes.append(note.to_dict())
        self._notes.sort(key=self._notes_sorter)

    def list_notes(self, tag_filter: list[str] | None = None):
        if not self._indexed_notes:
            raise NotesNotFoundError("Repository is empty. Run `note add` to add a note.")
        
        filtered_notes = deepcopy(self._indexed_notes)
        if tag_filter:
            filtered_notes = [inote for inote in filtered_notes if inote.note.tags and set(inote.note.tags) & set(tag_filter)]
            if not filtered_notes:
                filter_msg = ", ".join(tag_filter)
                raise NotesNotFoundError(f"There are no notes matching filter: '{filter_msg}' in repository.")
        
        print_notes(filtered_notes)

    def list_tags(self):
        tags = [note["tags"] for note in self._notes if note["tags"]]
        tags = [tag for group in tags for tag in group]
        if not tags:
            raise NotesNotFoundError("There are no tagged notes in the repository.")
        print_tags(tags)

    def list_statuses(self):
        statuses = [(name, Status.create(**status)) for name, status in self._statuses.items()]
        if not statuses:
            raise NoteAppError("There are no statuses in repository configuration. Run `note status --add` to create one.") # TODO test for that
        print_statuses(statuses)

    def delete_note(self, idx: int):
        if not 1 <= idx <= len(self._notes):
            raise NotesNotFoundError(f"There is no note with id {idx} in the repository. Run `note list` to see all notes.")
        self._notes.pop(idx - 1)

    def create_status(self, name: str, status: Status):
        if name in self._statuses.keys():
            raise NoteAppError(f"Status {name} already exists. Use `note config status -e` to edit statuses.")
        
        self._statuses[name] = {
            "style": status.style,
            "priority": status.priority
        } 
    
    def edit_status(self, name: str, style: str | None, priority: int | None):
        if name not in self._statuses.keys():
            raise StatusDoesNotExistError(f"There is no status {name} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")

        if style:
            self._statuses[name]["style"] = style

        if priority:
            self._statuses[name]["priority"] = priority

        self._notes.sort(key=self._notes_sorter)

    def delete_status(self, name: str):
        if name not in self._statuses.keys():
            raise StatusDoesNotExistError(f"There is no status {name} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")
        
        notes_with_status = [note for note in self._notes if note["status"] == name]

        if notes_with_status:
            confirmation = typer.confirm(f"There exist a note with status {name}, would you like to proceed? Note's status will be removed.")
            if not confirmation:
                return
            for note in notes_with_status:
                note["status"] = None
            self._notes.sort(key=self._notes_sorter)
        
        self._statuses.pop(name)
        # TODO add tests:
        # status deleted
        # ask for confirmation when note has status
        # status not deleted after No respond
        # notes sorted after removing status

def create_repository():
    return Repository.init_repository()

def add_note(note: Note):
    with Repository() as repo:
        repo.add_note(note)

def list_notes(tag_filter: list[str] | None = None):
    with Repository() as repo:
        repo.list_notes(tag_filter)

def list_tags():
    with Repository() as repo:
        repo.list_tags()

def list_statuses():
    with Repository() as repo:
        repo.list_statuses()

def delete_note(idx: int):
    with Repository() as repo:
        repo.delete_note(idx)

def create_status(name: str, status: Status):
    with Repository() as repo:
        repo.create_status(name, status)

def edit_status(name: str, style: str | None, priority: int | None):
    with Repository() as repo:
        repo.edit_status(name, style, priority)

def delete_status(name: str):
    with Repository() as repo:
        repo.delete_status(name)
