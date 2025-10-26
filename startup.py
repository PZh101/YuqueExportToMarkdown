# import sys
import argparse
from lake.lake_setup import start_convert

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--meta', help="lake文件的meta.json路径", type=str)
    parser.add_argument('-l', '--lake', help="lakebook文件的路径", type=str)
    parser.add_argument('-o', '--output', help="生成markdown的根路径", type=str)
    parser.add_argument('-d', '--downloadImage', help="是否下载图片", type=bool, default=True)
    parser.add_argument('-s', '--skip-existing-resources', help="是否跳过本地已存在的图片和附件文件", action='store_true')
    args = parser.parse_args()
    print("输入命令：%s,%s,%s,%s" % (args.meta, args.output, args.downloadImage, args.skip_existing_resources))
    start_convert(args.meta, args.lake, args.output, args.downloadImage, args.skip_existing_resources)
