from pathlib import Path

from sb_cfg_gen.other import load_config


__all__ = [
    # Path
    "project_config_file",
    "raw_cfg_file",
    "nodes_file",
    "nodes_diy_file"
]

# Path
project_config_file = Path("config.toml")
cache_dir = Path("cache")
raw_cfg_file = cache_dir/"raw_cfg.json"
nodes_file = cache_dir/"nodes.json"
nodes_diy_file = cache_dir/"nodes_diy.json"

# Initialization
project_config = load_config(project_config_file)
cache_dir.mkdir(parents=True, exist_ok=True)
