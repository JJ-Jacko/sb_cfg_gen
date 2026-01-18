from typing import get_args
from typing import List

from sb_cfg_gen.libs.config_factor import ConfigFactor
from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import write_json_file
from sb_cfg_gen.libs.types import AreaCode
from sb_cfg_gen.libs.web import url_get_singbox_config_file


def main():
    # Get urls
    url = input("url: ")
    
    # Get raw sing-box config
    raw_cfg = url_get_singbox_config_file(url)
        
    # Sava raw sing-box config
    write_json_file(f"cache/raw_cfg.json", raw_cfg)
    
    # Get nodes   
    nodes = ConfigFactor.extra_nodes_from_singbox_config(raw_cfg)
        
    # Deduplicate nodes
    nodes_deduplicated = NodeFactor.deduplicate_nodes(nodes)

    # Rename nodes
    nodes_renamed: List[Node] = []
    for area_code in get_args(AreaCode):
        nodes_filted_area = NodeFactor.filter_nodes_with_specified_area(nodes_deduplicated, area_code)
        nodes_filted_area_renamed = NodeFactor.rename_same_area_nodes(nodes_filted_area, area_code)
        nodes_renamed.extend(nodes_filted_area_renamed)

    # Merge new sing-box config
    final_cfg = ConfigFactor.merge_singbox_config(nodes_renamed)
    
    # Save sing-box config
    write_json_file("config.json", final_cfg)


if __name__ == "__main__":
    main()
