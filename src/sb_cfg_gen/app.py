import tomllib
from typing import Literal

from fastapi import FastAPI
from fastapi import HTTPException

from sb_cfg_gen.libs.other import load_json_file


app = FastAPI()
with open("config.toml", "rb") as f:
    config_file = tomllib.load(f)


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
