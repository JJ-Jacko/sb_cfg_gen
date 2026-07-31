from pathlib import Path

from sb_cfg_gen.other import load_config


__all__ = [
    # Path Container
    "CACHE",
    "TEMPLATES",
    
    # Config
    "CONFIG"
]

# Path
CONFIG_FILE = Path("config.toml")

class CACHE:
    DIR = Path("cache")
    
    RAW_CFG = DIR / "raw_cfg.json"
    RAW_BASE64 = DIR / "raw_base64.txt"
    NODES = DIR / "nodes.json"
    NODES_DIY = DIR / "nodes_diy.json"
    
class TEMPLATES:
    DIR = Path("templates")
    
    CLIENT = DIR / "client.json"
    WEB_SCRAPER = DIR / "web_scraper.json"


# Initialization
CONFIG = load_config(CONFIG_FILE)
CACHE.DIR.mkdir(parents=True, exist_ok=True)
