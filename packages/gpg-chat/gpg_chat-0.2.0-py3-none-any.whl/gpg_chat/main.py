import json
import subprocess
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Annotated, ClassVar, final, override

import pyperclip
import typer
from click import echo
from click.exceptions import Exit
from rich import print
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.types import CSSPathType
from textual.widgets import Button, Footer, Header, RichLog, TextArea
from typer.params import Option

from .gpg_utils import (
    File,
    decrypt_file_and_save,
    decrypt_message,
    encrypt_file,
    encrypt_message,
    recipient_exists,
)

try:
    __version__ = version("gpg-chat")
except PackageNotFoundError:
    __version__ = "ersion unknown"

CONVO_FILE = Path("conversation.txt")


### Textual part


@final
class ChatApp(App[None]):
    """Modern chat-style GPG encryption/decryption application"""

    CSS_PATH: ClassVar[CSSPathType | None] = "app.css"
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("ctrl+e", "encrypt", "Encrypt", priority=True),
        Binding("ctrl+d", "decrypt", "Decrypt", priority=True),
        Binding("ctrl+l", "clear_input", "Clear Input", priority=True),
    ]

    convo_log = reactive("")

    def __init__(self, recipients: list[str]):
        super().__init__()
        self.recipients = recipients

    @override
    def compose(self) -> ComposeResult:
        """Create the application UI"""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            # Conversation panel
            with VerticalScroll(id="convo-panel"):
                yield RichLog(id="convo-log", wrap=True, markup=True)

            # Input/Output panel
            with Vertical(id="io-panel"):
                yield TextArea("", id="input-box", language="markdown")
                with Horizontal(id="button-panel"):
                    yield Button("Encrypt", id="encrypt-btn", variant="success")
                    yield Button("Decrypt", id="decrypt-btn", variant="warning")
                    yield Button("Clear", id="clear-btn", variant="error")
                    yield Button("Attach File", id="attach-btn", variant="primary")

        yield Footer()

    def on_mount(self) -> None:
        """Load existing conversation when app starts"""
        self.title = "Secure GPG Messenger"
        self.sub_title = f"Recipients: {', '.join(self.recipients)}"
        _ = self.query_one("#input-box", TextArea).focus()
        self.theme = "gruvbox"

        if CONVO_FILE.exists():
            _ = self.query_one("#convo-log", RichLog).write(CONVO_FILE.read_text())

    def add_to_convo_log(self, role: str, message: str) -> None:
        """Add a message to the conversation log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = (
            rf"[b cyan]\[{timestamp}] You:[/] {message}"
            if role == "me"
            else rf"[b yellow]\[{timestamp}] Other:[/] {message}"
        )

        with CONVO_FILE.open("a") as f:
            _ = f.write(line + "\n")

        log = self.query_one("#convo-log", RichLog).write(line)
        log.scroll_end(animate=False)

    def action_encrypt(self) -> None:
        """Encrypt the current message"""
        self.on_button_pressed(Button.Pressed(self.query_one("#encrypt-btn", Button)))

    def action_decrypt(self) -> None:
        """Decrypt the current message"""
        self.on_button_pressed(Button.Pressed(self.query_one("#decrypt-btn", Button)))

    def action_clear_input(self) -> None:
        """Clear the input field"""
        self.query_one("#input-box", TextArea).focus().text = ""

    def try_parse_envelope(self, decrypted_text: str) -> File | None:
        try:
            data = json.loads(decrypted_text)
            if isinstance(data, dict) and "filename" in data:
                return File(**data)
        except Exception:
            return None

    def prompt_file_path(self) -> Path | None:
        try:
            proc = subprocess.run(["zenity", "--file-selection"], capture_output=True, text=True)
            if proc.returncode == 0:
                return Path(proc.stdout.strip())
        except FileNotFoundError:
            self.notify("File not found", title="Operation Failed", severity="error")
        return None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button click events"""
        input_box = self.query_one("#input-box", TextArea)
        text = input_box.text.strip()

        try:
            if event.button.id == "encrypt-btn":
                encrypted = encrypt_message(text, self.recipients)
                pyperclip.copy(encrypted)
                self.add_to_convo_log("me", text)
                self.notify("Encrypted & copied to clipboard!", title="Success")
                input_box.text = ""
                return

            if event.button.id == "decrypt-btn":
                decrypted = decrypt_message(text)
                envelope = self.try_parse_envelope(decrypted)
                if envelope:
                    saved_path = decrypt_file_and_save(envelope)
                    self.add_to_convo_log("other", f"[u]Decrypted file saved as '{saved_path}'[/]")
                    self.notify(f"File '{envelope.filename}' decrypted and saved!", title="Success")
                    input_box.text = ""
                    return

                self.add_to_convo_log("other", decrypted)
                self.notify("Message decrypted!", title="Success")
                input_box.text = ""
                return

            if event.button.id == "attach-btn":
                file_path = self.prompt_file_path()
                if file_path:
                    encrypted = encrypt_file(file_path, self.recipients)
                    pyperclip.copy(encrypted)
                    self.add_to_convo_log("me", f"[u]Encrypted file '{file_path.name}' attached[/]")
                    self.notify("File encrypted & copied to clipboard!", title="Success")
                return

            if event.button.id == "clear-btn":
                input_box.focus().text = ""
                return

        except Exception as e:
            self.notify(f"Error: {str(e)}", title="Operation Failed", severity="error")


### Typer part


app = typer.Typer()


def version_callback(value: bool):
    if value:
        echo(f"GPG Chat v{__version__}")
        raise Exit()


def validate_recipients(recipients: list[str]):
    for recipient in recipients:
        if not recipient_exists(recipient):
            print(f"[b red]Error:[/] GPG Key for recipient '{recipient}' not found")
            print("[yellow]Tip:[/] Import the recipient’s public key using:")
            print("  [cyan]gpg --import <recipient-public-key>.asc[/]")
            raise Exit()


@app.command()
def chat(
    recipients: Annotated[
        list[str],
        Option(
            ...,
            "--recipient",
            "-r",
            help="One or more GPG recipient username or email",
        ),
    ],
    version: Annotated[
        bool, Option("--version", "-v", callback=version_callback, help="Show version and exit")
    ] = False,
):
    """Start the secure messaging application"""
    validate_recipients(recipients)
    ChatApp(recipients).run()


if __name__ == "__main__":
    app()
