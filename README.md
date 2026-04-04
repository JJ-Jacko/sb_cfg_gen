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
uv sync
source .venv/bin/activate
```

### Run
```sh
sb-cfg-gen
```
```log
url:
```
