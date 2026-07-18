import copy
from typing import List

from sb_cfg_gen import constants
from sb_cfg_gen.areas import Areas
from sb_cfg_gen.dicts import Node
from sb_cfg_gen.other import keywords_in_text
from sb_cfg_gen.types import AreaCode


def _node_in_nodes(node: Node, nodes: List[Node]):
    for exist_node in nodes:
        if (
            node["server"] == exist_node["server"]
            and node["server_port"] == exist_node["server_port"]
        ):
            return True

    return False


def _get_cleaned_tag(tag: str):
    tag_cleaned = tag

    for kw in constants.NODE_TYPE_KEYWORDS:
        i = tag_cleaned.find(kw)
        if i != -1:
            tag_cleaned = tag_cleaned[:i] + tag_cleaned[i + len(kw):]
    
    return tag_cleaned


def _get_basic_nodes(nodes: List[Node]):
    basic_nodes: List[Node] = []
    
    for node in nodes:
        tag_cleaned = _get_cleaned_tag(node["tag"])
        if keywords_in_text(constants.NODE_LEVEL_KEYWORDS, tag_cleaned):
            if keywords_in_text(["x1", "x0.8"], tag_cleaned):
                basic_nodes.append(node)
        else:
            basic_nodes.append(node)
    
    return basic_nodes


def deduplicate_nodes(nodes: List[Node]) -> List[Node | None]:
    cleaned_nodes = []
    for n in nodes:
        if _node_in_nodes(n, cleaned_nodes):
            continue
        
        cleaned_nodes.append(n)

    return cleaned_nodes


def filter_nodes_with_specified_area(
        nodes: List[Node],
        area_code: AreaCode
) -> List[Node | None]:
    """
    Fiter nodes with specified area from input nodes.

    Returns:
        nodes_with_specified_area: A list of the nodes which is in specified area.
    """
    
    filtered_nodes: List[Node] = []
    for node in nodes:
        tag_cleaned = _get_cleaned_tag(node["tag"])
        if Areas.get(area_code).flag in tag_cleaned:
            filtered_nodes.append(node)
        elif area_code in tag_cleaned:
            filtered_nodes.append(node)
        elif area_code == "IN" and "印度尼西亚" in tag_cleaned:
            continue
        elif keywords_in_text(Areas.get(area_code).keywords, tag_cleaned):
            filtered_nodes.append(node)

    return filtered_nodes


def filter_nodes_with_specified_areas(
        nodes: List[Node],
        buildin_area_codes: List[AreaCode],
):
    """
    Fiter nodes with specified areas from input nodes.

    Returns:
        nodes_with_specified_areas: A list of nodes in order of the list of the area codes.
    """
    
    return [
        node
        for area_code in buildin_area_codes
        for node in filter_nodes_with_specified_area(nodes, area_code)
    ]


def rename_same_area_nodes(
        nodes: List[Node],
        area_code: AreaCode
) -> List[Node]:
    renamed_nodes = []
    
    for i, node in enumerate(nodes):
        new_node = copy.deepcopy(node)
        new_node["tag"] = f"{Areas.get(area_code).flag} {area_code} {i + 1}"
        renamed_nodes.append(new_node)
    
    return renamed_nodes


def organize_and_rename_nodes(nodes: List[Node]):
    result_nodes: List[Node] = []
    
    for area_code in constants.AREA_CODES:
        specified_area_nodes = filter_nodes_with_specified_area(nodes, area_code)
        basic_nodes = _get_basic_nodes(specified_area_nodes)
        for node in rename_same_area_nodes(basic_nodes, area_code):
            result_nodes.append(node)

    return result_nodes
