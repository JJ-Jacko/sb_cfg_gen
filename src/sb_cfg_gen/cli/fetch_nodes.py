import itertools
import requests
import time

from sb_cfg_gen import context
from sb_cfg_gen.dicts import SingBoxConfig
from sb_cfg_gen.factors.config_factor import ConfigFactor
from sb_cfg_gen.factors.node_factor import NodeFactor
from sb_cfg_gen.other import load_json_file
from sb_cfg_gen.other import write_json_file
from sb_cfg_gen.web import SingBox


__all__ = ["run"]


def fetch(url: str):
    client = SingBox()
    
    for attempt in itertools.count(0):
        if attempt >= 3:
            raise Exception("airport can not support sing-box")
        
        resp = client.fetch_singbox_config_file(url)
        
        try:
            cfg: SingBoxConfig = resp.json()
        except requests.exceptions.JSONDecodeError:
            time.sleep(5)
            continue

        return cfg


def run():
    # raw_cfg = load_json_file(context.raw_cfg_p)

    url = context.project_config["airport_url"]
    raw_cfg = fetch(url)
    write_json_file(context.raw_cfg_p, raw_cfg)
    
    nodes = ConfigFactor.extra_nodes_from_singbox_config(raw_cfg)
    nodes_deduplicated = NodeFactor.deduplicate_nodes(nodes)
    write_json_file(context.nodes_p, nodes_deduplicated)
    