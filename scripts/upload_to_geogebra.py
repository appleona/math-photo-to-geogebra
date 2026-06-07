#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEPRECATED] GeoGebra 云端上传与分享链接功能

状态：已弃用。GeoGebra 官方要求登录后才能上传保存到云端，
      因此无法通过纯脚本实现"一键获取分享链接"。

替代方案：
  1. 用 GeoGebra Desktop 打开 .ggb 文件
  2. 文件 -> 保存到 GeoGebra -> 登录账号 -> 获得分享链接

如需在浏览器中直接查看（无需登录），可将 .ggb 文件用
GeoGebra 官方嵌入代码手动转为 HTML，参考：
https://wiki.geogebra.org/en/Reference:GeoGebra_Apps_Embedding
"""

import sys


def main():
    print("=" * 60)
    print("[INFO] 此功能已弃用")
    print("=" * 60)
    print("原因：GeoGebra 云端保存必须登录账号，脚本无法绕过。")
    print("")
    print("获取分享链接的手动步骤：")
    print("  1. 用 GeoGebra Classic 6 打开 .ggb 文件")
    print("  2. 文件 -> 保存到 GeoGebra (Ctrl+S)")
    print("  3. 登录账号")
    print("  4. 获得链接：https://www.geogebra.org/m/xxxx")
    print("=" * 60)
    sys.exit(1)


if __name__ == '__main__':
    main()
