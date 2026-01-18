import json
from pathlib import Path
from typing import List


def keywords_in_text(
        keywords: List[str],
        text: str
):
    for kw in keywords:
        if kw in text:
            return True
    
    return False


def write_json_file(
        file: str | Path,
        data: dict,
        indent: int = 4
):

    with open(file, "w") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
