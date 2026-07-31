import functools
import itertools
import time
from typing import Literal

import httpx

from sb_cfg_gen import context


__all__ = ["VirtualClient"]


def web_retry(func):
    """
    Decorator for retrying web operations in case of disconnection
    修饰 Web 请求的函数断联后尝试重连

    Raises:
        Exception:
            Raised when multiple retry attempts fail
            多次尝试重连都无法连上
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in itertools.count(0):
            if attempt > 10:
                raise Exception("Web connection failed after multiple retries")
            
            try:
                resp: httpx.Response = func(*args, **kwargs)
            except (
                httpx.ConnectError,
                httpx.ConnectTimeout
            ):
                time.sleep(10)
                continue
            
            if resp.status_code in (504, ):
                time.sleep(10)
                continue
            
            break
        
        return resp
    
    return wrapper


class VirtualClient:
    client: httpx.Client
    
    def __init__(
            self,
            client_type: Literal["V2rayN", "SingBox", "ClashMeta"]
    ):
        self.client = httpx.Client()
    
        self.client.headers = {
            "user-agent": context.UA_MAP.get(client_type)
        }
    
    @web_retry
    def fetch_airport_config(self, url: str):
        resp = self.client.get(url)

        return resp