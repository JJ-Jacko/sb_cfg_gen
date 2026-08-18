from typing import Final
from typing import FrozenSet
from typing import get_args
from typing import Mapping
from typing import Tuple

from types import MappingProxyType

from sb_cfg_gen import types
from sb_cfg_gen.datas import Area


AIRPORT_INFO_KEYWORDS: Final[FrozenSet[str]] = frozenset([
    # KTM
    "剩余流量",
    "距离下次重置剩余",
    "套餐到期",
    
    # 流量光
    "剩余流量",
    "距离下次重置流量剩余",
    "未到期",
    
    # 快充云
    "过期时间",
    "官方地址",
    "备用地址"
])

NODE_TYPE_KEYWORDS: Final[FrozenSet[str]] = frozenset([
    "[优]",
    "[家宽]",
    "[家宽/住宅]",
    "[原生]",
    "[非原生]",
    "[日动]",
    "[月动]",
    "[大宽带]",
    "[实验]",
    "[星链]",
    "[starlink]",
    "[T-Mobile]",
    "[So-Net]",
    "[Hawaiian]",
    "[ISP]",
    "[ATT]",
    "[BGP]",
    "[GTT]",
    "[vless]"
])

NODE_LEVEL_KEYWORDS: Final[FrozenSet[str]] = frozenset(["x0.8", "x1", "x3", "x2", "x4"])

AREAS: Final[Tuple[Area, ...]] = (
    # 东亚
    Area("HK", "🇭🇰", ["香港", "Hong Kong"]),
    Area("MO", "🇲🇴", ["澳门", "Macao"]),
    Area("TW", "🇹🇼", ["台湾", "Taiwan"]),
    Area("JP", "🇯🇵", ["日本", "Japan"]),
    Area("KR", "🇰🇷", ["韩国"]),

    # 东南亚
    Area("SG", "🇸🇬", ["新加坡", "Singapore"]),
    Area("MY", "🇲🇾", ["马来西亚"]),
    Area("TH", "🇹🇭", ["泰国"]),
    Area("VN", "🇻🇳", ["越南"]),
    Area("KH", "🇰🇭", ["柬埔寨"]),
    Area("ID", "🇮🇩", ["印度尼西亚", "印尼"]),
    Area("PH", "🇵🇭", ["菲律宾"]),

    # 南亚
    Area("IN", "🇮🇳", ["印度"]),
    Area("PK", "🇵🇰", ["巴基斯坦"]),
    Area("BD", "🇧🇩", ["孟加拉"]),
    Area("NP", "🇳🇵", ["尼泊尔"]),
    
    # 中亚
    Area("KZ", "🇰🇿", ["哈萨克斯坦"]),
    Area("UZ", "🇺🇿", ["乌兹别克斯坦"]),

    # 西亚
    Area("GE", "🇬🇪", ["格鲁吉亚"]),
    Area("AM", "🇦🇲", ["亚美尼亚"]),
    Area("TR", "🇹🇷", ["土耳其"]),
    Area("CY", "🇨🇾", ["塞浦路斯"]),
    Area("IL", "🇮🇱", ["以色列"]),
    Area("QA", "🇶🇦", ["卡塔尔"]),
    Area("AE", "🇦🇪", ["阿拉伯联合酋长国"]),
    Area("SA", "🇸🇦", ["沙特阿拉伯"]),
    Area("IQ", "🇮🇶", ["伊拉克"]),
    Area("OM", "🇴🇲", ["阿曼"]),
    Area("AZ", "🇦🇿", ["阿塞拜疆"]),

    # 东欧
    Area("RU", "🇷🇺", ["俄罗斯"]),
    Area("UA", "🇺🇦", ["乌克兰"]),
    Area("MD", "🇲🇩", ["摩尔多瓦"]),
    Area("EE", "🇪🇪", ["爱沙尼亚"]),
    Area("RO", "🇷🇴", ["罗马尼亚"]),
    Area("SK", "🇸🇰", ["斯洛伐克"]),
    Area("LV", "🇱🇻", ["拉脱维亚"]),
    Area("LT", "🇱🇹", ["立陶宛"]),
    Area("PL", "🇵🇱", ["波兰"]),
    Area("AT", "🇦🇹", ["奥地利"]),
    Area("HU", "🇭🇺", ["匈牙利"]),
    
    # 东南欧
    Area("BG", "🇧🇬", ["保加利亚"]),
    Area("RS", "🇷🇸", ["塞尔维亚"]),
    Area("AL", "🇦🇱", ["阿尔巴尼亚"]),
    Area("HR", "🇭🇷", ["克罗地亚"]),
    Area("SI", "🇸🇮", ["斯洛文尼亚"]),
    Area("GR", "🇬🇷", ["希腊"]),
    Area("MK", "🇲🇰", ["马其顿"]),
    Area("MC", "🇲🇨", ["摩纳哥"]),
    
    # 西欧
    Area("DE", "🇩🇪", ["德国"]),
    Area("FR", "🇫🇷", ["法国"]),
    Area("NL", "🇳🇱", ["荷兰"]),
    Area("BE", "🇧🇪", ["比利时"]),
    Area("LU", "🇱🇺", ["卢森堡"]),
    Area("GB", "🇬🇧", ["英国"]),
    Area("IE", "🇮🇪", ["爱尔兰"]),
    Area("IT", "🇮🇹", ["意大利"]),
    Area("ES", "🇪🇸", ["西班牙"]),
    Area("PT", "🇵🇹", ["葡萄牙"]),
    Area("CH", "🇨🇭", ["瑞士"]),
    Area("CZ", "🇨🇿", ["捷克"]),

    # 北欧
    Area("DK", "🇩🇰", ["丹麦"]),
    Area("SE", "🇸🇪", ["瑞典"]),
    Area("NO", "🇳🇴", ["挪威"]),
    Area("FI", "🇫🇮", ["芬兰"]),
    Area("IS", "🇮🇸", ["冰岛"]),

    # 大洋洲
    Area("AU", "🇦🇺", ["澳大利亚", "澳洲"]),
    Area("NZ", "🇳🇿", ["新西兰", "纽西兰"]),
    
    # 北美洲
    Area("CA", "🇨🇦", ["加拿大"]),
    Area("US", "🇺🇸", ["美国", "United States"]),
    Area("MX", "🇲🇽", ["墨西哥"]),
    
    # 南美洲
    Area("GT", "🇬🇹", ["危地马拉"]),
    Area("CR", "🇨🇷", ["哥斯达黎加"]),
    Area("CO", "🇨🇴", ["哥伦比亚"]),
    Area("EC", "🇪🇨", ["厄瓜多尔"]),
    Area("BR", "🇧🇷", ["巴西"]),
    Area("AR", "🇦🇷", ["阿根廷"]),
    Area("PE", "🇵🇪", ["秘鲁"]),
    Area("CL", "🇨🇱", ["智利"]),
    Area("BO", "🇧🇴", ["玻利维亚"]),
    Area("UY", "🇺🇾", ["乌拉圭"]),
    Area("GF", "🇬🇫", ["法属圭亚那"]),

    # 非洲
    Area("EG", "🇪🇬", ["埃及"]),
    Area("MG", "🇲🇦", ["摩洛哥"]),
    Area("DZ", "🇩🇿", ["阿尔及利亚"]),
    Area("AO", "🇦🇴", ["安哥拉"]),
    Area("NG", "🇳🇬", ["尼日利亚"]),
    Area("ZA", "🇿🇦", ["南非"]),
    Area("TG", "🇹🇬", ["多哥"]),
    
    # 南极洲
    Area("AQ", "🇦🇶", ["南极"])
)

AREA_MAPPING: Final[Mapping[types.AreaCode, Area]] = MappingProxyType({
    area.area_code: area
    for area in AREAS
})

AREA_CODES: Final[Tuple[str, ...]] = get_args(types.AreaCode)

NODE_TYPES: Final[FrozenSet[str]] = frozenset(get_args(types.NodeType))
