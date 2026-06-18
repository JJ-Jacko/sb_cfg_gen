from typing import List

from . import context
from sb_cfg_gen.dicts import Node
from sb_cfg_gen.factors.config_factor import ConfigFactor
from sb_cfg_gen.libs.other import write_json_file
from sb_cfg_gen.libs.other import load_json_file


def run():
    nodes: List[Node] = load_json_file(context.nodes_file)
    
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
    write_json_file(context.diy_app_file, final_cfg_app)
    write_json_file(context.diy_cli_file, final_cfg_cli)
    write_json_file(context.diy_server_file, final_cfg_server)
    