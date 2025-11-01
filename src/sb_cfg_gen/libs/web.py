import requests


def url_get_singbox_config_file(url: str):
    headers = {
        "user-agent": "SFA/1.12.12 (575; sing-box 1.12.12; language zh_Hant_HK)",
        "accept-encoding": "gzip"
    }

    resp = requests.get(url, headers=headers)
    
    return resp.json()