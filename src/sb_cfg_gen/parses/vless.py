from urllib import parse

from sb_cfg_gen.dicts import Node


def exec(url: str):
    """
    Parse `vless` type of the url to the sing-box type node.

    Args:
        url: `vless` type of the url.
    """
    
    parsed = parse.urlparse(url)
    kwargs = dict(parse.parse_qsl(parsed.query))
    
    node: Node = {
        "tag": parsed.fragment,
        "type": parsed.scheme,
        "server": parsed.hostname,
        "server_port": parsed.port,
        "uuid": parsed.username,
        "packet_encoding": "xudp",
        "flow": kwargs["flow"],
        "tls": {
            "enabled": True,
            "insecure": False,
            "utls": {
                "enabled": True,
                "fingerprint": kwargs["fp"]
            },
            "server_name": kwargs["sni"],
            "reality": {
                "enabled": True,
                "public_key": kwargs["pbk"],
                "short_id": kwargs["sid"]
            }
        }
    }

    return node