from typing import Annotated
from typing import List
from typing import Literal

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query

from sb_cfg_gen import context
from sb_cfg_gen.dicts import Node
from sb_cfg_gen.factors import config_ops
from sb_cfg_gen.factors import node_ops
from sb_cfg_gen.other import load_json_file


app = FastAPI()


@app.get("/sb_cfg")
def sb_cfg(
        token: str,
        source: Literal["airport", "diy"] = "airport",
        client: Literal["app", "cli-win", "cli-linux", "server"] = "app",
        mainstream_area: Annotated[
            bool,
            Query(description=(
                "Using the custom **areas** nodes instead of all the nodes from airport. "
                "Only while `source` is set to `airport` effect."   
            ))
        ] = True,
        sort: Annotated[
            bool,
            Query(description=(
                "Using the custom **positions** instead of default positions of airport. "
                "Only while `source` is set to `airport` effect."   
            ))
        ] = True,
        rename: Annotated[
            bool,
            Query(description=(
                "Using the custom **names** instead of default names of airport. "
                "Only while `source` is set to `airport` effect."   
            ))
        ] = True,
        area_group: Annotated[
            bool,
            Query(description=(
                "Using the **area group** instead of default non-grouping layout in outbound. "
                "Only while `source` is set to `airport` effect."   
            ))
        ] = False
    ):
    
    if token not in context.CONFIG["api_tokens"]:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if source == "airport":
        nodes_raw: List[Node] = load_json_file(context.CACHE.NODES)
        
        if mainstream_area:
            nodes_1 = node_ops.filter_nodes_with_specified_areas(nodes_raw, context.CONFIG["buildin_area_codes"])
        else:
            nodes_1 = nodes_raw
        
        if sort:
            nodes_2 = node_ops.sort_nodes(nodes_1)
        else:
            nodes_2 = nodes_1
        
        if rename:
            nodes_3 = node_ops.rename_nodes(nodes_2)
        else:
            nodes_3 = nodes_2
            
    elif source == "diy":
        nodes_3: List[Node] = load_json_file(context.CACHE.NODES_DIY)
        
    if client == "app":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes_3,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=False,
            area_group=area_group
        )
    elif client == "cli-win":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes_3,
            inbound_mixd_in=False,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group
        )
    elif client == "cli-linux":
        sb_cfg = config_ops.merge_singbox_config_client(
            nodes_3, 
            inbound_mixd_in=True,
            inbound_tun_in=True,
            with_clash_api=True,
            area_group=area_group,
            clash_api_path="/var/www/clash_api"
        )
    elif client == "server":
        sb_cfg = config_ops.merge_singbox_config_web_scraper(nodes_3)
    
    return sb_cfg
