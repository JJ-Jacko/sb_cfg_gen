import requests

from sb_cfg_gen.libs.waiting import Waiting


def web_retry(func: callable):
    """修饰 Web 请求的函数断联后尝试重连

    Args:
        func (callable):  Web 请求的函数
        
    Raises:
        Exception: 多次尝试重连都无法连上
    """
    
    def wrapper(*args, **kwargs):
        count_retry = 0
        while True:
            if count_retry > 10:
                raise Exception("网络连接异常")
            try:
                result = func(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                count_retry += 1
                Waiting.normal(10, "[n]s 后尝试重连")
                continue
            break
        return result
    
    return wrapper


@web_retry
def url_get_singbox_config_file(url: str):
    headers = {
        "user-agent": "SFA/1.12.12 (575; sing-box 1.12.12; language zh_Hant_HK)",
        "accept-encoding": "gzip"
    }

    resp = requests.get(url, headers=headers)
    
    return resp.json()