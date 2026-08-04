import itertools
import json
import time
from urllib import parse

from sb_cfg_gen import context
from sb_cfg_gen.exceptions import ClientNotSupport
from sb_cfg_gen.factors import config_ops
from sb_cfg_gen.factors import node_ops
from sb_cfg_gen.other import base64_decode
from sb_cfg_gen.other import write_json_file
from sb_cfg_gen.parses import vless
from sb_cfg_gen.web import VirtualClient


__all__ = ["run"]


def fetch_using_V2rayN(url: str):
    """
    Raises:
        ClientNotSupport: When the airport not support V2rayN client.
    """
    virtual_client = VirtualClient("V2rayN")
    
    for attempt in itertools.count(0):
        if attempt >= 3:
            raise ClientNotSupport
        
        resp = virtual_client.fetch_airport_config(url)
        
        try:
            urls_str = base64_decode(resp.content)
        except Exception:
            time.sleep(5)
            continue

        break
    
    write_json_file(context.CACHE.RAW_BASE64, urls_str)
    urls_node = urls_str.split("\r\n")
    nodes = [
        vless.exec(parse.unquote(url_node))
        for url_node in urls_node
        if url_node
    ]
    
    return nodes


def fetch_using_SingBox(url: str):
    """
    Raises:
        ClientNotSupport: When the airport not support Sing-box client.
    """
    virtual_client = VirtualClient("SingBox")
    
    for attempt in itertools.count(0):
        if attempt >= 3:
            raise ClientNotSupport
        
        resp = virtual_client.fetch_airport_config(url)
        
        try:
            raw_cfg: str | list | dict = resp.json()
        except json.JSONDecodeError:
            time.sleep(5)
            continue

        break
    
    if isinstance(raw_cfg, (str, list)):
        raise ClientNotSupport
    
    if not isinstance(raw_cfg, dict):
        raise ClientNotSupport
    
    write_json_file(context.CACHE.RAW_CFG, raw_cfg)
    nodes = config_ops.extra_nodes_from_singbox_config(raw_cfg)

    return nodes
    

def run():
    url = context.CONFIG["airport_url"]
    
    try:
        nodes = fetch_using_SingBox(url)
    except ClientNotSupport:
        nodes = fetch_using_V2rayN(url)
    except ClientNotSupport:
        raise

    nodes_deduplicated = node_ops.deduplicate_nodes(nodes)
    write_json_file(context.CACHE.NODES, nodes_deduplicated)
    