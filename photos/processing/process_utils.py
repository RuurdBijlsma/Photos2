import re
from typing import Any


def readable_bytes(num: int, suffix: str = "B") -> str:
    fnum = float(num)
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(fnum) < 1024.0:
            return f"{fnum:3.1f}{unit}{suffix}"
        fnum /= 1024.0
    return f"{fnum:.1f}Yi{suffix}"


def remove_non_printable(input_string: str) -> str:
    # Use a regex to replace non-printable characters with an empty string
    return re.sub(r"[^\x20-\x7E\xA0-\uFFEF]", "", input_string)


def clean_object(obj: dict[str, Any]) -> dict[str, Any] | list[Any] | str:
    if isinstance(obj, dict):
        return {k: clean_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_object(v) for v in obj]
    elif isinstance(obj, str):
        return remove_non_printable(obj)  # Remove non-printable characters
    else:
        return obj
