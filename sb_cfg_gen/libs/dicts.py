from typing import TypedDict


class SingBoxConfig(TypedDict):
    log: dict
    dns: dict
    ntp: dict
    inbounds: list
    outbounds: list
    route: dict
    experimental: dict