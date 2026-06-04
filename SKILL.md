---
name: math-photo-to-geogebra
description: 将简体中文数学题（七到九年级平面几何、直角坐标系函数）转换为GeoGebra交互图形，支持OCR文本显示和动态演示。Use when users need to (1) Convert math problem images to GeoGebra diagrams, (2) Recreate geometric figures with proper constraints, (3) Generate .ggb files with OCR text and dynamic sliders.
---

# 数学拍照转 GeoGebra

将数学题图片转换为可交互的 GeoGebra 图形文件(.ggb)，支持题目文本显示和动态演示。

---

## 核心功能

1. **图形生成** - 使用GeoGebra原生工具构建几何图形
2. **OCR文本** - 显示题目文字（替代图片嵌入）
3. **动态演示** - 滑块控制参数、约束点移动
4. **约束保证** - 点在线段上、中点等使用正确工具实现

---

## 核心原则

### 使用GeoGebra原生工具

**必须**使用GeoGebra提供的工具命令：

| 需求 | 正确工具 | 错误做法 |
|------|----------|----------|
| 点在线段上 | `Point`工具 | 直接写坐标 |
| 中点 | `Midpoint`工具 | 坐标计算 |
| 交点 | `Intersect`工具 | 手动计算 |
| 垂线 | `PerpendicularLine` | 斜率计算 |

---

## 工作流程

```
用户图片 → OCR识别 → 分析几何结构 → 生成XML → 打包.ggb
                ↓              ↓
           提取文字     构建图形+约束+文本
```

---

## 正确格式

### 点约束到线段上

```xml
<!-- 1. 先创建线段 -->
<command name="Segment">
    <input a0="B" a1="C"/>
    <output a0="sideBC"/>
</command>
<element type="segment" label="sideBC">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>

<!-- 2. 使用Point工具约束到线段上 -->
<command name="Point">
    <input a0="sideBC"/>    <!-- 约束到线段 -->
    <output a0="E"/>
</command>
<element type="point" label="E">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
</element>
```

### 中点工具

```xml
<command name="Midpoint">
    <input a0="A" a1="E"/>  <!-- 输入两个端点 -->
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
</element>
```

### 题目文本显示

```xml
<!-- 在GeoGebra中显示题目文字 -->
<command name="Text">
    <input a0="&quot;【题目】菱形ABCD边长8，∠ABC=120°...&quot;"/>
    <input a1="(-10, 8)"/>
    <output a0="problemText"/>
</command>
<element type="text" label="problemText">
    <show object="true" label="false"/>
    <fontSize val="11"/>
</element>
```

> ⚠️ **注意**：原题图片base64嵌入在GeoGebra 6.0中不稳定（>10KB即失败），建议使用文本描述替代。

生成的XML：

```xml
<command name="Image">
    <input a0="&quot;data:image/png;base64,iVBORw0KGgo...&quot;"/>
    <input a1="(-2, -8)"/>
    <input a2="(14, 0)"/>
    <input a3="(0, 10)"/>
    <output a0="originalFigure"/>
</command>
<element type="image" label="originalFigure">
    <show object="true" label="false"/>
</element>
```

---

## 使用工具

### 打包ggb

```bash
echo '<xml...>' | python scripts/pack_ggb.py output.ggb
```

### 带图片嵌入

```bash
python create_with_image.py problem.jpg output_name
```

---

## 图形校对

生成的ggb文件布局：

```
┌─────────────────────────────┐
│     【生成图形】              │
│     蓝色几何图形              │
│     (使用GeoGebra工具生成)    │
├─────────────────────────────┤
│        分隔线                 │
├─────────────────────────────┤
│     【原题图片】              │
│     嵌入的题目原图            │
│     (用于对比参考)            │
└─────────────────────────────┘
```

### 校对清单

- [ ] **顶点位置** - 生成图形的顶点与原图是否对应
- [ ] **边线** - 线段连接关系是否正确
- [ ] **角度** - 特殊角度是否正确
- [ ] **比例** - 边长比例是否大致正确
- [ ] **标注** - 点和线的标签是否对应

---

## 完整示例

见 `references/image-embedding.md` 和 `demo_image_embedding.ggb`

---

## 参考资料

- `references/xml-cheatsheet.md` - XML快速参考
- `references/common-patterns.md` - 常见几何构造模式
- `references/image-embedding.md` - 图片嵌入与校对
- `scripts/image_utils.py` - 图片处理工具
