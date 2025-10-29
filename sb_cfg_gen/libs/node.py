from typing import List
from typing import Literal

from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.data import Area


areas = [
    # 亚洲
    Area("HK", "🇭🇰", ["香港", "Hong Kong"]),
    Area("TW", "🇹🇼", ["台湾", "Taiwan"]),
    Area("JP", "🇯🇵", ["日本", "Japan"]),
    Area("KR", "🇰🇷", ["韩国", "Korea", "South Korea"]),
    Area("VN", "🇻🇳", ["越南", "Vietnam"]),
    Area("SG", "🇸🇬", ["新加坡", "Singapore"]),
    Area("IN", "🇮🇳", ["印度", "India"]),
    # 大洋洲
    Area("AU", "🇦🇺", ["澳大利亚", "澳洲", "Australia"]),
    # 欧洲
    Area("PL", "🇵🇱", ["波兰", "Poland"]),
    Area("DE", "🇩🇪", ["德国", "Germany"]),
    Area("GB", "🇬🇧", ["英国", "United Kingdom"]),
    # 北美洲
    Area("US", "🇺🇸", ["美国", "United States"]),
    Area("CA", "🇨🇦", ["加拿大", "Canada"])
]


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


def get_area_flag(name: str):
    for area in areas:
        if name == area.name:
            return area.flag
    
    raise Exception(f"{name} 不存在")


def get_area_keywords(name: str):
    for area in areas:
        if name == area.name:
            return area.keywords
    
    raise Exception(f"{name} 不存在")


def filter_nodes_with_specified_area(
        nodes: List[dict],
        area_name: Literal[
            "HK", "TW", "JP", "KR", "VN", "SG", "IN",
            "AU",
            "PL", "DE", "GB",
            "US", "CA"
        ]
) -> List[dict | None]:
    return [
        node
        for node in nodes
        if keywords_in_text(get_area_keywords(area_name), node["tag"])
    ]
