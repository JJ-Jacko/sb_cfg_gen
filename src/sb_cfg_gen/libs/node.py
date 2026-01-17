import copy
import json
from pathlib import Path
from typing import List
from typing import get_args

from sb_cfg_gen.libs.area import get_area_flag
from sb_cfg_gen.libs.area import get_area_keywords
from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.dicts import SingBoxConfig
from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.types import AreaCode
from sb_cfg_gen.libs.types import NodeType


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


def extra_nodes_from_singbox_config(
        config: SingBoxConfig
) -> List[Node]:
    nodes = []
    for outbound in config["outbounds"]:
        # 过滤 代理组
        if outbound["type"] not in get_args(NodeType):
            continue

        # 过滤 机场信息
        if keywords_in_text(airport_info_keywords, outbound["tag"]):
            continue
        
        nodes.append(outbound)
        
    return nodes


def node_in_nodes(node: Node, nodes: List[Node]):
    for exist_node in nodes:
        if (
            node["server"] == exist_node["server"]
            and node["server_port"] == exist_node["server_port"]
        ):
            return True

    return False


def deduplicate_nodes(nodes: List[Node]) -> List[Node | None]:
    cleaned_nodes = []
    for n in nodes:
        if node_in_nodes(n, cleaned_nodes):
            continue
        
        cleaned_nodes.append(n)

    return cleaned_nodes


def filter_nodes_with_specified_area(
        nodes: List[Node],
        area_code: AreaCode
) -> List[Node | None]:
    return [
        node
        for node in nodes
        if (
            keywords_in_text(get_area_keywords(area_code), node["tag"])
            or area_code in node["tag"]
        )
    ]


def rename_same_area_nodes(
        nodes: List[Node],
        area_code: AreaCode
) -> List[Node]:
    renamed_nodes = []
    
    for i, node in enumerate(nodes):
        new_node = copy.deepcopy(node)
        new_node["tag"] = f"{get_area_flag(area_code)} {area_code} {i + 1}"
        renamed_nodes.append(new_node)
    
    return renamed_nodes


def merge_singbox_config(
        nodes: List[Node],
        with_clash_api: bool = True,
        template_file: Path = Path("template.json")
):
    with template_file.open("r") as f:
        template: SingBoxConfig = json.load(f)
    
    # 总控制组
    template["outbounds"].append({
        "tag": "🚀 Proxy",
        "type": "selector",
        "outbounds": [
            "⚡ Direct", "🖐️ Manual",
            "🇭🇰 HK", "🇹🇼 TW", "🇸🇬 SG", "🇯🇵 JP", "🇺🇸 US"
        ]
    })
    
    # 禁广告组
    template["outbounds"].append({
        "tag": "📢 ADs",
        "type": "selector",
        "outbounds": ["🚀 Proxy", "🚫 Reject"]
    })
    
    # 手动组
    template["outbounds"].append({
        "tag": "🖐️ Manual",
        "type": "selector",
        "outbounds": [
            node["tag"]
            for node in nodes
        ]
    })

    # 地区组
    for area_code, tag in [
            ("HK", "🇭🇰 HK"), ("TW", "🇹🇼 TW"),
            ("SG", "🇸🇬 SG"), ("JP", "🇯🇵 JP"), ("US", "🇺🇸 US")
    ]:
        template["outbounds"].append({
            "tag": tag,
            "type": "selector",
            "outbounds": [
                node["tag"]
                for node in filter_nodes_with_specified_area(nodes, area_code)
            ]
        })
    
    # 节点
    template["outbounds"].extend(nodes)
    
    # 额外项目
    if with_clash_api:
        template["experimental"]["clash_api"] = {
            "external_controller": "0.0.0.0:9090",
            "external_ui": "dashboard"
        }
    
    return template

    