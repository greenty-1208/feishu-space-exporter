# feishu-space-exporter
功能：
- 命令行交互式查看知识库
- 整本导出PDF

用户配置：
- 文件式
```
cp conf/user_config_template.yaml conf/user_config.yaml
```
```
# 更新相关参数
domain: {{domain}}
cookie: {{cookie}}
```
- 运行时输入


菜单命令：
|  命令   | 含义  |
|  ----  | ----  |
| h / help  | 查看本帮助 |
| q / quit  | 退出 |
| user | 查看当前登录用户|
| show&nbsp;&nbsp;space | 查看知识库列表|
| use&nbsp;&nbsp;$idx | 选择某一本知识库，$idx必须为数字, 可以通过show space查看| 选项|
| ls&nbsp;&nbsp;[-l] | 查看当前目录|
| cd&nbsp;&nbsp;$idx | 进入子目录|
| cd&nbsp;&nbsp;.. | 返回上级目录|
