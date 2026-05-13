# Math Photo to GeoGebra Skill

将数学题图片转换为GeoGebra交互图形文件的Skill。

## 适用场景

- 拍照识别初中数学几何题（七到九年级）
- 将平面几何、函数图像转换为可交互的GeoGebra图形
- 生成带有OCR文本和图片校对的.ggb文件

## 快速开始

### 1. 基本使用流程

```python
# 步骤1: 分析题目图片，提取几何结构
# 步骤2: 生成GeoGebra XML
# 步骤3: 使用pack_ggb.py打包为.ggb文件

python scripts/pack_ggb.py output.ggb -i input.xml
```

### 2. 主要工具脚本

| 脚本 | 功能 |
|------|------|
| `scripts/pack_ggb.py` | 将XML打包为.ggb文件 |
| `scripts/image_utils.py` | 图片处理工具（base64编码等） |

### 3. 参考文档

| 文档 | 内容 |
|------|------|
| `references/problem-analysis-guide.md` | 人教版各章节题目理解指南 |
| `references/dynamic-demo-patterns.md` | 动态演示XML模板 |
| `references/common-misunderstandings.md` | 常见偏差与修正 |
| `references/common-patterns.md` | 常见几何构造模式 |
| `references/xml-cheatsheet.md` | XML语法速查 |
| `references/quality-check.md` | 质量检查清单 |

## 核心原则

### 必须使用GeoGebra原生工具

| 需求 | 正确工具 | 错误做法 |
|------|----------|----------|
| 点在线段上 | `Point`工具 | 直接写坐标 |
| 中点 | `Midpoint`工具 | 坐标计算 |
| 交点 | `Intersect`工具 | 手动计算 |
| 垂线 | `PerpendicularLine` | 斜率计算 |
| 对称 | `Mirror`工具 | 坐标变换 |
| 旋转 | `Rotate`工具 | 三角函数计算 |

### 动态演示优先

- **参数问题** → 使用滑块(slider)
- **动点问题** → 使用约束点(Point工具)
- **变换问题** → 使用几何变换工具

## 示例

### 生成一次函数动态演示

```python
import zipfile

xml = '''<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<euclidianView>
    <coordSystem xZero="500" yZero="400" scale="50"/>
    <evSettings axes="true" grid="true"/>
</euclidianView>
<construction>
    <!-- 滑块控制斜率m -->
    <element type="numeric" label="m">
        <value val="0.5"/>
        <slider min="0" max="2" step="0.01"/>
        <show object="true" label="true"/>
    </element>
    
    <!-- 动态直线 y = mx -->
    <element type="function" label="f">
        <expression label="f" exp="m*x" type="function"/>
        <show object="true" label="true"/>
        <objColor r="0" g="128" b="0"/>
    </element>
</construction>
</geogebra>'''

with zipfile.ZipFile('output.ggb', 'w') as zf:
    zf.writestr('geogebra.xml', xml.encode('utf-8'))
```

### 生成动点几何题

```xml
<!-- 动点M约束在线段AC上 -->
<command name="Point">
    <input a0="segmentAC"/>
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0"/>
</element>
```

## 文件结构

```
math-photo-to-geogebra/
├── SKILL.md                      # Skill定义文件
├── README.md                     # 本文件
├── scripts/
│   ├── pack_ggb.py              # 打包工具
│   └── image_utils.py           # 图片工具
└── references/
    ├── problem-analysis-guide.md
    ├── dynamic-demo-patterns.md
    ├── common-misunderstandings.md
    ├── common-patterns.md
    ├── xml-cheatsheet.md
    ├── quality-check.md
    └── image-embedding.md
```

## 注意事项

1. **XML编码**: 必须使用UTF-8编码
2. **特殊字符**: 引号需要转义为 `&quot;`
3. **坐标系**: 默认scale=50，根据需要调整
4. **动态演示**: 优先使用滑块和约束点，而非静态坐标

## 依赖

- Python 3.6+
- 标准库: zipfile, argparse, sys, base64

无需额外安装第三方库。
