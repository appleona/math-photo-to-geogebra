#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键在浏览器中打开 GeoGebra 交互图形（零依赖，纯标准库）

原理：
  GeoGebra 官方提供 deployggb.js 嵌入库，支持通过 ggbBase64 参数
  直接加载 .ggb 文件内容，无需上传到云端、无需登录。

使用方法：
    python upload_to_geogebra.py path/to/your.ggb

输出：
    1. 生成同名 .html 文件（自包含，可离线查看）
    2. 自动用系统默认浏览器打开
    3. 用户可交互操作（拖动点、查看数值）

如需真正的 geogebra.org 分享链接，仍需手动登录后保存到云端。
"""

import sys
import os
import base64
import webbrowser


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; font-family: sans-serif; }}
        #header {{
            background: #f0f0f0; padding: 8px 16px; font-size: 14px;
            border-bottom: 1px solid #ccc; display: flex; align-items: center;
        }}
        #header span {{ margin-right: 20px; }}
        #header a {{
            color: #0066cc; text-decoration: none; margin-left: auto;
        }}
        #ggb-container {{ width: 100vw; height: calc(100vh - 36px); }}
    </style>
</head>
<body>
    <div id="header">
        <span><b>{title}</b></span>
        <span>文件: {filename}</span>
        <a href="https://www.geogebra.org/classic" target="_blank">
            登录 GeoGebra 保存可获取分享链接
        </a>
    </div>
    <div id="ggb-container"></div>
    <script>
        var ggbApp = new GGBApplet({{
            appName: "classic",
            width: window.innerWidth,
            height: window.innerHeight - 36,
            ggbBase64: "{ggb_base64}",
            showAlgebraInput: true,
            showToolBar: true,
            showMenuBar: true,
            showResetIcon: true,
            enableLabelDrags: true,
            enableShiftDragZoom: true,
            capturingThreshold: 3,
            appletOnLoad: function() {{
                console.log("[OK] GeoGebra loaded successfully");
            }}
        }}, true);
        ggbApp.inject('ggb-container');
    </script>
</body>
</html>'''


def open_in_browser(ggb_path):
    """
    读取 .ggb 文件，生成 HTML，用浏览器打开。
    零依赖，纯 Python 标准库。
    """
    if not os.path.exists(ggb_path):
        print("[ERROR] File not found: " + ggb_path)
        return False

    # 读取 ggb 并转 base64
    with open(ggb_path, 'rb') as f:
        ggb_data = f.read()
    b64 = base64.b64encode(ggb_data).decode('ascii')

    filename = os.path.basename(ggb_path)
    title = os.path.splitext(filename)[0]
    html_path = os.path.splitext(ggb_path)[0] + '.html'

    # 生成 HTML
    html = HTML_TEMPLATE.format(
        title=title,
        filename=filename,
        ggb_base64=b64
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("=" * 60)
    print("[OK] Generated: " + html_path)
    print("=" * 60)
    print("Features:")
    print("  - Interactive geometry (drag points, zoom, pan)")
    print("  - Works offline after first load (deployggb.js cached)")
    print("  - No GeoGebra account required")
    print("")
    print("To get a shareable geogebra.org link:")
    print("  1. Open the page below")
    print("  2. Click 'Login GeoGebra to save' in top-right")
    print("  3. Login and save -> get link like geogebra.org/m/xxxx")
    print("=" * 60)

    # 自动打开浏览器
    abs_path = os.path.abspath(html_path)
    # Windows 用 file:// 协议
    url = 'file:///' + abs_path.replace('\\', '/')
    webbrowser.open(url, new=2)
    print("[OK] Browser opened: " + url)
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_to_geogebra.py <path/to/file.ggb>")
        print("Example: python upload_to_geogebra.py test_problem.ggb")
        sys.exit(1)

    ggb_path = sys.argv[1]
    success = open_in_browser(ggb_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
