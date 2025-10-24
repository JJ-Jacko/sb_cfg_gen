import json
from sb_cfg_gen.lib import url_get_raw_config_file
from sb_cfg_gen.lib import patch_config_file


def main():
    url = input("url: ")
    print(f"正在获取: {url}")
    raw = url_get_raw_config_file(url)
    cfg_file = patch_config_file(raw)
    with open(f"jacko.json", "w") as f:
        json.dump(cfg_file, f, indent=4, ensure_ascii=False)
    print("保存成功！")


if __name__ == "__main__":
    main()