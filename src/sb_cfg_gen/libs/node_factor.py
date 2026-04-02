import copy
from typing import get_args
from typing import List

from sb_cfg_gen.libs.areas import Areas
from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.types import AreaCode


class NodeFactor:
    node_type_keywords: List[str] = [
        "[优]",
        "[家宽]",
        "[家宽/住宅]",
        "[原生]",
        "[非原生]",
        "[日动]",
        "[月动]",
        "[大宽带]",
        "[实验]",
        "[星链]",
        "[starlink]",
        "[T-Mobile]",
        "[So-Net]",
        "[Hawaiian]",
        "[ISP]",
        "[ATT]",
        "[GTT]",
        "[vless]"
    ]
    node_level_keywords: List[str] = ["x0.8", "x1", "x3", "x2", "x4"]
    
    @classmethod
    def __node_in_nodes(cls, node: Node, nodes: List[Node]):
        for exist_node in nodes:
            if (
                node["server"] == exist_node["server"]
                and node["server_port"] == exist_node["server_port"]
            ):
                return True

        return False

    @classmethod
    def __get_cleaned_tag(cls, tag: str):
        tag_cleaned = tag

        for kw in cls.node_type_keywords:
            i = tag_cleaned.find(kw)
            if i != -1:
                tag_cleaned = tag_cleaned[:i] + tag_cleaned[i + len(kw):]
        
        return tag_cleaned

    @classmethod
    def __get_basic_nodes(cls, nodes: List[Node]):
        basic_nodes: List[Node] = []
        
        for node in nodes:
            tag_cleaned = cls.__get_cleaned_tag(node["tag"])
            if keywords_in_text(cls.node_level_keywords, tag_cleaned):
                if keywords_in_text(["x1", "x0.8"], tag_cleaned):
                    basic_nodes.append(node)
            else:
                basic_nodes.append(node)
        
        return basic_nodes

    @classmethod
    def deduplicate_nodes(cls, nodes: List[Node]) -> List[Node | None]:
        cleaned_nodes = []
        for n in nodes:
            if cls.__node_in_nodes(n, cleaned_nodes):
                continue
            
            cleaned_nodes.append(n)

        return cleaned_nodes

    @classmethod
    def filter_nodes_with_specified_area(
            cls,
            nodes: List[Node],
            area_code: AreaCode
    ) -> List[Node | None]:
        
        filtered_nodes: List[Node] = []
        for node in nodes:
            tag_cleaned = cls.__get_cleaned_tag(node["tag"])
            if Areas.get(area_code).flag in tag_cleaned:
                filtered_nodes.append(node)
            elif area_code in tag_cleaned:
                filtered_nodes.append(node)
            elif area_code == "IN" and "印度尼西亚" in tag_cleaned:
                continue
            elif keywords_in_text(Areas.get(area_code).keywords, tag_cleaned):
                filtered_nodes.append(node)

        return filtered_nodes

    @classmethod
    def rename_same_area_nodes(
            cls,
            nodes: List[Node],
            area_code: AreaCode
    ) -> List[Node]:
        renamed_nodes = []
        
        for i, node in enumerate(nodes):
            new_node = copy.deepcopy(node)
            new_node["tag"] = f"{Areas.get(area_code).flag} {area_code} {i + 1}"
            renamed_nodes.append(new_node)
        
        return renamed_nodes

    @classmethod
    def organize_and_rename_nodes(cls, nodes: List[Node]):
        result_nodes: List[Node] = []
        
        for area_code in get_args(AreaCode):
            specified_area_nodes = cls.filter_nodes_with_specified_area(nodes, area_code)
            basic_nodes = cls.__get_basic_nodes(specified_area_nodes)
            for node in cls.rename_same_area_nodes(basic_nodes, area_code):
                result_nodes.append(node)
    
        return result_nodes