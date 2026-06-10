---
name: math-photo-to-geogebra
version: "1.2.0"
description: 将简体中文数学题（七到九年级平面几何、直角坐标系函数）转换为GeoGebra交互图形，支持OCR文本显示和图片嵌入校对。Use when users need to (1) Convert math problem images to GeoGebra diagrams, (2) Recreate geometric figures with proper constraints, (3) Generate .ggb files with OCR text and original image for comparison.
---

# 数学拍照转 GeoGebra

将数学题图片转换为可交互的 GeoGebra 图形文件(.ggb)，支持原题图片嵌入和图形校对。

---

## 核心功能

1. **结构化理解** - 从题目文本/图像中提取几何对象、约束条件、已知/未知信息
2. **约束建模** - 使用GeoGebra原生工具构建几何约束关系
3. **OCR文本** - 显示题目文字与关键标注
4. **图片嵌入** - 嵌入原题图片用于对比校对
5. **质量验证** - 多项检查确保约束正确、图形合理

---

## 核心原则

### 原则1：先理解，后建模

生成XML之前，必须先完成**题目结构化理解**。禁止直接凭直觉写坐标！

### 原则2：文本框间距规范

所有文本框之间必须保持足够间距，避免重叠：

| 规范 | 要求 | 示例 |
|------|------|------|
| **行间距** | 相邻文本框y坐标差 >= 1.5个单位 | `y=8` 和 `y=6` 差2单位 |
| **分组间距** | 题目/答案/分析之间 >= 2个单位 | 题目在y=8，答案在y=5 |
| **与图形间距** | 文本与最近图形 >= 1个单位 | 文本y=5，图形顶点y<=4 |
| **边距** | 文本不超出坐标系边界 | 检查xZero/yZero和scale |

### 原则3：图形方向与原图一致

生成图形的方向、顶点顺序必须与原题图片一致，方便对照：
- 原图底边水平 => 生成图形底边也必须水平
- 顶点标签顺序（顺时针/逆时针）与原图一致
- 对称轴方向与原图一致

### 原则4：使用GeoGebra原生工具

**必须**使用GeoGebra提供的工具命令实现约束：

| 约束类型 | 正确工具 | 错误做法 |
|----------|----------|----------|
| 点在线段上 | `Point`工具（输入线段） | 直接写坐标 |
| 中点 | `Midpoint`工具 | 坐标计算 |
| 交点 | `Intersect`工具 | 手动计算 |
| 垂线 | `PerpendicularLine` | 斜率计算 |
| 平行线 | `Line`工具（输入点+平行线） | 斜率相同 |
| 角平分线 | `AngleBisector`工具 | 手动画线 |
| 圆+半径 | `Circle`工具（圆心+半径/点） | 手动画圆 |
| 垂足 | `PerpendicularLine`+`Intersect` | 投影计算 |
| 线段等长 | `Segment`+长度标注 | 目测坐标 |
| 角度标注 | `Angle`工具 | 文本标注冒充 |

---

## 工作流程（强制）

```
用户图片 → [步骤1] 题目结构化理解
              ↓
         [步骤2] 约束关系建模
              ↓
         [步骤3] 生成XML
              ↓
         [步骤4] 嵌入图片
              ↓
         [步骤5] 打包ggb + 质量验证
```

### 步骤1：题目结构化理解（必须先完成）

对每道题，在生成XML前必须先明确以下信息：

#### 1.1 题目类型分类

| 类型 | 识别关键词 | 典型特征 |
|------|-----------|----------|
| **静态几何** | 求长度、面积、角度 | 固定图形，所有点位置确定 |
| **动态几何** | 动点、移动、范围、最值 | 存在可拖动点，探究变化规律 |
| **函数图像** | 抛物线、直线、交点 | 坐标系背景，有函数表达式 |
| **尺规作图** | 作图、作一条线、构造 | 需要保留作图痕迹 |
| **证明题** | 求证、证明 | 需要标注已知条件和辅助线 |

#### 1.2 几何对象提取清单

```
□ 点：顶点（A,B,C...）、特殊点（中点、垂足、交点、动点）
□ 线：边、对角线、中线、高线、角平分线、中位线、延长线、辅助线
□ 圆：圆心、半径、直径、切线、弦
□ 角：直角、等角、特殊角（30°、45°、60°）
□ 形：三角形、四边形（平行四边形/矩形/菱形/正方形/梯形）、圆
```

#### 1.3 约束条件提取（关键！）

从题目文本中识别以下约束类型：

**位置约束：**
- "点E在BC上" → `Point`约束到线段
- "延长BA到F" → 在BA延长线上创建点
- "P在CD上移动" → 动点约束

**度量约束：**
- "AB=10, AC=6" → 线段长度（用坐标实现比例，或用`Distance`标注）
- "∠B=90°" → 直角约束（可用PerpendicularLine或角度标注）
- "半径为5" → 圆约束

**关系约束：**
- "中点" → `Midpoint`工具
- "平行" → `Line`工具（输入点+平行线）
- "垂直" → `PerpendicularLine`工具
- "角平分线" → `AngleBisector`工具
- "相切" → `Tangent`工具
- "等腰/等边" → 边长相等（通过坐标对称性实现）

**动态约束：**
- "动点P从C运动到D" → 点在线段上可拖动
- "求MN的最大值" → 轨迹或测量工具

#### 1.4 已知 vs 未知标记

| 元素类型 | 标记方式 | 说明 |
|----------|----------|------|
| 已知条件 | 黑色实线、正常粗细 | 题目给定的边、角 |
| 所求目标 | **红色粗线**、加粗显示 | 需要求解的线段/角 |
| 辅助线 | **虚线**、灰色或绿色 | 为解题添加的线 |
| 隐藏条件 | 标注文本说明 | 如"AB=AC（等腰）" |

---

### 步骤2：约束关系建模

根据步骤1提取的信息，建立约束优先级：

```
1. 先建基础形（三角形/四边形的顶点）
2. 再建关系约束（中点、平行、垂直、点在线上）
3. 然后建辅助元素（延长线、辅助线、圆）
4. 最后建标注（长度、角度、OCR文本）
```

**重要：** 如果题目给出具体长度（如AB=10），先按比例设定坐标，再用`Text`或`Caption`标注实际长度值。

---

### 步骤3：生成XML

参照 `references/xml-cheatsheet.md` 和 `references/common-patterns.md` 生成XML。

**必须遵守的格式规则：**
1. 所有`"`在XML属性中必须转义为`&quot;`
2. 点标签用大写字母（A, B, C...），线段用小写字母或描述性名称（sideAB, midline）
3. 动态点用蓝色(r=0,g=0,b=255)，中点用紫色(r=255,g=0,b=255)，所求用红色(r=255,g=0,b=0)
4. 辅助线用虚线(type=1)，实线用type=0

---

### 步骤4：嵌入图片（可选，受限制）

如需对比校对，可使用 `scripts/image_utils.py` 将原题图片嵌入ggb文件底部。

> **重要限制**：GeoGebra 6.0 Classic 对 base64 内嵌图片支持不稳定，超过 ~10KB 即可能加载失败。原题图片（通常100KB+）大概率无法显示。
>
> **替代方案**：使用 Text 命令显示题目文字（见原则2），这是更可靠的方式。

---

### 步骤5：质量验证

使用 `references/quality-check.md` 的清单逐项验证，重点检查：
- 约束工具使用是否正确（是否用了Midpoint而不是手动坐标）
- 动态点是否能拖动且保持约束
- 所求目标是否用红色突出显示
- OCR文本是否完整

---

## 常见题型建模指南

### 题型A：静态几何计算题

**特征：** 求长度、面积、角度

**建模要点：**
- 所有点用固定坐标（按给定比例）
- 特殊约束用工具实现（中点、垂线等）
- 所求线段用**红色加粗**
- 已知长度用`caption`或文本标注

### 题型B：动态几何探究题

**特征：** 动点、求范围/最值

**建模要点：**
- 动点必须用`Point`工具约束到线段/圆上（可拖动）
- 依赖动点的元素会自动更新
- 添加轨迹或测量显示变化
- 图片嵌入后可以用滑块验证特殊位置

### 题型C：函数图像题

**特征：** 抛物线、直线、坐标系

**建模要点：**
- 开启坐标轴和网格
- 函数用`expression`元素定义
- 交点用`Intersect`工具
- 关键点（顶点、交点）标注坐标

### 题型D：几何证明题

**特征：** 求证、证明

**建模要点：**
- 用不同颜色区分已知条件（黑）、辅助线（绿/虚线）、所求证（红）
- 添加文本框标注"已知：...""求证：..."
- 保留完整的辅助线构造痕迹

---

## 约束工具速查

### 基础约束

```xml
<!-- 点在线段上（可拖动） -->
<command name="Point">
    <input a0="sideBC"/>
    <output a0="E"/>
</command>

<!-- 中点 -->
<command name="Midpoint">
    <input a0="A" a1="B"/>
    <output a0="M"/>
</command>

<!-- 交点 -->
<command name="Intersect">
    <input a0="line1" a1="line2"/>
    <output a0="D"/>
</command>
```

### 高级约束

```xml
<!-- 角平分线 -->
<command name="AngleBisector">
    <input a0="B" a1="A" a2="C"/>  <!-- ∠BAC的平分线 -->
    <output a0="bisector"/>
</command>

<!-- 过点作平行线 -->
<command name="Line">
    <input a0="C"/>                 <!-- 经过的点 -->
    <input a1="lineAB"/>            <!-- 平行的线 -->
    <output a0="parallel"/>
</command>

<!-- 过点作垂线 -->
<command name="PerpendicularLine">
    <input a0="C"/>                 <!-- 经过的点 -->
    <input a1="sideAB"/>            <!-- 垂直的线段/线 -->
    <output a0="perp"/>
</command>

<!-- 圆（圆心+半径） -->
<command name="Circle">
    <input a0="O"/>                 <!-- 圆心 -->
    <input a1="3"/>                 <!-- 半径（数值或线段） -->
    <output a0="c1"/>
</command>

<!-- 圆的切线（过圆外一点） -->
<command name="Tangent">
    <input a0="P"/>                 <!-- 圆外点 -->
    <input a1="c1"/>                <!-- 圆 -->
    <output a0="t1"/>
    <output a0="t2"/>               <!-- 两个切点/切线 -->
</command>

<!-- 角度 -->
<command name="Angle">
    <input a0="B" a1="A" a2="C"/>  <!-- ∠BAC -->
    <output a0="alpha"/>
</command>
```

详见 `references/common-patterns.md` 获取完整模式。

---

## 完整示例

见 `references/common-patterns.md` 中的完整示例和 `references/image-embedding.md` 的图片嵌入指南。

---

## 参考资料

- `references/constraint-guide.md` - 约束建模深度指南
- `references/xml-cheatsheet.md` - XML快速参考与完整元素列表
- `references/common-patterns.md` - 常见几何构造模式（含圆、切线、轨迹等）
- `references/image-embedding.md` - 图片嵌入与限制说明
- `references/quality-check.md` - 质量复查机制与约束验证
- `references/problem-analysis-guide.md` - 人教版题目理解指南
- `references/dynamic-demo-patterns.md` - 动态演示XML模板
- `references/common-misunderstandings.md` - 常见理解偏差与修正
- `scripts/image_utils.py` - 图片处理工具
- `scripts/pack_ggb.py` - ggb打包工具
