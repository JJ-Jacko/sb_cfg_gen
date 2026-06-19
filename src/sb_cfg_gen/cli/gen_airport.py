from . import context
from sb_cfg_gen.factors.config_factor import ConfigFactor
from sb_cfg_gen.factors.node_factor import NodeFactor
from sb_cfg_gen.other import load_json_file
from sb_cfg_gen.other import write_json_file
from sb_cfg_gen.web import Web


def run():
    # raw_cfg = load_json_file(context.raw_cfg_file)
    
    # Get urls
    url = context.project_config["airport_url"]
    
    # Get raw sing-box config
    raw_cfg: dict = Web.singbox_config_file(url).json()
        
    # Sava raw sing-box config
    write_json_file(context.raw_cfg_file, raw_cfg)
    
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
    write_json_file(context.airport_app_file, final_cfg_app)
    write_json_file(context.airport_cli_file, final_cfg_cli)
    write_json_file(context.airport_server_file, final_cfg_server)
    