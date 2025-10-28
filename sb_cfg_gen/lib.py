import json
from typing import List
from pathlib import Path


def found_same_node(node, nodes: list):
    for exist_node in nodes:
        if (
            node["server"] == exist_node["server"]
            and node["server_port"] == exist_node["server_port"]
        ):
            return True

    return False


def patch_config_file(
        raw: dict,
        template_file: Path = Path("template.json")
):
    hk_nodes = []
    us_nodes = []
    sg_nodes = []
    tw_nodes = []
    jp_nodes = []
    other_nodes = []
    
    with template_file.open("r") as f:
        template = json.load(f)

    # 提取节点
    for outbound in raw["outbounds"]:
        if outbound["type"] not in ["shadowsocks", "vless", "vmess", "hysteria2"]:
            continue

        tag = outbound["tag"]

        # 获取剩余流量
        if "剩余流量" in tag:
            flow = tag[5:]
            continue

        # 获取到期时间
        if "套餐到期" in tag:
            expiration_time = tag[5:]
            continue
        elif "未到期" in tag:
            expiration_time = tag[4:]
            continue

        # 跳过重复
        if found_same_node(
            outbound,
            hk_nodes + us_nodes + sg_nodes +
            tw_nodes + jp_nodes + other_nodes
        ):
            continue

        # 按地区分类
        if "香港" in tag:
            hk_nodes.append(outbound)
        elif "美国" in tag:
            us_nodes.append(outbound)
        elif "新加坡" in tag:
            sg_nodes.append(outbound)
        elif "台湾" in tag:
            tw_nodes.append(outbound)
        elif "日本" in tag:
            jp_nodes.append(outbound)
        else:
            other_nodes.append(outbound)

    nodes = hk_nodes + us_nodes + sg_nodes + tw_nodes + jp_nodes + other_nodes

    outbounds: List[dict] = template["outbounds"]
    outbounds.append({
        "type": "selector",
        "tag": "🚀 节点选择",
        "outbounds": [
            "🎯 全部节点",
            "🇭🇰 香港",
            "🇺🇸 美国",
            "🇸🇬 新加坡",
            "🇹🇼 台湾",
            "🇯🇵 日本",
            "🌐 其他国家"
        ]
    })    
    outbounds.append({
        "type": "urltest",
        "tag": "🎯 全部节点",
        "outbounds": [
            node["tag"]
            for node in nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🇭🇰 香港",
        "outbounds": [
            n["tag"]
            for n in hk_nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🇺🇸 美国",
        "outbounds": [
            n["tag"]
            for n in us_nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🇸🇬 新加坡",
        "outbounds": [
            n["tag"]
            for n in sg_nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🇹🇼 台湾",
        "outbounds": [
            n["tag"]
            for n in tw_nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🇯🇵 日本",
        "outbounds": [
            n["tag"]
            for n in jp_nodes
        ]
    })
    outbounds.append({
        "type": "urltest",
        "tag": "🌐 其他国家",
        "outbounds": [
            n["tag"]
            for n in other_nodes
        ]
    })
    for node in nodes:
        outbounds.append(node)
        
    return template