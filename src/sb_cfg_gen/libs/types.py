from typing import Literal


AreaCode = Literal[
    # 东亚
    "HK", "MO", "TW", "JP", "KR",
    
    # 东南亚
    "SG", "MY", "TH", "VN", "KH", "ID", "PH",
    
    # 南亚
    "IN", "PK", "BD", "NP",
    
    # 中亚
    "KZ", "UZ",
    
    # 西亚
    "GE", "AM", "TR", "CY", "IL", "QA", "AE", "SA", "IQ", "OM", "AZ",
    
    # 东欧
    "RU", "UA", "MD", "EE", "RO", "SK", "LV", "LT", "PL", "AT", "HU",
    
    # 东南欧
    "BG", "RS", "AL", "HR", "SI", "GR", "MK",
    
    # 西欧
    "DE", "FR", "NL", "BE", "LU", "GB", "IE", "IT", "ES", "PT", "CH",
    
    # 北欧
    "DK", "SE", "NO", "FI", "IS",
    
    # 大洋洲
    "AU", "NZ",
    
    # 北美洲
    "CA", "US", "MX",
    
    # 南美洲
    "GT", "CR", "CO", "EC", "BR", "AR", "PE", "CL", "BO", "UY", "GF",
    
    # 非洲
    "EG", "MG", "DZ", "AO", "NG", "ZA", "TG",
    
    # 南极洲
    "AQ"
]


NodeType = Literal[
    "hysteria2",
    "shadowsocks",
    "vless",
    "vmess"
]