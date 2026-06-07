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

### 原则1：文本框间距规范

所有文本框之间必须保持足够间距，避免重叠：

| 规范 | 要求 | 示例 |
|------|------|------|
| **行间距** | 相邻文本框y坐标差 ≥ 1.5个单位 | `y=8` 和 `y=6` 差2单位 ✓ |
| **分组间距** | 题目/答案/分析之间 ≥ 2个单位 | 题目在y=8，答案在y=5 |
| **与图形间距** | 文本与最近图形 ≥ 1个单位 | 文本y=5，图形顶点y≤4 |
| **边距** | 文本不超出坐标系边界 | 检查xZero/yZero和scale |

**示例布局（正确）：**
```
y=9  【题目】第一行文字
y=7  【题目】第二行文字
y=5  【答案】xxx
y=3  【分析】关键提示
y=0  ───── 图形区域 ─────
```

**错误示例（重叠）：**
```
y=8  【题目】第一行文字
y=7  【题目】第二行文字    ← 间距只有1，可能重叠
y=6  【答案】xxx            ← 与上行紧贴，字体大时重叠
```

### 原则2：图形方向与原图一致

生成图形的方向、顶点顺序必须与原题图片一致，方便对照：

| 要素 | 要求 |
|------|------|
| **底边方向** | 保持水平（如原图底边水平，则生成图形底边也水平） |
| **顶点顺序** | 按原图顺时针/逆时针顺序标注A、B、C、D |
| **相对位置** | 上/下/左/右关系与原图一致 |
| **对称轴** | 竖直对称轴保持竖直，水平对称轴保持水平 |

**示例：** 原图菱形AC水平、BD竖直 → 生成图形也应AC水平、BD竖直，不要旋转90°。

### 原则3：使用GeoGebra原生工具

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
用户图片 → OCR识别 → 分析几何结构 → 生成XML → 打包.ggb → 上传网页 → 分享链接
                ↓              ↓                        ↓
           提取文字     构建图形+约束+文本          自动上传
```

### 一键网页分享

生成.ggb文件后，自动上传到GeoGebra网页版并获取分享链接：

```bash
python scripts/upload_to_geogebra.py output.ggb
# 输出: https://www.geogebra.org/classic#matrix/xxxxxx
```

用户无需安装软件，点击链接即可在浏览器中打开交互式图形。

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

### 带题目文本

```xml
<!-- 在图形上方显示题目文字 -->
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

---

## 图形校对

生成的ggb文件布局：

```
┌─────────────────────────────┐
│     【题目文本】              │
│     原题关键信息              │
│     (Text命令显示)            │
├─────────────────────────────┤
│        分隔线                 │
├─────────────────────────────┤
│     【生成图形】              │
│     蓝色几何图形              │
│     (使用GeoGebra工具生成)    │
└─────────────────────────────┘
```

### 校对清单

**几何正确性：**
- [ ] **顶点位置** - 生成图形的顶点与原图是否对应
- [ ] **边线** - 线段连接关系是否正确
- [ ] **角度** - 特殊角度是否正确
- [ ] **比例** - 边长比例是否大致正确
- [ ] **标注** - 点和线的标签是否对应

**方向一致性（对照原图）：**
- [ ] **底边方向** - 生成图形底边与原图方向一致（通常为水平）
- [ ] **顶点顺序** - A→B→C→D顺序与原图一致（顺时针/逆时针）
- [ ] **相对位置** - 上下左右关系与原图一致
- [ ] **对称关系** - 对称轴方向与原图一致

**文本间距（避免重叠）：**
- [ ] **行间距** - 相邻文本框y坐标差 ≥ 1.5
- [ ] **分组间距** - 题目/答案/分析之间 ≥ 2
- [ ] **图形间距** - 文本与最近图形 ≥ 1
- [ ] **边界检查** - 所有文本在可视范围内

---

## 完整示例

见 `references/problem-analysis-guide.md` 和 `references/dynamic-demo-patterns.md`

---

## 参考资料

- `references/xml-cheatsheet.md` - XML快速参考
- `references/common-patterns.md` - 常见几何构造模式
- `references/problem-analysis-guide.md` - 题目理解指南
- `references/dynamic-demo-patterns.md` - 动态演示模式
- `scripts/pack_ggb.py` - XML打包工具
