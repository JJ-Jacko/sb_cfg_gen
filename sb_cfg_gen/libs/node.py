import copy
from typing import List
from typing import Literal

from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.data import Area
from sb_cfg_gen.libs.dicts import SingBoxConfig
from sb_cfg_gen.libs.types import AreaCode


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


def extra_nodes_from_singbox_config(config: SingBoxConfig) -> List[dict]:
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
    for outbound in config["outbounds"]:
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


def get_area_flag(area_code: AreaCode):
    for area in areas:
        if area_code == area.area_code:
            return area.flag
    
    raise Exception(f"{area_code} 不存在")


def get_area_keywords(area_code: AreaCode):
    for area in areas:
        if area_code == area.area_code:
            return area.keywords
    
    raise Exception(f"{area_code} 不存在")


def filter_nodes_with_specified_area(
        nodes: List[dict],
        area_code: AreaCode
) -> List[dict | None]:
    return [
        node
        for node in nodes
        if keywords_in_text(get_area_keywords(area_code), node["tag"])
    ]


def rename_same_area_nodes(
        nodes: List[dict],
        area_code: AreaCode,
        area_name_mode: Literal["upper_case", "lower_case"] = "upper_case"
):
    renamed_nodes = []
    
    for i, node in enumerate(nodes):
        new_node = copy.deepcopy(node)
        match area_name_mode:
            case "upper_case":
                new_node["tag"] = f"{get_area_flag(area_code)} {area_code.upper()} {i + 1}"
            case "lower_case":
                new_node["tag"] = f"{get_area_flag(area_code)} {area_code.lower()} {i + 1}"
        
        renamed_nodes.append(new_node)
    
    return renamed_nodes

