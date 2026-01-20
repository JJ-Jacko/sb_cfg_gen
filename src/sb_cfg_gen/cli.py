from sb_cfg_gen.libs.config_factor import ConfigFactor
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import write_json_file
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

    # Organize and rename nodes
    nodes_organize_renamed = NodeFactor.organize_and_rename_nodes(nodes_deduplicated)

    # Merge new sing-box config
    final_cfg = ConfigFactor.merge_singbox_config(nodes_organize_renamed)
    
    # Save sing-box config
    write_json_file("config.json", final_cfg)


if __name__ == "__main__":
    main()
