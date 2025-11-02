import json
from pathlib import Path

from sb_cfg_gen.libs.web import url_get_singbox_config_file
from sb_cfg_gen.libs.node import extra_nodes_from_singbox_config
from sb_cfg_gen.libs.node import deduplicate_nodes
from sb_cfg_gen.libs.node import filter_nodes_with_specified_area
from sb_cfg_gen.libs.node import rename_same_area_nodes
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

    # Filter nodes by area
    hk_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "HK")
    tw_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "TW")
    jp_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "JP")
    kr_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "KR")
    vn_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "VN")
    sg_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "SG")
    in_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "IN")
    au_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "AU")
    pl_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "PL")
    de_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "DE")
    gb_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "GB")
    us_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "US")
    ca_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "CA")
    aq_nodes = filter_nodes_with_specified_area(nodes_low_deduplicated, "AQ")
    
    HK_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "HK")
    TW_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "TW")
    JP_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "JP")
    KR_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "KR")
    VN_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "VN")
    SG_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "SG")
    IN_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "IN")
    AU_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "AU")
    PL_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "PL")
    DE_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "DE")
    GB_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "GB")
    US_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "US")
    CA_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "CA")
    AQ_nodes = filter_nodes_with_specified_area(nodes_high_deduplicated, "AQ")

    # Rename nodes based on region
    hk_nodes_renamed = rename_same_area_nodes(hk_nodes, "HK", "lower_case")
    tw_nodes_renamed = rename_same_area_nodes(tw_nodes, "TW", "lower_case")
    jp_nodes_renamed = rename_same_area_nodes(jp_nodes, "JP", "lower_case")
    kr_nodes_renamed = rename_same_area_nodes(kr_nodes, "KR", "lower_case")
    vn_nodes_renamed = rename_same_area_nodes(vn_nodes, "VN", "lower_case")
    sg_nodes_renamed = rename_same_area_nodes(sg_nodes, "SG", "lower_case")
    in_nodes_renamed = rename_same_area_nodes(in_nodes, "IN", "lower_case")
    au_nodes_renamed = rename_same_area_nodes(au_nodes, "AU", "lower_case")
    pl_nodes_renamed = rename_same_area_nodes(pl_nodes, "PL", "lower_case")
    de_nodes_renamed = rename_same_area_nodes(de_nodes, "DE", "lower_case")
    gb_nodes_renamed = rename_same_area_nodes(gb_nodes, "GB", "lower_case")
    us_nodes_renamed = rename_same_area_nodes(us_nodes, "US", "lower_case")
    ca_nodes_renamed = rename_same_area_nodes(ca_nodes, "CA", "lower_case")
    aq_nodes_renamed = rename_same_area_nodes(aq_nodes, "AQ", "lower_case")
    
    HK_nodes_renamed = rename_same_area_nodes(HK_nodes, "HK", "upper_case")
    TW_nodes_renamed = rename_same_area_nodes(TW_nodes, "TW", "upper_case")
    JP_nodes_renamed = rename_same_area_nodes(JP_nodes, "JP", "upper_case")
    KR_nodes_renamed = rename_same_area_nodes(KR_nodes, "KR", "upper_case")
    VN_nodes_renamed = rename_same_area_nodes(VN_nodes, "VN", "upper_case")
    SG_nodes_renamed = rename_same_area_nodes(SG_nodes, "SG", "upper_case")
    IN_nodes_renamed = rename_same_area_nodes(IN_nodes, "IN", "upper_case")
    AU_nodes_renamed = rename_same_area_nodes(AU_nodes, "AU", "upper_case")
    PL_nodes_renamed = rename_same_area_nodes(PL_nodes, "PL", "upper_case")
    DE_nodes_renamed = rename_same_area_nodes(DE_nodes, "DE", "upper_case")
    GB_nodes_renamed = rename_same_area_nodes(GB_nodes, "GB", "upper_case")
    US_nodes_renamed = rename_same_area_nodes(US_nodes, "US", "upper_case")
    CA_nodes_renamed = rename_same_area_nodes(CA_nodes, "CA", "upper_case")
    AQ_nodes_renamed = rename_same_area_nodes(AQ_nodes, "AQ", "upper_case")

    # Merge the final sing-box config
    config = merge_singbox_config(
        hq_HK_nodes=HK_nodes_renamed,
        hq_TW_nodes=TW_nodes_renamed,
        hq_SG_nodes=SG_nodes_renamed,
        hq_JP_nodes=JP_nodes_renamed,
        hq_US_nodes=US_nodes_renamed,
        hq_other_nodes= KR_nodes_renamed + VN_nodes_renamed + IN_nodes_renamed + \
            AU_nodes_renamed + \
            PL_nodes_renamed + DE_nodes_renamed + GB_nodes_renamed + \
            CA_nodes_renamed + \
            AQ_nodes_renamed,
        lq_HK_nodes=hk_nodes_renamed,
        lq_TW_nodes=tw_nodes_renamed,
        lq_SG_nodes=sg_nodes_renamed,
        lq_JP_nodes=jp_nodes_renamed,
        lq_US_nodes=us_nodes_renamed,
        lq_other_nodes= kr_nodes_renamed + vn_nodes_renamed + in_nodes_renamed + \
            au_nodes_renamed + \
            pl_nodes_renamed + de_nodes_renamed + gb_nodes_renamed + \
            ca_nodes_renamed + \
            aq_nodes_renamed
    )
    
    # Save sing-box config
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
