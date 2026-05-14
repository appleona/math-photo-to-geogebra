#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简 GeoGebra 打包工具
将 XML 内容打包为 .ggb 文件

使用方法:
    # 方式1: 从文件读取
    python pack_ggb.py output.ggb < input.xml
    
    # 方式2: 通过管道
    echo '<xml...>' | python pack_ggb.py output.ggb
    
    # 方式3: 使用 -i 参数
    python pack_ggb.py output.ggb -i input.xml
"""

import argparse
import sys
import zipfile


def pack_ggb(xml_content: str, output_path: str):
    """将 XML 内容打包为 .ggb 文件"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('geogebra.xml', xml_content.encode('utf-8'))
    print(f"[OK] 已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='将 GeoGebra XML 打包为 .ggb 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s output.ggb < input.xml
  echo '<xml...>' | %(prog)s output.ggb
  %(prog)s output.ggb -i input.xml
        """
    )
    parser.add_argument('output', help='输出 .ggb 文件路径')
    parser.add_argument('-i', '--input', help='输入 XML 文件路径（默认从 stdin 读取）')
    
    args = parser.parse_args()
    
    # 读取 XML 内容
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    else:
        xml_content = sys.stdin.read()
    
    # 打包
    pack_ggb(xml_content, args.output)


if __name__ == '__main__':
    main()
