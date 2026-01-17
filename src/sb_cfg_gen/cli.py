from sb_cfg_gen.libs.web import url_get_singbox_config_file
from sb_cfg_gen.libs.node import extra_nodes_from_singbox_config
from sb_cfg_gen.libs.node import deduplicate_nodes
from sb_cfg_gen.libs.other import write_json_file


def main():
    # Get urls
    url = input("url: ")
    
    # Get raw sing-box config
    raw_cfg = url_get_singbox_config_file(url)
        
    # Sava raw sing-box config
    write_json_file(f"cache/raw_cfg.json")
    
    # Get nodes   
    nodes = extra_nodes_from_singbox_config(raw_cfg)
        
    # Deduplicate nodes
    nodes_deduplicated = deduplicate_nodes(nodes)

    # Rename nodes
    
    # Merge new sing-box config
    
    # Save sing-box config
    write_json_file("config.json", config)


if __name__ == "__main__":
    main()
