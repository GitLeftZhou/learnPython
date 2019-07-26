excel对比小工具

将需要对比的文件放入当前文件夹，双击运行compare.exe即可
运行完成后会生成   XXX(打标记)   文件

模版文件可以随意编辑数据

如果想要修改模版文件名字：

用记事本程序打开configuration.config

# 模版文件名
templet_file=国别核查数据模板.xlsx


想要修改根据那一列匹配（eg.   这里是根据S列匹配）


# 模版文件匹配列
templet_match_col=S
# 对比文件匹配列
target_match_col=S


想要对比那一列的值（eg.   这里是对比U列的值）

# 模版文件对比列
templet_compare_col=U
# 对比文件对比列
target_compare_col=U