import itertools
import time
from urllib import parse

from sb_cfg_gen import context
from sb_cfg_gen.factors import node_ops
from sb_cfg_gen.other import base64_decode
from sb_cfg_gen.other import write_json_file
from sb_cfg_gen.parses import vless
from sb_cfg_gen.web import Client


__all__ = ["run"]


def fetch(url: str):
    client = Client("V2rayN")
    
    for attempt in itertools.count(0):
        if attempt >= 3:
            raise Exception("airport can not support V2rayN")
        
        resp = client.fetch_airport_config(url)
        
        try:
            content = base64_decode(resp.content)
        except Exception:
            time.sleep(5)
            continue

        return content


def run():
    # urls_str = base64_decode(context.raw_base64.read_text())

    url = context.project_config["airport_url"]
    urls_str = fetch(url)
    
    urls_node = urls_str.split("\r\n")
    nodes = [
        vless.exec(parse.unquote(url_node))
        for url_node in urls_node
        if url_node
    ]
    
    nodes_deduplicated = node_ops.deduplicate_nodes(nodes)
    write_json_file(context.nodes_p, nodes_deduplicated)
    