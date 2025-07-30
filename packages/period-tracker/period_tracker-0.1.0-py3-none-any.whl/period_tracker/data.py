import json
import os
from datetime import timedelta, date
from pathlib import Path
from typing import List, Dict
from period_tracker.crypto import encrypt_data_file, decrypt_data_file

if os.name == "nt":  # windows
    DATA_DIR = Path(os.getenv("LOCALAPPDATA")) / "period-tracker"
else:
    DATA_DIR = Path.home() / ".period-tracker"

DATA_FILE = DATA_DIR / "data.json"
ENCRYPTED_FILE = DATA_DIR / "data.json.gpg"


def get_data_file() -> Path:
    return ENCRYPTED_FILE


def set_data_file(path: Path) -> None:
    global DATA_FILE, ENCRYPTED_FILE
    ENCRYPTED_FILE = path
    DATA_FILE = path.with_suffix("")


def save_period(start_date: date, duration: int) -> None:
    """Save a new period entry with start and end dates."""
    entry = create_entry(start_date, duration)
    entries = load_entries()
    entries.append(entry)
    write_entries(entries)


def create_entry(start_date: date, duration: int) -> Dict[str, str]:
    """Create a period entry dictionary from start date and duration."""
    end_date = start_date + timedelta(days=duration - 1)
    return {
        "start": start_date.strftime("%Y-%m-%d"),
        "end": end_date.strftime("%Y-%m-%d"),
    }


def load_entries() -> List[Dict[str, str]]:
    """Load existing period entries from the data file."""
    if not ENCRYPTED_FILE.exists():
        return []

    decrypt_data_file(ENCRYPTED_FILE, DATA_FILE)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    DATA_FILE.unlink()
    return data


def write_entries(entries: List[Dict[str, str]]) -> None:
    """Write period entries to the data file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=4)

    encrypt_data_file(DATA_FILE)
