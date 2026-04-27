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
uv sync
source .venv/bin/activate
```

### 運行
#### 生成機場的 sing-box 配置文件
設定配置文件 `config.toml`
```toml
airport_url = "https://example.com/sing-box"
```
```sh
sb-gen-airport
```
#### 生成客制化代理的 sing-box 配置文件
在檔案 `nodes.json` 中寫入節點
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
#### Web API
設定配置文件 `config.toml`
```toml
api_tokens = [
    "jacko",
    "john"
]
```
```sh
sb-web-api
```
