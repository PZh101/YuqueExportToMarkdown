# import sys
import argparse
from lake.lake_setup import start_convert

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--meta', help="lake文件的meta.json路径", type=str)
    parser.add_argument('-o', '--output', help="生成markdown的根路径", type=str)
    parser.add_argument('-d', '--downloadImage', help="是否下载图片", type=bool, default=True)
    args = parser.parse_args()
    print("输入命令：%s,%s,%s" % (args.meta, args.output, args.downloadImage))
    start_convert(args.meta, args.output, args.downloadImage)
