import requests


def url_get_raw_config_file(url: str):
    headers = {
        "user-agent": "SFA/1.12.9 (575; sing-box 1.12.9; language zh_Hant_HK)",
        "accept-encoding": "gzip"
    }

    resp = requests.get(url, headers=headers)
    
    return resp.json()
