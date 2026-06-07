#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键上传.ggb文件到GeoGebra网页版并获取分享链接

使用方法:
    python upload_to_geogebra.py path/to/your.ggb

输出:
    分享链接 (如 https://www.geogebra.org/classic#matrix/xxxxxx)
"""

import sys
import os
import time


def upload_and_get_link(ggb_path):
    """
    使用Playwright上传.ggb文件到GeoGebra网页版
    
    注意: 需要安装playwright
    pip install playwright
    playwright install chromium
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] 需要安装playwright: pip install playwright")
        print("[ERROR] 然后运行: playwright install chromium")
        return None
    
    if not os.path.exists(ggb_path):
        print(f"[ERROR] 文件不存在: {ggb_path}")
        return None
    
    print(f"[INFO] 正在上传: {ggb_path}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 可见模式，方便调试
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        try:
            # 1. 打开GeoGebra网页版
            print("[INFO] 打开GeoGebra网页版...")
            page.goto("https://www.geogebra.org/classic", wait_until="networkidle")
            time.sleep(3)
            
            # 2. 点击"打开"菜单（左上角汉堡菜单）
            print("[INFO] 点击菜单...")
            # GeoGebra的菜单按钮
            menu_button = page.locator('button[title="Open Menu"]').first
            if menu_button.count() == 0:
                menu_button = page.locator('div[role="button"]').filter(has_text="☰").first
            
            if menu_button.count() > 0:
                menu_button.click()
                time.sleep(1)
            
            # 3. 点击"打开"选项
            print("[INFO] 点击'打开'...")
            open_option = page.locator('text=Open').first
            if open_option.count() > 0:
                open_option.click()
                time.sleep(1)
            
            # 4. 点击"浏览"选择文件
            print("[INFO] 选择文件上传...")
            # 找到文件输入框
            file_input = page.locator('input[type="file"]').first
            if file_input.count() > 0:
                file_input.set_input_files(ggb_path)
                time.sleep(3)  # 等待上传和加载
            else:
                print("[WARN] 未找到文件输入框，尝试拖放方式...")
                # 拖放方式
                page.evaluate(f"""
                    async () => {{
                        const file = await fetch('file://{ggb_path}').then(r => r.blob());
                        const dt = new DataTransfer();
                        dt.items.add(new File([file], '{os.path.basename(ggb_path)}'));
                        const event = new DragEvent('drop', {{dataTransfer: dt}});
                        document.body.dispatchEvent(event);
                    }}
                """)
                time.sleep(5)
            
            # 5. 等待加载完成，获取URL
            print("[INFO] 等待加载完成...")
            time.sleep(3)
            
            current_url = page.url
            print(f"[INFO] 当前URL: {current_url}")
            
            # 如果URL包含material ID，说明已保存
            if "material" in current_url or "classic#matrix" in current_url:
                print(f"[OK] 分享链接: {current_url}")
                return current_url
            else:
                # 尝试点击保存按钮获取链接
                print("[INFO] 尝试保存获取链接...")
                save_button = page.locator('button[title="Save"]').first
                if save_button.count() > 0:
                    save_button.click()
                    time.sleep(3)
                    current_url = page.url
                
                print(f"[OK] 访问链接: {current_url}")
                return current_url
                
        except Exception as e:
            print(f"[ERROR] 上传失败: {e}")
            # 截图保存以便调试
            page.screenshot(path="upload_error.png")
            print("[INFO] 错误截图已保存: upload_error.png")
            return None
        finally:
            browser.close()


def main():
    if len(sys.argv) < 2:
        print("用法: python upload_to_geogebra.py <path/to/file.ggb>")
        print("示例: python upload_to_geogebra.py test_problem.ggb")
        sys.exit(1)
    
    ggb_path = sys.argv[1]
    link = upload_and_get_link(ggb_path)
    
    if link:
        print("\n" + "="*60)
        print("分享链接 (用户可直接在浏览器打开):")
        print(link)
        print("="*60)
    else:
        print("\n[FAIL] 上传失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
