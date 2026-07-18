# Sing-box 配置文件生成器

**Languages:** [简中](README_zh_cn.md) | [English](README.md)

## 📋 描述
由於 sing-box 官方更新比較激進，
很多機場透過訂閱下發的 sing-box 配置文件實質上過於陳舊，
有許多配置不得當的地方，
故這個項目就是為了解決這個問題。

原理是通過 Python 的 `requests` 庫請求該機場的 sing-box 配置文件，
然後通過規則將節點有關的配置文件提取出來，
最後移花接木到自己的配置文件模板上。

期間可以配置高度客製化的模板，
調整節點的順序、分組或者分流規則，
也可以指定需不需要 clash-api 前端。

## 🚀 使用方法
### 激活環境
```sh
uv venv --python /usr/bin/python3 .venv
```
```sh
uv sync
```
```sh
source .venv/bin/activate
```
### 配置
#### 配置文件 `config.toml`
機場訂閲鏈接
```toml
airport_url = "https://example.com/sing-box"
```
容許通過的 token
```toml
api_tokens = [
    "jacko",
    "john"
]
```
需要注入 Sing-box 配置文件的節點的地區 
```toml
buildin_area_codes = ["HK", "TW", "SG", "JP", "US"]
```
#### 自建節點列表 `cache/nodes.json`
```json
[
    {
        "tag": "vless_reality",
        "type": "vless",
        ...
    },
    {
        "tag": "hy2",
        "type": "hysteria2",
        ...
    },
    ...
]
```
#### Sing-box 配置文件模板 `templates`
* `templates/client.json` 客戶端模板
* `templates/web_scraper.json` 爬蟲代理伺服器模板
### 服務
WebAPI 服務文件 `/etc/systemd/system/sb_cfg_gen_webapi.service`
```ini
[Unit]
Description=Sing-box Config Genarator Web API
After=network.target
Wants=network.target
Before=shutdown.target

[Service]
Type=simple
User=web_runner
WorkingDirectory=/opt/sb_cfg_gen
ExecStart=/opt/sb_cfg_gen/.venv/bin/sb-web-api

[Install]
WantedBy=multi-user.target
```
自動生成機場配置文件的服務文件 `/etc/systemd/system/sb_cfg_gen_fetch_nodes.service`
```ini
[Unit]
Description=Sing-box Config Genarator Fetch Nodes
After=network.target

[Service]
Type=oneshot
User=web_runner
WorkingDirectory=/opt/sb_cfg_gen
ExecStart=/opt/sb_cfg_gen/.venv/bin/sb-fetch-nodes
```
計時文件 `/etc/systemd/system/sb_cfg_gen_fetch_nodes.timer`
```ini
[Unit]
Description=Timer for sb_cfg_gen_fetch_nodes.service

[Timer]
OnCalendar=*-*-* 00,12:00:00

[Install]
WantedBy=timers.target
```
重載
```sh
sudo systemctl daemon-reload
```
開啓 WebAPI 服務
```sh
sudo systemctl start sb_cfg_gen_webapi.service
```
```sh
sudo systemctl enable sb_cfg_gen_webapi.service
```
開啓計時服務
```sh
sudo systemctl start sb_cfg_gen_fetch_nodes.timer
```
```sh
sudo systemctl enable sb_cfg_gen_fetch_nodes.timer
```
### Web API
#### GET `/sb_cfg`
獲取 sing-box 配置文件.
| 參數 | 選項 | 默認 | 必要項 | 描述 |
| :-: | :-: | :-: | :-: | :-: |
| token |  |  | ✔️ | API token |
| source | airport | ✔️ |  | 透過機場獲取節點 |
|  | diy |  |  | 透過客制化獲取節點 |
| client | app | ✔️ |  | App 的配置文件 (Andriod, IOS, Mac 官方 App) |
|  | cli-win |  |  | 在 Windows 命令行的配置文件 |
|  | cli-linux |  |  | 在 Linux 命令行的配置文件 |
|  | server |  |  | 在伺服器用於爬蟲程式的配置文件 |
| mainstream_area | true / false | true |  | 使用客制化的地區節點替代機場默認的所有節點，僅當 `source` 設置為 `airport` 時才生效 |
| organize_and_rename | true / false | false |  | 使用客制化的名稱和位置替代機場默認的名稱和位置，僅當 `source` 設置為 `airport` 時才生效 |
| area_group | true / false | false |  | 在 outbound 使用地區組替代默認的無組佈局，僅當 `client` 設置為 `app`, `cli-win`, `cli-linux` 時才生效 |
