# Sing-box 配置文件生成器

**Languages:** [English](README.md) | [繁中](README_zh_hk.md)

## 📋 描述
由于 sing-box 官方更新比较激进，
很多机场通过订阅下发的 sing-box 配置文件实质上过于陈旧，
有许多配置不得当的地方，
故这个项目就是为了解决这个问题。

原理是通过 Python 的 `requests` 库请求该机场的 sing-box 配置文件，
然后通过规则将节点有关的配置文件提取出来，
最后移花接木到自己的配置文件模板上。

期间可以配置高度客制化的模板，
调整节点的顺序、分组或者分流规则，
也可以指定需不需要 clash-api 前端。 

## 🚀 使用方法
### 激活环境
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
机场订阅链接
```toml
airport_url = "https://example.com/sing-box"
```
允许通过的 token
```toml
api_tokens = [
    "jacko",
    "john"
]
```
#### 自建节点列表 `cache/nodes.json`
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
* `templates/client.json` 客户端模板
* `templates/web_scraper.json` 爬虫代理服务器模板
### 服务
WebAPI 服务文件 `/etc/systemd/system/sb_cfg_gen_webapi.service`
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
自动生成机场配置文件的服务文件 `/etc/systemd/system/sb_cfg_gen_fetch_nodes.service`
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
计时文件 `/etc/systemd/system/sb_cfg_gen_fetch_nodes.timer`
```ini
[Unit]
Description=Timer for sb_cfg_gen_fetch_nodes.service

[Timer]
OnCalendar=*-*-* 00,12:00:00

[Install]
WantedBy=timers.target
```
重载
```sh
sudo systemctl daemon-reload
```
开启 WebAPI 服务
```sh
sudo systemctl start sb_cfg_gen_webapi.service
```
```sh
sudo systemctl enable sb_cfg_gen_webapi.service
```
开启计时服务
```sh
sudo systemctl start sb_cfg_gen_fetch_nodes.timer
```
```sh
sudo systemctl enable sb_cfg_gen_fetch_nodes.timer
```
