from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi import HTTPException

from sb_cfg_gen.libs.other import load_json_file
from sb_cfg_gen.libs.other import load_config


app = FastAPI()
project_config_file = Path("config.toml")
config_file = load_config(project_config_file)


@app.get("/sb_cfg")
def sb_cfg(
        token: str,
        type: Literal["airport", "diy"] = "airport",
        client: Literal["app", "cli", "server"] = "app"
    ):
    if token not in config_file["api_tokens"]:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    sb_cfg: dict = load_json_file(f"output/{type}-{client}.json")
    
    return sb_cfg
