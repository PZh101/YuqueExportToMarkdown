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

**可选参数：**

- 跳过已存在的图片和附件文件（提高重复转换速度）：
```shell script
python startup.py -l your.lakebook路径 -o 输出md文档路径 --skip-existing-resources
```

- 禁用图片下载：
```shell script
python startup.py -l your.lakebook路径 -o 输出md文档路径 -d False
```

打包
```shell
Pyinstaller -F -w -i image/asrgu-k3t3q-001.ico -n YuqueExportToMarkdown startup.py
```

feature:
- [x] 支持命令行转换文件
- [x] 支持直接读取lakebook格式的文件
- [x] 支持跳过已存在的图片和附件文件，提高重复转换效率
- [x] 支持禁用图片下载功能
- [ ] 提供可视化操作