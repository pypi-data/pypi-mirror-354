"""
Configuration commands for the note application.

This module defines commands to manage user-defined configuration options,
such as statuses. It includes subcommands for adding, editing, and deleting
custom statuses that can be associated with notes to support workflow or categorization.

Commands:
    status
"""
import typer
from typing_extensions import Annotated

from app.core.models import Status
from app.core.repository import create_status, edit_status, delete_status
from app.core.errors import NoteAppError

app = typer.Typer(
    help="Manage application configuration.",
    invoke_without_command=True,
    add_completion=True,
    add_help_option=True,
    no_args_is_help=True
)

@app.command()
def status(
    add: Annotated[
        str | None,
        typer.Option(
            "--add",
            "-a",
            help="Add STATUS to the application."
        )
    ] = None,
    edit: Annotated[
        str | None,
        typer.Option(
            "--edit",
            "-e",
            help="Edit STATUS in the application."
        )
    ] = None,
    delete: Annotated[
        str | None,
        typer.Option(
            "--delete",
            "-d",
            help="Delete STATUS from the application."
        )
    ] = None,
    style: Annotated[
        str | None,
        typer.Option(
            "--style",
            "-s",
            help="Provide status' style."
        )
    ] = None,
    priority: Annotated[
        int | None,
        typer.Option(
            "--priority",
            "-p",
            help="Provide status' priority."
        )
    ] = None
):
    """
    Manage statuses in the application. Use one of --add, --edit or --delete to
    add, edit or delete status.

    Use this command to create, edit and delete statuses in the appliaction.
    You must use exactly one of --add, --edit or --delete for this command to work.
    \n\n
    Status will be displayed according to style provided with --style STYLE 
    option. For available styles visit Rich's documentation at
    https://rich.readthedocs.io/en/stable/style.html. If no status is provided
    then white will be used. 
    \n\n
    Notes will be displayed in descending order of priority. Use --priority
    PRIORITY to set this value. If no priority is provided then 0 will be used.
    """
    
    options = [add, edit, delete]
    used = [opt for opt in options if opt is not None]

    if len(used) != 1:
        print("You must use exactly one of --add, --edit or --delete.")
        raise typer.Exit()
    
    try:
        if add:
            status = Status.create(style, priority)
            create_status(add, status)
        if edit:
            edit_status(edit, style, priority)
        if delete:
            delete_status(delete)
    except NoteAppError as error:
        print(error)
