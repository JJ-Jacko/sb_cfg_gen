from pathlib import Path
from typing import List
from typing import Literal

from fastapi import FastAPI
from fastapi import HTTPException

from sb_cfg_gen.cli import context
from sb_cfg_gen.dicts import Node
from sb_cfg_gen.factors.config_factor import ConfigFactor
from sb_cfg_gen.factors.node_factor import NodeFactor
from sb_cfg_gen.other import load_config
from sb_cfg_gen.other import load_json_file


app = FastAPI()
project_config_file = Path("config.toml")
config_file = load_config(project_config_file)


@app.get("/sb_cfg")
def sb_cfg(
        token: str,
        source: Literal["airport", "diy"] = "airport",
        client: Literal["app", "cli", "server"] = "app",
        area_group: bool = False
    ):
    if token not in config_file["api_tokens"]:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if source == "airport":
        nodes_raw: List[Node] = load_json_file(context.nodes_p)
        nodes = NodeFactor.organize_and_rename_nodes(nodes_raw)
    elif source == "diy":
        nodes: List[Node] = load_json_file(context.nodes_diy_p)
        
    if client == "app":
        sb_cfg = ConfigFactor.merge_singbox_config(
            nodes,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=False,
            area_group=area_group
        )
    elif client == "cli":
        sb_cfg = ConfigFactor.merge_singbox_config(
            nodes,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group
        )
    elif client == "server":
        sb_cfg = ConfigFactor.merge_singbox_config(
            nodes, 
            inbound_mixd_in=True,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group,
            clash_api_path="/var/www/clash_api"
        )
    
    return sb_cfg
