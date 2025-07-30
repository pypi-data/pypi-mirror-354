from dataclasses import dataclass, asdict

@dataclass
class Note:
    content: str
    tags: list[str] | None
    status: str | None

    @staticmethod
    def create(content: str, tags: list[str] | None = None, status: str | None = None):
        return Note(content, tags, status)

    def to_dict(self):
        return asdict(self)

@dataclass
class Status:
    style: str
    priority: int

    @staticmethod
    def create(style: str | None = None, priority: int | None = None):
        style = style if style else "white"
        priority = priority if priority else 0
        return Status(style, priority)

@dataclass
class NoteWithStatus:
    idx: int
    note: Note
    status: Status
