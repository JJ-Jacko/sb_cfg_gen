from sb_cfg_gen.libs.datas import Area
from sb_cfg_gen.libs.types import AreaCode


areas = [
    # 亚洲
    Area("HK", "🇭🇰", ["香港", "Hong Kong"]),
    Area("TW", "🇹🇼", ["台湾", "Taiwan"]),
    Area("JP", "🇯🇵", ["日本", "Japan"]),
    Area("KR", "🇰🇷", ["韩国", "Korea", "South Korea"]),
    Area("VN", "🇻🇳", ["越南", "Vietnam"]),
    Area("SG", "🇸🇬", ["新加坡", "Singapore"]),
    Area("IN", "🇮🇳", ["印度", "India"]),
    # 大洋洲
    Area("AU", "🇦🇺", ["澳大利亚", "澳洲", "Australia"]),
    # 欧洲
    Area("PL", "🇵🇱", ["波兰", "Poland"]),
    Area("DE", "🇩🇪", ["德国", "Germany"]),
    Area("GB", "🇬🇧", ["英国", "United Kingdom"]),
    # 北美洲
    Area("US", "🇺🇸", ["美国", "United States"]),
    Area("CA", "🇨🇦", ["加拿大", "Canada"]),
    # 南极洲
    Area("AQ", "🇦🇶", ["南极", "Antarctica"])
]


def get_area_flag(area_code: AreaCode):
    for area in areas:
        if area_code == area.area_code:
            return area.flag
    
    raise Exception(f"{area_code} 不存在")


def get_area_keywords(area_code: AreaCode):
    for area in areas:
        if area_code == area.area_code:
            return area.keywords
    
    raise Exception(f"{area_code} 不存在")
