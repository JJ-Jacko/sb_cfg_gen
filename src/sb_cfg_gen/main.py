import uvicorn
from pathlib import Path

from sb_cfg_gen.libs.config_factor import ConfigFactor
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import write_json_file
from sb_cfg_gen.libs.other import load_json_file
from sb_cfg_gen.libs.other import load_config
from sb_cfg_gen.libs.web import Web


project_config_file = Path("config.toml")
nodes_file = Path("nodes.json")
cache_dir = Path("cache")
output_dir = Path("output")
raw_cfg_file = cache_dir / "raw_cfg.json"
airport_app_file = output_dir / "airport-app.json"
airport_cli_file = output_dir / "airport-cli.json"
airport_server_file = output_dir / "airport-server.json"
diy_app_file = output_dir / "diy-app.json"
diy_cli_file = output_dir / "diy-cli.json"
diy_server_file = output_dir / "diy-server.json"


def _init():
    cache_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)


def gen_airport():
    # raw_cfg = load_json_file(raw_cfg_file)
    
    # Get urls
    url = project_config["airport_url"]
    
    # Get raw sing-box config
    raw_cfg: dict = Web.singbox_config_file(url).json()
        
    # Sava raw sing-box config
    write_json_file(raw_cfg_file, raw_cfg)
    
    # Get nodes   
    nodes = ConfigFactor.extra_nodes_from_singbox_config(raw_cfg)
        
    # Deduplicate nodes
    nodes_deduplicated = NodeFactor.deduplicate_nodes(nodes)

    # Organize and rename nodes
    nodes_organize_renamed = NodeFactor.organize_and_rename_nodes(nodes_deduplicated)

    # Merge new sing-box config
    final_cfg_app = ConfigFactor.merge_singbox_config(
        nodes_organize_renamed,
        inbound_mixd_in=False,
        inbound_tun_in=True,
        with_clash_api=False,
        type="airport"
    )
    final_cfg_cli = ConfigFactor.merge_singbox_config(
        nodes_organize_renamed,
        inbound_mixd_in=False,
        inbound_tun_in=True,
        with_clash_api=True,
        type="airport"
    )
    final_cfg_server = ConfigFactor.merge_singbox_config(
        nodes_organize_renamed, 
        inbound_mixd_in=True,
        inbound_tun_in=True,
        with_clash_api=True,
        type="airport",
        clash_api_path="/var/www/clash_api"
    )
    
    # Save sing-box config
    write_json_file(airport_app_file, final_cfg_app)
    write_json_file(airport_cli_file, final_cfg_cli)
    write_json_file(airport_server_file, final_cfg_server)


def gen_diy():
    nodes = load_json_file(nodes_file)["nodes"]
    
    # Merge new sing-box config
    final_cfg_app = ConfigFactor.merge_singbox_config(
        nodes,
        inbound_mixd_in=False,
        inbound_tun_in=True,
        with_clash_api=False,
        type="diy"
    )
    final_cfg_cli = ConfigFactor.merge_singbox_config(
        nodes,
        inbound_mixd_in=False,
        inbound_tun_in=True,
        with_clash_api=True,
        type="diy"
    )
    final_cfg_server = ConfigFactor.merge_singbox_config(
        nodes, 
        inbound_mixd_in=True,
        inbound_tun_in=True,
        with_clash_api=True,
        type="diy",
        clash_api_path="/var/www/clash_api"
    )
    
    # Save sing-box config
    write_json_file(diy_app_file, final_cfg_app)
    write_json_file(diy_cli_file, final_cfg_cli)
    write_json_file(diy_server_file, final_cfg_server)


def web_api():
    uvicorn.run(
        "sb_cfg_gen.app:app",
        host="0.0.0.0",
        port=9988,
        reload=False
    )


def test():
    pass


_init()
project_config = load_config(project_config_file)


if __name__ == "__main__":
    # gen_airport()
    # gen_diy()
    # web_api()
    # test()
    
    pass
