# Sing-box 配置文件生成器

**Languages:** [English](README.md) | [繁中](README_zh_hk.md)


## 📋 描述
由于 sing-box 官方更新比较激进，
很多机场通过订阅下发的 sing-box 配置文件实质上过于陈旧，
有许多配置不得当的地方，
故这个项目就是为了解决这个问题。

原理是通过 Python 的 `request` 库请求该机场的 sing-box 配置文件，
然后通过规则将节点有关的配置文件提取出来，
最后移花接木到自己的配置文件模板上。

期间可以配置高度客制化的模板，
调整节点的顺序、分组或者分流规则，
也可以指定需不需要 clash-api 前端。 

## 🚀 使用方法
### 激活环境
```sh
uv sync
source .venv/bin/activate
```

### 运行
```sh
sb-cfg-gen
```
```log
url:
```
