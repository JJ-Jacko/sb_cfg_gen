from pathlib import Path
from typing import List
from typing import Literal

from fastapi import FastAPI
from fastapi import HTTPException

from sb_cfg_gen import context
from sb_cfg_gen.dicts import Node
from sb_cfg_gen.factors import config_ops
from sb_cfg_gen.factors import node_ops
from sb_cfg_gen.other import load_config
from sb_cfg_gen.other import load_json_file


app = FastAPI()
project_config_file = Path("config.toml")
config_file = load_config(project_config_file)


@app.get("/sb_cfg")
def sb_cfg(
        token: str,
        source: Literal["airport", "diy"] = "airport",
        client: Literal["app", "cli-win", "cli-linux", "server"] = "app",
        mainstream_area: bool = True,
        organize_and_rename: bool = False,
        area_group: bool = False
    ):
    """
    Args:
        mainstream_area:
            Using the custom areas nodes instead of all the nodes from airport.
            Only while `source` is set to `airport` effect.
        organize_and_rename:
            Using the custom names and positions instead of default names and positions of airport.
            Only while `source` is set to `airport` effect.
        area_group:
            Using the area group instead of default non-grouping layout in outbound.
            Only while `client` is set to `app`, `cli-win`, `cli-linux` effect.
    """
    
    if token not in config_file["api_tokens"]:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if source == "airport":
        nodes_raw: List[Node] = load_json_file(context.f_nodes)
        
        if mainstream_area:
            nodes_filterd_area = node_ops.filter_nodes_with_specified_areas(nodes_raw, context.project_config["buildin_area_codes"])
        else:
            nodes_filterd_area = nodes_raw
            
        if organize_and_rename:
            nodes = node_ops.organize_and_rename_nodes(nodes_filterd_area)
        else:
            nodes = nodes_filterd_area
            
    elif source == "diy":
        nodes: List[Node] = load_json_file(context.f_nodes_diy)
        
    if client == "app":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=False,
            area_group=area_group
        )
    elif client == "cli-win":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group
        )
    elif client == "cli-linux":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes, 
            inbound_mixd_in=True,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group,
            clash_api_path="/var/www/clash_api"
        )
    elif client == "server":
        sb_cfg = config_ops.merge_singbox_config_web_scraper(nodes)
    
    return sb_cfg
