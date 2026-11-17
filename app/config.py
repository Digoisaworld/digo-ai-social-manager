import os
from dotenv import load_dotenv
load_dotenv()

def get(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

def required(*names: str) -> None:
    missing = [name for name in names if not get(name)]
    if missing:
        raise RuntimeError("Missing environment settings: " + ", ".join(missing))
