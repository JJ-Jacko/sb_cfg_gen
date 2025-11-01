import json
from typing import List
from pathlib import Path


def keywords_in_text(
        keywords: List[str],
        text: str
):
    for kw in keywords:
        if kw in text:
            return True
    
    return False
