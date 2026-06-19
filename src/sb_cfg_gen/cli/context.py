from pathlib import Path

from sb_cfg_gen.other import load_config


__all__ = [
    # Path
    "nodes_file",
    "raw_cfg_file",
    "airport_app_file",
    "airport_cli_file",
    "airport_server_file",
    "diy_app_file",
    "diy_cli_file",
    "diy_server_file"
]

# Path
project_config_file = Path("config.toml")
nodes_file = Path("nodes.json")
cache_dir = Path("cache")
output_dir = Path("output")
raw_cfg_file = cache_dir/"raw_cfg.json"
airport_app_file = output_dir/"airport-app.json"
airport_cli_file = output_dir/"airport-cli.json"
airport_server_file = output_dir/"airport-server.json"
diy_app_file = output_dir/"diy-app.json"
diy_cli_file = output_dir/"diy-cli.json"
diy_server_file = output_dir/"diy-server.json"

# Initialization
project_config = load_config(project_config_file)
cache_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)
