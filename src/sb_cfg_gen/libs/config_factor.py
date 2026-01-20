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
        "未到期"
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
            
            # 过滤 节点本身带的 domain_resolver 键
            if outbound.get("domain_resolver", None):
                node_cleaned = copy.deepcopy(outbound)
                node_cleaned.pop("domain_resolver")
                nodes.append(node_cleaned)
            else:
                nodes.append(outbound)
            
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

        if with_clash_api:
            cls.__merge_clash_api_into_singbox_config(template)
        
        return template

        