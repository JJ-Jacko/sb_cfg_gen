import copy
from typing import List

from sb_cfg_gen.libs.areas import Areas
from sb_cfg_gen.libs.dicts import Node
from sb_cfg_gen.libs.other import keywords_in_text
from sb_cfg_gen.libs.types import AreaCode


class NodeFactor:
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
            tag = node["tag"]
            if area_code in tag:
                filtered_nodes.append(node)
            elif Areas.get(area_code).flag in tag:
                filtered_nodes.append(node)
            else:
                if (
                    area_code == "IN"
                    and "印度尼西亚" in tag
                ):
                    continue

                if keywords_in_text(Areas.get(area_code).keywords, tag):
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
