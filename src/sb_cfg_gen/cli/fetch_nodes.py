import itertools
import requests
import time

from sb_cfg_gen import context
from sb_cfg_gen.dicts import SingBoxConfig
from sb_cfg_gen.factors import config_ops
from sb_cfg_gen.factors import node_ops
from sb_cfg_gen.other import load_json_file
from sb_cfg_gen.other import write_json_file
from sb_cfg_gen.web import Client


__all__ = ["run"]


def fetch(url: str):
    client = Client("SingBox")
    
    for attempt in itertools.count(0):
        if attempt >= 3:
            raise Exception("airport can not support sing-box")
        
        resp = client.fetch_airport_config(url)
        
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
    
    nodes = config_ops.extra_nodes_from_singbox_config(raw_cfg)
    nodes_deduplicated = node_ops.deduplicate_nodes(nodes)
    write_json_file(context.nodes_p, nodes_deduplicated)
    