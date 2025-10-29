from dataclasses import dataclass
from typing import List


@dataclass
class Area:
    name: str
    flag: str
    keywords: List[str]