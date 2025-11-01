from typing import Literal


AreaCode = Literal[
    # 亚洲
    "HK", "TW", "JP", "KR", "VN", "SG", "IN",
    # 大洋洲
    "AU",
    # 欧洲
    "PL", "DE", "GB",
    # 北美洲
    "US", "CA"
]


NodeType = Literal[
    "hysteria2",
    "shadowsocks",
    "vless",
    "vmess"
]