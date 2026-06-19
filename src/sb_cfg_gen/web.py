import functools
import itertools
import time

import requests


__all__ = ["SingBox"]


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
                resp: requests.Response = func(*args, **kwargs)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout
            ):
                time.sleep(10)
                continue
            
            if resp.status_code in (504, ):
                time.sleep(10)
                continue
            
            break
        
        return resp
    
    return wrapper


class SingBox:
    s: requests.Session
    
    def __init__(self):
        self.s = requests.Session()
    
        self.s.headers = {
            "user-agent": "SFA/1.12.12 (575; sing-box 1.12.12; language zh_Hant_HK)",
            "accept-encoding": "gzip"
        }
    
    @web_retry
    def fetch_singbox_config_file(self, url: str):
        resp = self.s.get(url)

        return resp