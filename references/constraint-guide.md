# 约束建模深度指南

## 什么是约束建模

约束建模是将数学题中的几何关系转换为GeoGebra原生工具命令的过程。
**核心原则：让GeoGebra计算，不要自己计算。**

---

## 约束层次结构

```
Level 1: 基础约束（必须掌握）
├── 点在线段上 → Point工具
├── 中点 → Midpoint工具
└── 交点 → Intersect工具

Level 2: 方向约束（常用）
├── 垂线 → PerpendicularLine工具
├── 平行线 → Line工具（点+平行线模式）
└── 角平分线 → AngleBisector工具

Level 3: 圆约束（中高档题）
├── 圆（圆心+半径） → Circle工具
├── 切线（圆上/圆外） → Tangent工具
└── 点在圆上 → Point工具（约束到圆）

Level 4: 动态约束（探究题）
├── 动点在线段上 → Point工具（可拖动）
├── 动点在圆上 → Point工具（约束到圆）
├── 轨迹追踪 → trace属性
└── 范围测量 → 长度/角度测量
```

---

## 从题目文本到约束的映射

### 关键词-工具对照表

| 题目关键词 | 约束类型 | GeoGebra工具 | 示例 |
|-----------|---------|-------------|------|
| "点E在BC上" | 位置约束 | `Point`+线段输入 | `<input a0="sideBC"/>` |
| "E是BC中点" | 中点约束 | `Midpoint` | `<input a0="B" a1="C"/>` |
| "延长AB到D" | 延长线约束 | `Line`+`Point`参数>1 | `<input a1="1.5"/>` |
| "AD⊥BC" | 垂直约束 | `PerpendicularLine`+`Intersect` | 垂足H |
| "DE∥AB" | 平行约束 | `Line`（点+平行线） | `<input a1="lineAB"/>` |
| "AD平分∠BAC" | 角平分约束 | `AngleBisector` | `<input a0="B" a1="A" a2="C"/>` |
| "以O为圆心，5为半径" | 圆约束 | `Circle` | `<input a0="O"/><input a1="5"/>` |
| "PA是圆的切线" | 切线约束 | `Tangent` | `<input a0="P"/><input a1="c1"/>` |
| "P在BC上移动" | 动态约束 | `Point`（可拖动） | 不指定参数 |
| "AB=AC" | 等长约束 | 坐标对称性 | A在BC垂直平分线上 |
| "∠B=90°" | 直角约束 | 坐标放置+`Angle` | B在直角位置 |

---

## 特殊几何图形的约束建模

### 等腰三角形（AB=AC）

**方法：** 利用对称性，顶点放在底边垂直平分线上

```xml
<!-- 底边BC水平放置 -->
<element type="point" label="B"><coords x="-3" y="0" z="1"/><show object="true" label="true"/></element>
<element type="point" label="C"><coords x="3" y="0" z="1"/><show object="true" label="true"/></element>

<!-- 顶点A在垂直平分线上（x=0） -->
<element type="point" label="A"><coords x="0" y="5" z="1"/><show object="true" label="true"/></element>

<!-- 这样AB=AC自动满足 -->
```

### 等边三角形

**方法：** 一个顶点在原点，另一个在x轴，第三个用60°角度

```xml
<element type="point" label="A"><coords x="0" y="0" z="1"/></element>
<element type="point" label="B"><coords x="6" y="0" z="1"/></element>
<element type="point" label="C"><coords x="3" y="5.196" z="1"/></element>
<!-- 高度 = 6 * √3/2 ≈ 5.196 -->
```

### 直角三角形（∠B=90°）

**方法：** 直角顶点放在角落，两边沿坐标轴

```xml
<element type="point" label="B"><coords x="0" y="0" z="1"/></element>
<element type="point" label="A"><coords x="0" y="6" z="1"/></element>
<element type="point" label="C"><coords x="8" y="0" z="1"/></element>

<!-- 标注直角 -->
<command name="Angle">
    <input a0="A" a1="B" a2="C"/>
    <output a0="rightB"/>
</command>
<element type="angle" label="rightB"><show object="true" label="false"/></element>
```

### 正方形

```xml
<element type="point" label="A"><coords x="0" y="4" z="1"/></element>
<element type="point" label="B"><coords x="0" y="0" z="1"/></element>
<element type="point" label="C"><coords x="4" y="0" z="1"/></element>
<element type="point" label="D"><coords x="4" y="4" z="1"/></element>
```

### 菱形（对角线互相垂直平分）

```xml
<!-- 对角线交点在原点 -->
<element type="point" label="O"><coords x="0" y="0" z="1"/></element>
<element type="point" label="A"><coords x="-4" y="0" z="1"/></element>
<element type="point" label="C"><coords x="4" y="0" z="1"/></element>
<element type="point" label="B"><coords x="0" y="3" z="1"/></element>
<element type="point" label="D"><coords x="0" y="-3" z="1"/></element>
```

---

## 动态约束建模

### 动点+依赖元素

当点P在线段上移动时，所有依赖P的元素自动更新：

```xml
<!-- P在BC上（动点） -->
<command name="Point">
    <input a0="sideBC"/>
    <output a0="P"/>
</command>

<!-- AP自动随P移动 -->
<command name="Segment">
    <input a0="A" a1="P"/>
    <output a0="segAP"/>
</command>

<!-- M是AP中点（自动更新） -->
<command name="Midpoint">
    <input a0="A" a1="P"/>
    <output a0="M"/>
</command>
```

### 轨迹追踪

```xml
<!-- M的轨迹 -->
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="5"/>
    <trace val="true"/>   <!-- 开启轨迹 -->
</element>
```

### 范围/最值显示

```xml
<!-- 显示MN长度 -->
<command name="Segment">
    <input a0="M" a1="N"/>
    <output a0="segMN"/>
</command>
<element type="segment" label="segMN">
    <show object="true" label="true"/>
    <caption val="MN"/>
</element>

<!-- 或者显示距离文本 -->
<command name="Distance">
    <input a0="M"/>
    <input a0="N"/>
    <output a0="distMN"/>
</command>
```

---

## 辅助线约束建模

辅助线必须用**虚线**和**绿色/灰色**区分。

### 延长线

```xml
<!-- 延长BA到F（F在BA延长线上，A在B和F之间） -->
<command name="Line">
    <input a0="B" a1="A"/>
    <output a0="lineBA"/>
</command>
<command name="Point">
    <input a0="lineBA"/>
    <input a1="-0.5"/>    <!-- <0表示在B的外侧 -->
    <output a0="F"/>
</command>
<command name="Segment">
    <input a0="A" a1="F"/>
    <output a0="extAF"/>
</command>
<element type="segment" label="extAF">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>  <!-- 虚线 -->
</element>
```

### 平行辅助线

```xml
<!-- 过C作AB的平行线（辅助线） -->
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>
<command name="Line">
    <input a0="C"/>
    <input a1="lineAB"/>
    <output a0="auxParallel"/>
</command>
<element type="line" label="auxParallel">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>
</element>
```

### 垂线辅助线

```xml
<!-- 过A作BC的垂线（辅助线） -->
<command name="PerpendicularLine">
    <input a0="A"/>
    <input a1="sideBC"/>
    <output a0="auxPerp"/>
</command>
<element type="line" label="auxPerp">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>
</element>

<!-- 垂足 -->
<command name="Intersect">
    <input a0="auxPerp" a1="sideBC"/>
    <output a0="H"/>
</command>
```

---

## 约束建模检查口诀

```
见中点，用Midpoint，不要除二算坐标
见垂直，用PerpendicularLine，不要斜率负倒数
见平行，用Line点加线，不要斜率复制粘贴
见交点，用Intersect，不要联立方程算
见线上，用Point工具，不要目测写坐标
见切线，用Tangent，不要手动画一条
见平分，用AngleBisector，不要角度除以二
见圆上，用Point约束圆，不要三角函数算
```
