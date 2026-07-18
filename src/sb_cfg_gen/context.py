from pathlib import Path

from sb_cfg_gen.other import load_config


__all__ = [
    # Path
    "f_project_config",
    "f_raw_cfg",
    "f_raw_base64",
    "f_nodes",
    "f_nodes_diy",
    "f_template_client",
    "f_template_web_scraper"
]

# Path
d_cache = Path("cache")
d_template = Path("templates")

f_project_config = Path("config.toml")
f_raw_cfg = d_cache / "raw_cfg.json"
f_raw_base64 = d_cache / "raw_base64.txt"
f_nodes = d_cache / "nodes.json"
f_nodes_diy = d_cache / "nodes_diy.json"
f_template_client = d_template / "client.json"
f_template_web_scraper = d_template / "web_scraper.json"

# Initialization
project_config = load_config(f_project_config)
d_cache.mkdir(parents=True, exist_ok=True)
