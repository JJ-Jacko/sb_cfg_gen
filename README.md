# Sing-box Config Generator

**Languages:** [简中](README_zh_cn.md) | [繁中](README_zh_hk.md)

## 📋 Description
Since official sing-box updates are quite aggressive,
the subscription-based configuration files provided by many airports are
essentially outdated and contain numerous improper configurations.
This project was created to address this exact issue. 

Under the hood, it uses the Python `requests` library to fetch the airport's sing-box config file,
extracts the node-related configurations using specific rules,
and finally injects them into your own custom configuration template. 

During this process, you can configure highly customized templates,
adjust node order, grouping, or routing rules, and specify whether a clash-api frontend is required.

## 🚀 Usage
### Activate Environment
```sh
uv venv --python /usr/bin/python3 .venv
```
```sh
uv sync
```
```sh
source .venv/bin/activate
```
### Manually run
#### Generate airport's sing-box config file 
Set configuration file `config.toml`
```toml
airport_url = "https://example.com/sing-box"
```
```sh
sb-gen-airport
```
#### Generate DIY sing-box config file 
Write nodes in file `nodes.json`
```json
{
    "nodes": [
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
}
```
```sh
sb-gen-diy
```
### Web API
Set configuration file `config.toml`
```toml
api_tokens = [
    "jacko",
    "john"
]
```
WebAPI service file `/etc/systemd/system/sb_cfg_gen_webapi.service`
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
Service file which automatically generate airport configration file `/etc/systemd/system/sb_cfg_gen.service`
```ini
[Unit]
Description=Sing-box Config Genarator
After=network.target

[Service]
Type=oneshot
User=web_runner
WorkingDirectory=/opt/sb_cfg_gen
ExecStart=/opt/sb_cfg_gen/.venv/bin/sb-gen-airport
```
Timmer file `/etc/systemd/system/sb_cfg_gen.timer`
```ini
[Unit]
Description=Timer for sb_cfg_gen.service

[Timer]
OnCalendar=*-*-* 00,12:00:00

[Install]
WantedBy=timers.target
```
