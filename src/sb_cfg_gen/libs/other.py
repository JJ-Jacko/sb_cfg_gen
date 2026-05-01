import json
import tomllib
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


def load_config(p: Path):
        
    with p.open("rb") as f:

        return  tomllib.load(f)


def load_json_file(file: str | Path):

    with open(file, "r") as f:
        return json.load(f)


def write_json_file(
        file: str | Path,
        data: dict,
        indent: int = 4
):

    with open(file, "w") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
