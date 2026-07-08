from typing import List


AIRPORT_INFO_KEYWORDS: List[str] = [
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
]

NODE_TYPE_KEYWORDS: List[str] = [
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
]

NODE_LEVEL_KEYWORDS: List[str] = ["x0.8", "x1", "x3", "x2", "x4"]