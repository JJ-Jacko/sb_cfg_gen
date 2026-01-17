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
        if keywords_in_text(get_area_keywords(area_code), node["tag"])
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
        hq_HK_nodes: List[Node],
        hq_TW_nodes: List[Node],
        hq_SG_nodes: List[Node],
        hq_JP_nodes: List[Node],
        hq_US_nodes: List[Node],
        hq_other_nodes: List[Node],
        lq_HK_nodes: List[Node],
        lq_TW_nodes: List[Node],
        lq_SG_nodes: List[Node],
        lq_JP_nodes: List[Node],
        lq_US_nodes: List[Node],
        lq_other_nodes: List[Node],
        with_clash_api: bool = True,
        template_file: Path = Path("template.json")
):
    with template_file.open("r") as f:
        template: SingBoxConfig = json.load(f)
    
    if with_clash_api:
        template["experimental"]["clash_api"] = {
            "external_controller": "0.0.0.0:9090",
            "external_ui": "dashboard"
        }

    # 代理组
    template["outbounds"].extend([
        {
            "type": "selector",
            "tag": "🖐️ Manual",
            "outbounds": [
                n["tag"]
                for n in hq_HK_nodes + lq_HK_nodes + \
                        hq_TW_nodes + lq_TW_nodes + \
                        hq_SG_nodes + lq_SG_nodes + \
                        hq_JP_nodes + lq_JP_nodes + \
                        hq_US_nodes + lq_US_nodes + \
                        hq_other_nodes + lq_other_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "⚒️ DataSaver",
            "outbounds": [
                n["tag"]
                for n in lq_HK_nodes + lq_TW_nodes + \
                        lq_SG_nodes + lq_JP_nodes + \
                        lq_US_nodes + \
                        lq_other_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "🇭🇰 HK",
            "outbounds": [
                n["tag"]
                for n in hq_HK_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "🇹🇼 TW",
            "outbounds": [
                n["tag"]
                for n in hq_TW_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "🇸🇬 SG",
            "outbounds": [
                n["tag"]
                for n in hq_SG_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "🇯🇵 JP",
            "outbounds": [
                n["tag"]
                for n in hq_JP_nodes
            ]
        },
        {
            "type": "urltest",
            "tag": "🇺🇸 US",
            "outbounds": [
                n["tag"]
                for n in hq_US_nodes
            ]
        }
    ])

    # 节点
    template["outbounds"].extend([
        n
        for n in hq_HK_nodes + lq_HK_nodes + \
                hq_TW_nodes + lq_TW_nodes + \
                hq_SG_nodes + lq_SG_nodes + \
                hq_JP_nodes + lq_JP_nodes + \
                hq_US_nodes + lq_US_nodes + \
                hq_other_nodes + lq_other_nodes
    ])
    
    return template

    