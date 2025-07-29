import base64
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    filename: str
    content: str


def run_gpg(args: list[str], input_data: bytes) -> str:
    """Run GPG command with input and return output or raise an error."""
    proc = subprocess.run(args, input=input_data, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    return proc.stdout.decode()


def encrypt_input(input: bytes, recipients: list[str]) -> str:
    """Encrypt input using GPG"""
    args = ["gpg", "-aes"] + [f"-r {r}" for r in recipients]
    return run_gpg(args, input)


def encrypt_message(plaintext: str, recipients: list[str]) -> str:
    """Encrypt message using GPG"""
    return encrypt_input(plaintext.encode(), recipients)


def encrypt_file(filepath: Path, recipients: list[str]) -> str:
    """Encrypt file wrapped in json using GPG"""
    file_b64 = base64.b64encode(filepath.read_bytes()).decode("ascii")
    envelope = json.dumps(File(filepath.name, file_b64).__dict__)
    return encrypt_message(envelope, recipients)


def decrypt_message(ciphertext: str) -> str:
    """Decrypt message using GPG"""
    proc = subprocess.run(
        ["gpg", "-d"],
        input=ciphertext.encode(),
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    return proc.stdout.decode()


def decrypt_file_and_save(file: File) -> str:
    data = base64.b64decode(file.content)
    # Prompt use to ask where to save the file or not
    saved_path = file.filename
    _ = Path(saved_path).write_bytes(data)
    return saved_path


def recipient_exists(recipient: str) -> bool:
    """Making sure tha recipient exists using GPG"""
    try:
        proc = subprocess.run(
            ["gpg", "--list-keys", recipient],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(proc.stdout.strip())
    except subprocess.CalledProcessError:
        return False
