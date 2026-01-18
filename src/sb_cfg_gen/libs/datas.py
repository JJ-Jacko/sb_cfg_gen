from dataclasses import dataclass
from typing import List

from sb_cfg_gen.libs.types import AreaCode


@dataclass
class Area:
    area_code: AreaCode
    flag: str
    keywords: List[str]
