#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理工具 - 用于将题目图片嵌入ggb文件
"""

import base64
import io
from PIL import Image


def image_to_base64(image_path):
    """
    将图片转为base64编码（完整图片）
    
    Args:
        image_path: 图片路径
        
    Returns:
        base64字符串，格式：data:image/png;base64,xxx
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()
    base64_str = base64.b64encode(image_data).decode('utf-8')
    
    # 检测图片格式
    ext = image_path.split('.')[-1].lower()
    if ext == 'png':
        mime = 'image/png'
    elif ext in ['jpg', 'jpeg']:
        mime = 'image/jpeg'
    elif ext == 'gif':
        mime = 'image/gif'
    else:
        mime = 'image/png'
    
    return f"data:{mime};base64,{base64_str}"


def crop_image(image_path, crop_box=None):
    """
    裁剪图片
    
    Args:
        image_path: 图片路径
        crop_box: 裁剪区域 (left, top, right, bottom)
                 为None则返回原图
    
    Returns:
        PIL Image对象
    """
    img = Image.open(image_path)
    
    if crop_box:
        img = img.crop(crop_box)
    
    return img


def crop_and_encode(image_path, crop_box=None):
    """
    裁剪图片并转为base64
    
    Args:
        image_path: 图片路径
        crop_box: 裁剪区域 (left, top, right, bottom)
    
    Returns:
        base64字符串
    """
    img = crop_image(image_path, crop_box)
    
    # 转为PNG并编码
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{base64_str}"


def create_image_xml(base64_data, label="originalFigure", 
                     pos=(-8, -6), width=16, height=12):
    """
    创建嵌入图片的XML
    
    Args:
        base64_data: base64编码的图片数据
        label: 图片标签
        pos: 左下角坐标 (x, y)
        width: 宽度
        height: 高度
        
    Returns:
        XML字符串
    """
    # 转义base64中的引号
    safe_data = base64_data.replace('"', '&quot;')
    
    xml = f'''<command name="Image">
    <input a0="&quot;{safe_data}&quot;"/>
    <input a1="({pos[0]}, {pos[1]})"/>
    <input a2="({width}, 0)"/>
    <input a3="(0, {height})"/>
    <output a0="{label}"/>
</command>
<element type="image" label="{label}">
    <show object="true" label="false"/>
</element>'''
    
    return xml


# 测试代码
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python image_utils.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # 测试转换为base64
    print("转换图片为base64...")
    base64_data = image_to_base64(image_path)
    print(f"Base64长度: {len(base64_data)} 字符")
    print(f"Base64前100字符: {base64_data[:100]}...")
    
    # 测试生成XML
    print("\n生成XML...")
    xml = create_image_xml(base64_data)
    print(xml[:500])
    print("...")
