import subprocess
from pathlib import Path
from period_tracker.config import get_gpg_recipient


def encrypt_data_file(input_path: Path) -> None:
    output_path = input_path.with_suffix(input_path.suffix + ".gpg")
    recipient = get_gpg_recipient()
    subprocess.run(
        [
            "gpg",
            "--yes",
            "--batch",
            "-o",
            str(output_path),
            "-r",
            recipient,
            "-e",
            str(input_path),
        ],
        check=True,
    )
    input_path.unlink()


def decrypt_data_file(input_path: Path, output_path: Path) -> None:
    subprocess.run(
        ["gpg", "--yes", "--batch", "-o", str(output_path), "-d", str(input_path)],
        check=True,
    )
