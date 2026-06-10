#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEPRECATED] 图片处理工具

状态：已弃用。图片嵌入功能已移除。

原因：
  GeoGebra 6.0 Classic 对 base64 内嵌图片支持不稳定，
  超过 ~10KB 即无法加载。原题图片（通常100KB+）嵌入后必然失败。

替代方案：
  使用 Text 命令显示题目文字，见 SKILL.md 核心原则2。
"""


def main():
    print("=" * 60)
    print("[INFO] 此工具已弃用")
    print("=" * 60)
    print("图片嵌入功能已移除。")
    print("原因：GeoGebra 6.0 无法加载大于 ~10KB 的 base64 图片。")
    print("")
    print("替代方案：在 XML 中使用 Text 命令显示题目文字。")
    print("示例：")
    print('  <command name="Text">')
    print('      <input a0="&quot;【题目】等腰直角三角形ABC...&quot;"/>')
    print('      <input a1="(-10, 8)"/>')
    print('      <output a0="title1"/>')
    print('  </command>')
    print("=" * 60)


if __name__ == '__main__':
    main()
