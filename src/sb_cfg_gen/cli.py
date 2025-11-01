import json
from sb_cfg_gen.libs.web import url_get_singbox_config_file


def main():
    print("输入屌丝机场(质量差流量多)的 url")
    url = input(">>> ")
    raw = url_get_singbox_config_file(url)
    
    print("输入苹果机场(高质量流量少)的 url")
    url = input(">>> ")
    raw = url_get_singbox_config_file(url)
    
    
    with open(f"jacko.json", "w") as f:
        json.dump(cfg_file, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
