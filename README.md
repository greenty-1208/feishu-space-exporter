# feishu-space-exporter
## 写在前面

**本read me 包含了超前于开发进展的功能点，空余时间开发，欢迎关注+收藏**

飞书知识库是一款非常好用的在线文档知识库，但是如果想导出为本地文档，只能单篇导出

这个项目最主要的功能是希望提供批量导出整棵树的文档的能力，也希望可以提供命令行交互式的对知识库的访问（会访问网络）

本项目的批量导出能力只建议使用于个人知识库，不要应用于企业文档！！！

## 功能概述

|功能|已支持|
|---|---|
|在线访问列表目录|✔|
|离线访问已缓存列表目录| |
|批量文档导出| |
|指定根的文档树合并（PDF合并）| |
|指定根的文档树合并（json合并）| |
|可扩展开发式支持其他在线文档（提供基类）| |

## 用户配置：
- 文件式
```
cp conf/user_config_template.yaml conf/user_config.yaml
```
`user_config.yaml` 增加以下配置
```
domain: {{domain}}
cookie: {{cookie}}
```
- 运行时输入

## 使用
当前
```
./feishu_exporter.sh
```
未来
```
./feishu_exporter.sh [local] [--view_mode vscode(默认) / custom] 
```





## 菜单命令：
|  命令   | 含义  | 已支持 |
|  ----  | ----  | ---- |
| h / help  | 查看本帮助 | ✔ |
| q / quit  | 退出 | ✔ |
| user | 查看当前登录用户| ✔ |
| show&nbsp;&nbsp;space | 查看知识库列表| ✔ |
| use&nbsp;&nbsp;$idx | 选择某一本知识库，$idx必须为数字, 可以通过show space查看|  ✔ |
| pwd | 查看当前路径|  |
| ls&nbsp;&nbsp;[-l] | 查看当前目录下文件| ✔ |
| cd&nbsp;&nbsp;$idx | 进入指定\$idx目录<br>\$idx = '..' 返回上级目录| ✔ |
|view [-all] [-u] $idx |通过vscode 查看指定文档 <br>-all: 以$idx为根目录的整本文档（会提示需要提前导出, 不支持EXCEL）<br>-u: 如果编辑时间晚于导出时间会重新导出，也会重新生成整本<br> $idx = '.' 当前路径 |
|export [-all] $idx | 导出指定目录文档<br>-all: 以$idx为根目录的整本文档<br>$idx = '.' 当前路径,|


## 文档查看形式
由命令行参数`--view_mode`指定
### VScode模式 (默认)
|  类型   | 格式  | vscode模式 | 
|  --- | ----  | ---|
|  docx | pdf  | 任意PDF扩展程序 |
|  思维导图 | json  | 直接打开即可|
| excel  | xlsx  |Excel Viewer |

### 自定义模式
需要在`user_config.yaml` 中配置相关的软件的bin（或命令）
|  类型   | 格式  | 默认程序 | 
|  --- | ----  | ---|
|  docx | pdf  | 报错 |
|  思维导图 | json  | vim|
| excel  | xlsx  |报错 |


### FIX TODO 
- 未命名文档文件名是空的需要特殊处理一下