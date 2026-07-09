from pathlib import Path

from sb_cfg_gen.other import load_config


__all__ = [
    # Path
    "project_config_p",
    "raw_cfg_p",
    "nodes_p",
    "nodes_diy_p"
]

# Path
project_config_p = Path("config.toml")
cache_p = Path("cache")
template_p = Path("templates")
raw_cfg_p = cache_p/"raw_cfg.json"
nodes_p = cache_p/"nodes.json"
nodes_diy_p = cache_p/"nodes_diy.json"
template_client_p = template_p/"client.json"
template_web_scraper_p = template_p/"web_scraper.json"

# Initialization
project_config = load_config(project_config_p)
cache_p.mkdir(parents=True, exist_ok=True)
