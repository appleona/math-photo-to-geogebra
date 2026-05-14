# Math Photo to GeoGebra

拍照识别初中数学题，转换为可交互的 GeoGebra 图形文件（.ggb）。

## 功能特性

- 📷 **拍照识别** - 将数学题图片转换为 GeoGebra 交互图形
- 🔧 **原生工具** - 使用 GeoGebra 原生工具（非手动坐标计算）
- 🎚️ **动态演示** - 支持滑块控制参数、约束动点
- 📝 **OCR 文本** - 在图形中显示题目原文
- 🖼️ **图片嵌入** - 嵌入原题图片用于对比校对
- 📚 **完整参考** - 涵盖人教版七至九年级数形结合内容

## 适用场景

| 题型 | 动态特性 | 示例 |
|------|----------|------|
| 一次函数参数范围 | 滑块控制斜率 m | `y=mx` 绕原点旋转 |
| 动点几何 | 约束点在线段上移动 | 求线段和最小值 |
| 几何变换 | 旋转/翻折动画 | 矩形折叠、三角形旋转 |
| 函数图像 | 实时显示交点坐标 | 二次函数与几何综合 |

## 快速开始

### 1. 生成 XML

```xml
<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<euclidianView>
    <coordSystem xZero="500" yZero="400" scale="50" yscale="50"/>
    <evSettings axes="true" grid="true"/>
</euclidianView>
<construction>
    <!-- 滑块控制斜率 m -->
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
</geogebra>
```

### 2. 打包为 .ggb

```bash
python scripts/pack_ggb.py output.ggb -i input.xml
```

### 3. 在 GeoGebra 中打开

双击 `.ggb` 文件即可在 GeoGebra Classic 6 中打开。

## 核心原则

### 使用 GeoGebra 原生工具

| 需求 | 正确工具 | 错误做法 |
|------|----------|----------|
| 点在线段上 | `Point` 命令 | 直接写坐标 |
| 中点 | `Midpoint` 命令 | 坐标公式计算 |
| 交点 | `Intersect` 命令 | 手动求解 |
| 垂线 | `PerpendicularLine` | 斜率计算 |
| 对称 | `Mirror` 命令 | 坐标变换 |
| 旋转 | `Rotate` 命令 | 三角函数计算 |

### 动态演示优先

- **参数问题** → 使用滑块（Slider）
- **动点问题** → 使用约束点（Point 工具）
- **变换问题** → 使用几何变换工具

## 目录结构

```
math-photo-to-geogebra/
├── SKILL.md                          # Skill 定义文件
├── README.md                         # 本文件
├── AGENTS.md                         # Agent 使用指南
├── scripts/
│   ├── pack_ggb.py                  # XML 打包工具
│   └── image_utils.py               # 图片处理工具
└── references/
    ├── problem-analysis-guide.md     # 题目理解指南
    ├── dynamic-demo-patterns.md      # 动态演示 XML 模板
    ├── common-misunderstandings.md   # 常见偏差与修正
    ├── common-patterns.md            # 几何构造模式
    ├── xml-cheatsheet.md             # XML 语法速查
    ├── quality-check.md              # 质量检查清单
    └── image-embedding.md            # 图片嵌入指南
```

## 参考文档

| 文档 | 内容 |
|------|------|
| [题目理解指南](references/problem-analysis-guide.md) | 人教版七至九年级数形结合内容详解 |
| [动态演示模式](references/dynamic-demo-patterns.md) | 滑块、动点、变换的 XML 模板 |
| [常见理解偏差](references/common-misunderstandings.md) | 静态 vs 动态、计算 vs 工具等 |
| [几何构造模式](references/common-patterns.md) | 矩形、三角形、中位线等构造 |
| [XML 速查](references/xml-cheatsheet.md) | GeoGebra XML 语法快速参考 |
| [质量检查](references/quality-check.md) | 生成后的验证清单 |

## 示例题目

### 示例 1：一次函数参数范围

> 一次函数 `y=kx+b` 经过 `(4,1)` 和 `(0,-1)`，当 `x>-2` 时 `mx>kx+b` 恒成立，求 `m` 范围。

**答案**：`1/2 ≤ m ≤ 1`

**实现**：滑块控制 `m`，绿线 `y=mx` 绕原点旋转。

### 示例 2：菱形最短路径

> 菱形 ABCD 边长 8，∠ABC=120°，E 是 AB 中点，M 在 AC 上动，求 `BM+EM` 最小值。

**答案**：`4√3`

**实现**：将军饮马模型，利用对称性 `BM=DM`。

### 示例 3：矩形折叠

> 矩形 ABCD 沿 EF 折叠，使 C 落在 AD 上的 C' 处。

**实现**：`Mirror` 工具创建对称图形，动点控制折叠位置。

## 依赖

- Python 3.6+
- GeoGebra 6.0+（查看 .ggb 文件）

无需额外 Python 包，仅使用标准库。

## 工作流程

```
用户图片 → OCR 识别 → 分析几何结构 → 生成 XML → 嵌入图片 → 打包 .ggb
                ↓              ↓              ↓
           提取文字      构建图形+约束    base64 编码
```

## 检查清单

生成 .ggb 文件后，验证：

- [ ] 拖动测试 - 点是否可以拖动？
- [ ] 约束测试 - 动点是否保持约束？
- [ ] 中点测试 - 中点是否在正确位置？
- [ ] 答案核对 - 计算结果是否正确？
- [ ] 文本完整 - OCR 题目是否完整显示？

## License

MIT License
