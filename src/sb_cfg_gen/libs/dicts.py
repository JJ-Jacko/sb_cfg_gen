from typing import List
from typing import TypedDict

from sb_cfg_gen.libs.types import NodeType

class Node(TypedDict):
    tag: str
    type: NodeType
    server: str
    server_port: int


class SingBoxConfig(TypedDict):
    log: dict
    dns: dict
    ntp: dict
    inbounds: list
    outbounds: List[Node | dict]
    route: dict
    experimental: dict
