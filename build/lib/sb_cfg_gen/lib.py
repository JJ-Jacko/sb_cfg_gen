from sb_cfg_gen.key_path import KeyPath
from typing import List


def get_minecraft_instances() -> List[str | None]:
    instances = []
    
    for item_1 in KeyPath.VERSIONS.iterdir():
        if not item_1.is_dir():
            continue
        
        for item_2 in item_1.iterdir():
            if not item_2.is_file():
                continue

            if item_2.suffix != ".json":
                continue
            
            if item_2.stem != item_1.name:
                continue
            
            instances.append(item_2.stem)
            
    return instances

