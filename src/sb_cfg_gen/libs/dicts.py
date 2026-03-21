from typing import List
from typing import TypedDict

from sb_cfg_gen.libs.types import NodeType


class Node(TypedDict):
    tag: str
    type: NodeType
    server: str
    server_port: int
    method: str
    password: str
    domain_resolver: str
    plugin: str
    plugin_opts: str
    network: str
    tcp_fast_open: bool

class RuleSet(TypedDict):
    tag: str
    type: str
    format: str
    url: str

class Rules(TypedDict):
    rule_set: List[str]
    outbound: str

class Route(TypedDict):
    rule_set: List[RuleSet]
    rules: List[Rules]

class SingBoxConfig(TypedDict):
    log: dict
    dns: dict
    ntp: dict
    inbounds: list
    outbounds: List[Node | dict]
    route: Route
    experimental: dict
