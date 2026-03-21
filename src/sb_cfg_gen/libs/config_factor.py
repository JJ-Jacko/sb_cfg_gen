import copy
import json
from pathlib import Path
from typing import get_args
from typing import List

from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.dicts import SingBoxConfig
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.types import NodeType


class ConfigFactor:
    airport_info_keywords: List[str] = [
        # KTM
        "剩余流量",
        "距离下次重置剩余",
        "套餐到期",
        
        # 流量光
        "剩余流量",
        "距离下次重置流量剩余",
        "未到期",
        
        # 快充云
        "过期时间",
        "官方地址",
        "备用地址"
    ]

    @classmethod
    def __merge_nodes_into_singbox_config(
            cls,
            nodes: List[Node],
            template: SingBoxConfig
    ):
        
        # 总控制组
        template["outbounds"].append({
            "tag": "🚀 Proxy",
            "type": "selector",
            "outbounds": [
                "⚡ Direct", "🖐️ Manual",
                "🇭🇰 HK", "🇹🇼 TW", "🇸🇬 SG", "🇯🇵 JP", "🇺🇸 US"
            ]
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

        # 禁广告组
        template["outbounds"].append({
            "tag": "📢 ADs",
            "type": "selector",
            "outbounds": ["🚀 Proxy", "🚫 Reject"]
        })

        # 地区组
        for area_code, tag in [
                ("HK", "🇭🇰 HK"), ("TW", "🇹🇼 TW"),
                ("SG", "🇸🇬 SG"), ("JP", "🇯🇵 JP"), ("US", "🇺🇸 US")
        ]:
            template["outbounds"].append({
                "tag": tag,
                "type": "urltest",
                "outbounds": [
                    node["tag"]
                    for node in NodeFactor.filter_nodes_with_specified_area(nodes, area_code)
                ]
            })
        
        # 节点
        template["outbounds"].extend(nodes)

    @classmethod
    def __merge_rule_sets_into_singbox_config(
            cls,
            template: SingBoxConfig,
            proxy: bool = True
    ):
        
        url_proxy = "https://gh-proxy.com"
        url_raw = "https://raw.githubusercontent.com/lyc8503/sing-box-rules/refs/heads"
        rule_sets_map = {
            # direct
            "geoip-private": "geoip",
            "geosite-geolocation-cn": "geosite",
            "geosite-cn": "geosite",
            "geoip-cn": "geoip",
            # proxy
            "geosite-geolocation-!cn": "geosite",
            # ads
            "geosite-category-ads-all": "geosite",
            # other
            "geosite-spotify": "geosite"
        }
        
        for rule_set, type in rule_sets_map.items():
            url = f"{url_raw}/rule-set-{type}/{rule_set}.srs"
            
            if proxy:
                url =  f"{url_proxy}/{url}"
    
            template["route"]["rule_set"].append({
                "tag": rule_set,
                "type": "remote",
                "format": "binary",
                "url": url
            })
            
    @classmethod
    def __merge_rules_into_singbox_config(
            cls,
            template: SingBoxConfig,
            block_ads: bool = True
    ):
        
        # block ads
        if block_ads:
            template["route"]["rules"].append({
                "rule_set": ["geosite-category-ads-all"],
                "outbound": "📢 ADs"
            })
        
        # dirct
        template["route"]["rules"].append({
            "rule_set": [
                "geoip-private",
                "geosite-geolocation-cn",
                "geosite-cn",
                "geoip-cn",
                # other
                "geosite-spotify"
            ],
            "outbound": "⚡ Direct"
        })
        
        # proxy
        template["route"]["rules"].append({
            "rule_set": ["geosite-geolocation-!cn"],
            "outbound": "🚀 Proxy"
        })
        
    @classmethod
    def __merge_clash_api_into_singbox_config(
            cls,
            template: SingBoxConfig,
            port: int = 9090
    ):
        template["experimental"]["clash_api"] = {
            "external_controller": f"0.0.0.0:{port}",
            "external_ui": "dashboard"
        }

    @classmethod
    def extra_nodes_from_singbox_config(
            cls,
            config: SingBoxConfig
    ) -> List[Node]:
        
        nodes = []
        for outbound in config["outbounds"]:
            # 过滤 代理组
            if outbound["type"] not in get_args(NodeType):
                continue

            # 过滤 机场信息
            if keywords_in_text(cls.airport_info_keywords, outbound["tag"]):
                continue
            
            node_cleaned = copy.deepcopy(outbound)
            
            # 去除 节点本身带的不需要的键
            for e in [
                "domain_resolver", "plugin",
                "plugin_opts", "network", "tcp_fast_open"
            ]:
                if e in node_cleaned:
                    node_cleaned.pop(e)

            nodes.append(node_cleaned)
            
        return nodes
    
    @classmethod
    def merge_singbox_config(
            cls,
            nodes: List[Node],
            with_clash_api: bool = True,
            template_file: Path = Path("template.json")
    ):
        
        with template_file.open("r") as f:
            template: SingBoxConfig = json.load(f)
        
        cls.__merge_nodes_into_singbox_config(nodes, template)
        cls.__merge_rule_sets_into_singbox_config(template)
        cls.__merge_rules_into_singbox_config(template)

        if with_clash_api:
            cls.__merge_clash_api_into_singbox_config(template)
        
        return template

        