from sb_cfg_gen.libs.config_factor import ConfigFactor
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import write_json_file
from sb_cfg_gen.libs.other import load_json_file
from sb_cfg_gen.libs.web import Web


def gen_airport():
    # raw_cfg = load_json_file("cache/raw_cfg.json")
    
    # Get urls
    url = input("url: ")
    
    # Get raw sing-box config
    raw_cfg: dict = Web.singbox_config_file(url).json()
        
    # Sava raw sing-box config
    write_json_file(f"cache/raw_cfg.json", raw_cfg)
    
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
    write_json_file("output/airport-app.json", final_cfg_app)
    write_json_file("output/airport-cli.json", final_cfg_cli)
    write_json_file("output/airport-server.json", final_cfg_server)


def gen_diy():
    nodes = load_json_file("nodes.json")["nodes"]
    
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
    write_json_file("output/diy-app.json", final_cfg_app)
    write_json_file("output/diy-cli.json", final_cfg_cli)
    write_json_file("output/diy-server.json", final_cfg_server)


def test():
    pass


if __name__ == "__main__":
    # gen_airport()
    # gen_diy()
    # test()
    
    pass
