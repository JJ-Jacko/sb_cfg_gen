import requests

from sb_cfg_gen.libs.waiting import Waiting


def _web_retry(func: callable):
    """Decorator for retrying web operations in case of disconnection 修饰 Web 请求的函数断联后尝试重连

    Args:
        func (callable): The function that accesses the web Web 请求的函数
        
    Raises:
        Exception: Raised when multiple retry attempts fail 多次尝试重连都无法连上
    """
    
    def wrapper(*args, **kwargs):
        count_retry = 0
        while True:
            if count_retry > 10:
                raise Exception("Web connection failed after multiple retries")
            try:
                result = func(*args, **kwargs)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout
            ):
                count_retry += 1
                Waiting.normal(10, "Reconnect in [n]s")
                continue
            break
        return result
    
    return wrapper


class Web:
    s = requests.session()
    s.headers = {
        "user-agent": "SFA/1.12.12 (575; sing-box 1.12.12; language zh_Hant_HK)",
        "accept-encoding": "gzip"
    }
    
    @classmethod
    @_web_retry
    def singbox_config_file(cls, url: str):
        resp = cls.s.get(url)

        return resp