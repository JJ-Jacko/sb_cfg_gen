import json
from pathlib import Path
from typing import get_args
from typing import List

from sb_cfg_gen.libs.areas import Areas
from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.dicts import SingBoxConfig
from sb_cfg_gen.libs.node_factor import NodeFactor
from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.types import NodeType
from sb_cfg_gen.libs.types import AreaCode


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
            buildin_area_codes: List[AreaCode],
            template: SingBoxConfig,
            extra_area: bool = False
    ):
        
        if extra_area:
            nodes_output = nodes
        else:
            nodes_output = [
                node
                for area_code in buildin_area_codes
                for node in NodeFactor.filter_nodes_with_specified_area(nodes, area_code)
            ]
        
        # 总控制组
        template["outbounds"].append({
            "tag": "🚀 Proxy",
            "type": "selector",
            "outbounds": (
                ["⚡ Direct", "🖐️ Manual"] +
                [
                    f"{Areas.get(area_code).flag} {area_code}"
                    for area_code in buildin_area_codes
                ]
            )
        })
        
        # 手动组
        template["outbounds"].append({
            "tag": "🖐️ Manual",
            "type": "selector",
            "outbounds": [
                node["tag"]
                for node in nodes_output
            ]
        })

        # 地区组
        for area_code in buildin_area_codes:
            template["outbounds"].append({
                "tag": f"{Areas.get(area_code).flag} {area_code}",
                "type": "urltest",
                "outbounds": [
                    node["tag"]
                    for node in NodeFactor.filter_nodes_with_specified_area(nodes, area_code)
                ]
            })
        
        # 节点
        template["outbounds"].extend(nodes_output)
        
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
        
        nodes: List[Node] = []
        
        for outbound in config["outbounds"]:
            # 过滤 代理组
            if outbound["type"] not in get_args(NodeType):
                continue

            # 过滤 机场信息
            if keywords_in_text(cls.airport_info_keywords, outbound["tag"]):
                continue
            
            # 保留 节点必须的键值
            node_cleaned: Node = dict()
            for k in ["tag", "type", "server", "server_port", "method", "password"]:
                if k in outbound:
                    node_cleaned[k] = outbound[k]
            
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
        
        cls.__merge_nodes_into_singbox_config(
            nodes,
            ["HK", "TW", "SG", "JP", "US"],
            template
        )

        if with_clash_api:
            cls.__merge_clash_api_into_singbox_config(template)
        
        return template

        