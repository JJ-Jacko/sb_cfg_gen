import json
from pathlib import Path

from sb_cfg_gen.libs.web import url_get_singbox_config_file
from sb_cfg_gen.libs.node import extra_nodes_from_singbox_config
from sb_cfg_gen.libs.node import deduplicate_nodes
from sb_cfg_gen.libs.node import NodePool
from sb_cfg_gen.libs.node import merge_singbox_config
from sb_cfg_gen.libs.inputing import Input


def main():
    # Get urls
    low_urls = Input.texts("Low quality url: ")
    high_urls = Input.texts("High quality url: ")
    
    # Get raw sing-box config
    low_raws = [
        url_get_singbox_config_file(url)
        for url in low_urls
    ]
        
    high_raws = [
        url_get_singbox_config_file(url)
        for url in high_urls
    ]
        
    # Sava raw sing-box config
    cache = Path("cache")

    for i, raw in enumerate(low_raws):
        with (cache / f"low_{i + 1}.json").open("w") as f:
            json.dump(raw, f, indent=4, ensure_ascii=False)
            
    for i, raw in enumerate(high_raws):
        with (cache / f"high_{i + 1}.json").open("w") as f:
            json.dump(raw, f, indent=4, ensure_ascii=False)
    
    # Get nodes   
    nodes_low = []
    for raw in low_raws:
        nodes_low.extend(extra_nodes_from_singbox_config(raw))
        
    nodes_high =[]
    for raw in high_raws:
        nodes_high.extend(extra_nodes_from_singbox_config(raw))
    
    # Deduplicate nodes
    nodes_low_deduplicated = deduplicate_nodes(nodes_low)
    nodes_high_deduplicated = deduplicate_nodes(nodes_high)

    np = NodePool(
        low_nodes=nodes_low_deduplicated,
        high_nodes=nodes_high_deduplicated
    )

    # Merge the final sing-box config
    config = merge_singbox_config(
        hq_HK_nodes=np.get_nodes("high", "HK"),
        hq_TW_nodes=np.get_nodes("high", "TW"),
        hq_SG_nodes=np.get_nodes("high", "SG"),
        hq_JP_nodes=np.get_nodes("high", "JP"),
        hq_US_nodes=np.get_nodes("high", "US"),
        hq_other_nodes= np.get_nodes("high", "KR") + np.get_nodes("high", "VN") + np.get_nodes("high", "IN") + \
            np.get_nodes("high", "AU") + \
            np.get_nodes("high", "PL") + np.get_nodes("high", "DE") + np.get_nodes("high", "GB") + \
            np.get_nodes("high", "CA") + \
            np.get_nodes("high", "AQ"),
        lq_HK_nodes=np.get_nodes("low", "HK"),
        lq_TW_nodes=np.get_nodes("low", "TW"),
        lq_SG_nodes=np.get_nodes("low", "SG"),
        lq_JP_nodes=np.get_nodes("low", "JP"),
        lq_US_nodes=np.get_nodes("low", "US"),
        lq_other_nodes= np.get_nodes("low", "KR") + np.get_nodes("low", "VN") + np.get_nodes("low", "IN") + \
            np.get_nodes("low", "AU") + \
            np.get_nodes("low", "PL") + np.get_nodes("low", "DE") + np.get_nodes("low", "GB") + \
            np.get_nodes("low", "CA") + \
            np.get_nodes("low", "AQ")
    )
    
    # Save sing-box config
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
