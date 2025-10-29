from typing import List
from typing import Literal

from sb_cfg_gen.libs.other import keywords_in_text


node_tag_keywords = {
    "HK": ["香港", "Hong Kong"],
    "TW": ["台湾", "Taiwan"],
    "SG": ["新加坡", "Singapore"],
    "JP": ["日本", "Japan"],
    "US": ["美国", "United States"],
    "Other": [""]
}


def extra_nodes_from_singbox_config(singbox_config: dict) -> List[dict]:
    node_types = [
        "hysteria2",
        "shadowsocks",
        "vless",
        "vmess",
    ]
    airport_info_keywords = [
        # KTM
        "剩余流量",
        "距离下次重置剩余",
        "套餐到期",
        
        # 流量光
        "剩余流量",
        "距离下次重置流量剩余",
        "未到期"
    ]
    
    nodes = []
    for outbound in singbox_config["outbounds"]:
        # 过滤 代理组
        if outbound["type"] not in node_types:
            continue

        # 过滤 机场信息
        if keywords_in_text(airport_info_keywords, outbound["tag"]):
            continue
        
        nodes.append(outbound)
        
    return nodes


def node_in_nodes(node: dict, nodes: List[dict]):
    for exist_node in nodes:
        if (
            node["server"] == exist_node["server"]
            and node["server_port"] == exist_node["server_port"]
        ):
            return True

    return False


def deduplicate_nodes(nodes: List[dict]) -> List[dict | None]:
    cleaned_nodes = []
    for n in nodes:
        if node_in_nodes(n, cleaned_nodes):
            continue
        
        cleaned_nodes.append(n)

    return cleaned_nodes


def filter_nodes_with_specified_area(
        nodes: List[dict],
        area: Literal["HK", "TW", "SG", "JP", "US", "Other"]
) -> List[dict | None]:
    if area == "Other":
        return [
            node
            for node in nodes
            if not keywords_in_text(node_tag_keywords.get("HK"), node["tag"])
            if not keywords_in_text(node_tag_keywords.get("TW"), node["tag"])
            if not keywords_in_text(node_tag_keywords.get("SG"), node["tag"])
            if not keywords_in_text(node_tag_keywords.get("JP"), node["tag"])
            if not keywords_in_text(node_tag_keywords.get("US"), node["tag"])
        ]
    
    return [
        node
        for node in nodes
        if keywords_in_text(node_tag_keywords.get(area), node["tag"])
    ]
