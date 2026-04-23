import copy
import json
from pathlib import Path
from typing import get_args
from typing import List
from typing import Literal

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
    def __merge_nodes_into_singbox_config_no_area_group(
            cls,
            nodes: List[Node],
            template: SingBoxConfig
    ):
        
        # 总控制组
        template["outbounds"].append({
            "tag": "🚀 Proxy",
            "type": "selector",
            "outbounds": [
                node["tag"]
                for node in nodes
            ]
        })

        # 节点
        template["outbounds"].extend(nodes)
        
    @classmethod
    def __merge_clash_api_into_singbox_config(
            cls,
            template: SingBoxConfig,
            port: int = 9090,
            clash_api_path: str = "dashboard"
    ):
        template["experimental"]["clash_api"] = {
            "external_controller": f"0.0.0.0:{port}",
            "external_ui": clash_api_path
        }

    @classmethod
    def __merge_inbounds_into_singbox_config(
            cls,
            template: SingBoxConfig,
            mixed_in: bool = True,
            mixed_in_port: int = 8848,
            tun_in: bool = True
    ):

        if mixed_in:
            template["inbounds"].append({
                "tag": "mixed-in",
                "type": "mixed",
                "listen": "0.0.0.0",
                "listen_port": mixed_in_port
            })
            template["route"]["rules"][0]["inbound"].append("mixed-in")
        if tun_in:
            template["inbounds"].append({
                "tag": "tun-in",
                "type": "tun",
                "address": "172.19.0.1/30",
                "auto_route": True,
                "strict_route": True,
                "stack": "mixed"
            })
            template["route"]["rules"][0]["inbound"].append("tun-in")

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
            
            # 调整 不同类型的节点键值顺序
            match outbound["type"]:
                case "shadowsocks":
                    node_cleaned = {
                        k: copy.deepcopy(outbound[k])
                        for k in ["tag", "type", "server", "server_port", "method", "password"]
                        if k in outbound
                    }
                    
                case _:
                    node_cleaned = {
                        k: copy.deepcopy(outbound[k])
                        for k in ["tag", "type", "server", "server_port"]
                        if k in outbound
                    }
                            
                    for k in outbound:
                        if k not in node_cleaned:
                            node_cleaned[k] = outbound[k]
                    
            nodes.append(node_cleaned)
            
        return nodes
    
    @classmethod
    def merge_singbox_config(
            cls,
            nodes: List[Node],
            inbound_mixd_in: bool,
            inbound_tun_in: bool,
            with_clash_api: bool,
            type: Literal["airport", "diy"],
            clash_api_path: str = "dashboard",
            template_file: Path = Path("template.json")
    ):
        
        with template_file.open("r") as f:
            template: SingBoxConfig = json.load(f)
        
        match type:
            case "airport":
                cls.__merge_nodes_into_singbox_config(
                    nodes,
                    ["HK", "TW", "SG", "JP", "US"],
                    template
                )
            case "diy":
                cls.__merge_nodes_into_singbox_config_no_area_group(
                    nodes,
                    template
                )
        
        cls.__merge_inbounds_into_singbox_config(
            template,
            mixed_in=inbound_mixd_in,
            tun_in=inbound_tun_in
        )

        if with_clash_api:
            cls.__merge_clash_api_into_singbox_config(template, clash_api_path=clash_api_path)
        
        return template

        