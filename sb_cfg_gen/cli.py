import argparse
import json
from sb_cfg_gen.lib import url_get_raw_config_file
from sb_cfg_gen.lib import patch_config_file


parser = argparse.ArgumentParser()
parser.add_argument("url", help="订阅链接")
args = parser.parse_args()


def main():
    url = args.url
    print(f"正在获取: {url}")
    raw = url_get_raw_config_file(url)
    cfg_file = patch_config_file(raw)
    with open(f"config.json", "w") as f:
        json.dump(cfg_file, f, indent=4, ensure_ascii=False)
    print("保存成功！")


if __name__ == "__main__":
    main()