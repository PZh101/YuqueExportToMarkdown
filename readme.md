## 语雀导出的Lake文档转为Markdown文档

> 环境:
> python 3.7
> pip



### 使用方法

生成依赖(使用时可以忽略该步骤)：
```shell script
# 安装
pip install pipreqs
# 在当前目录生成
pipreqs . --encoding=utf8 --force
```

安装依赖：
```shell script
pip install -r requirements.txt
```

运行代码：

```shell script
python startup.py -i meta.json路径 -o 输出md文档路径
```

```shell script
python startup.py -l your.lakebook路径 -o 输出md文档路径
```

feature:
- [x] 支持命令行转换文件
- [x] 支持直接读取lakebook格式的文件
- [ ] 提供可视化操作