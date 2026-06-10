# GeoGebra XML 快速参考

## 核心原则

**使用GeoGebra原生工具，不要手动计算！**

---

## 基本结构

```xml
<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<euclidianView>
    <viewNumber viewNo="1"/>
    <coordSystem xZero="600" yZero="400" scale="50" yscale="50"/>
    <evSettings axes="false" grid="true"/>
    <bgColor r="255" g="255" b="255"/>
</euclidianView>
<construction title="数学题目" author="OCR" date="">
    <!-- 几何对象 -->
</construction>
</geogebra>
```

---

## 几何对象

### 点

#### 自由点

```xml
<element type="point" label="A">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="0" alpha="0"/>
    <pointSize val="4"/>
    <pointStyle val="0"/>
    <coords x="0" y="0" z="1"/>
</element>
```

#### 点在线段上（关键！）

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
    <pointSize val="5"/>
</element>
```

#### 点在直线上（用于延长线）

```xml
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>
<element type="line" label="lineAB">
    <show object="false" label="false"/>
</element>

<command name="Point">
    <input a0="lineAB"/>       <!-- 约束到直线 -->
    <input a1="1.5"/>          <!-- 参数：1=点B，0=点A，>1在B外侧 -->
    <output a0="F"/>
</command>
```

#### 点在圆上

```xml
<command name="Point">
    <input a0="c1"/>           <!-- 约束到圆 -->
    <input a1="0.3"/>          <!-- 参数：0~1对应圆周位置 -->
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
</element>
```

---

### 线段

```xml
<!-- 创建线段 -->
<command name="Segment">
    <input a0="A" a1="B"/>
    <output a0="s1"/>
</command>

<!-- 设置显示属性 -->
<element type="segment" label="s1">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="0"/>  <!-- 线宽2，实线 -->
</element>
```

线型类型：
- `type="0"`: 实线
- `type="1"`: 虚线
- `type="2"`: 点线

粗细建议：
- 普通边线：`thickness="2"`
- 所求目标：`thickness="4"`
- 辅助线：`thickness="1"` 或 `2` + 虚线

---

### 中点（Midpoint工具）

```xml
<!-- 使用Midpoint工具自动计算中点 -->
<command name="Midpoint">
    <input a0="A" a1="E"/>  <!-- 输入两个端点 -->
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="4"/>
</element>
```

**注意**：不要使用坐标计算中点！

---

### 直线

```xml
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="l1"/>
</command>
<element type="line" label="l1">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

---

### 圆

```xml
<!-- 圆心+半径 -->
<command name="Circle">
    <input a0="O"/>     <!-- 圆心 -->
    <input a1="3"/>     <!-- 半径数值 -->
    <output a0="c1"/>
</command>

<!-- 圆心+圆上一点 -->
<command name="Circle">
    <input a0="O"/>     <!-- 圆心 -->
    <input a1="A"/>     <!-- 圆上一点 -->
    <output a0="c1"/>
</command>

<element type="conic" label="c1">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

---

### 角度

```xml
<!-- ∠BAC -->
<command name="Angle">
    <input a0="B" a1="A" a2="C"/>
    <output a0="alpha"/>
</command>
<element type="angle" label="alpha">
    <show object="true" label="true"/>
</element>
```

---

### 垂线

```xml
<command name="PerpendicularLine">
    <input a0="C"/>         <!-- 经过的点 -->
    <input a1="sideAB"/>    <!-- 垂直对象（线段/直线） -->
    <output a0="perp"/>
</command>
<element type="line" label="perp">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="1"/>
</element>
```

---

### 平行线

```xml
<!-- 先定义参考线 -->
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>

<!-- 过C作AB的平行线 -->
<command name="Line">
    <input a0="C"/>
    <input a1="lineAB"/>    <!-- 平行于lineAB -->
    <output a0="parallel"/>
</command>
```

---

### 角平分线

```xml
<!-- ∠BAC的角平分线 -->
<command name="AngleBisector">
    <input a0="B" a1="A" a2="C"/>
    <output a0="bisector"/>
</command>
<element type="line" label="bisector">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>
</element>
```

---

### 切线

```xml
<!-- 过圆上一点A作切线 -->
<command name="Tangent">
    <input a0="A"/>
    <input a1="c1"/>
    <output a0="tangent"/>
</command>

<!-- 过圆外一点P作切线（两条） -->
<command name="Tangent">
    <input a0="P"/>
    <input a1="c1"/>
    <output a0="t1"/>
    <output a0="t2"/>
</command>
```

---

### 交点

```xml
<!-- 两线交点 -->
<command name="Intersect">
    <input a0="line1" a1="line2"/>
    <output a0="D"/>
</command>

<!-- 线与圆交点 -->
<command name="Intersect">
    <input a0="line1" a1="c1"/>
    <output a0="E"/>
    <output a0="F"/>
</command>
```

---

### 垂足

```xml
<!-- 方法一：PerpendicularLine + Intersect -->
<command name="PerpendicularLine">
    <input a0="C"/>
    <input a1="sideAB"/>
    <output a0="perp"/>
</command>
<command name="Intersect">
    <input a0="perp" a1="sideAB"/>
    <output a0="H"/>
</command>
```

---

## 函数图像

```xml
<element type="function" label="f">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
<expression label="f" exp="x^2-2*x-3" type="function"/>
```

---

## OCR文本框

```xml
<!-- 文本命令 -->
<command name="Text">
    <input a0="&quot;题目OCR内容...&quot;"/>
    <input a1="(-10, 9)"/>  <!-- 位置坐标 -->
    <output a0="textOCR"/>
</command>

<!-- 文本元素设置 -->
<element type="text" label="textOCR">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="0" alpha="0"/>
    <fontSize val="12"/>
</element>
```

---

## 图片嵌入

```xml
<command name="Image">
    <input a0="&quot;data:image/png;base64,iVBORw0KGgo...&quot;"/>
    <input a1="(-2, -8)"/>     <!-- 左下角坐标 -->
    <input a2="(14, 0)"/>      <!-- 宽度向量 -->
    <input a3="(0, 10)"/>      <!-- 高度向量 -->
    <output a0="originalFigure"/>
</command>
<element type="image" label="originalFigure">
    <show object="true" label="false"/>
</element>
```

---

## 颜色编码规范

| 元素类型 | 颜色 (r,g,b) | 说明 |
|----------|-------------|------|
| 普通顶点 | (0,0,0) 黑色 | 默认点颜色 |
| 动态点 | (0,0,255) 蓝色 | 可拖动的动点 |
| 中点/特殊点 | (255,0,255) 紫色 | 中点、垂足等 |
| 所求目标 | (255,0,0) 红色 | 需要求解的边/角 |
| 辅助线 | (0,128,0) 绿色 | 延长线、辅助线 |
| 函数图像 | (0,0,255) 蓝色 | 一次函数 |
| 二次函数 | (255,0,0) 红色 | 二次函数 |
| 圆 | (0,0,255) 蓝色 | 默认圆颜色 |
| 切线 | (255,0,0) 红色 | 切线突出显示 |

---

## 常见错误

### 错误1：手动计算中点

```xml
<!-- ✗ 错误 -->
<element type="point" label="M">
    <coords x="1" y="3" z="1"/>  <!-- 手动计算 -->
</element>

<!-- ✓ 正确 -->
<command name="Midpoint">
    <input a0="A" a1="E"/>
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
</element>
```

### 错误2：点不约束到线段

```xml
<!-- ✗ 错误 -->
<element type="point" label="E">
    <coords x="2" y="0" z="1"/>
</element>

<!-- ✓ 正确 -->
<command name="Point">
    <input a0="sideBC"/>
    <output a0="E"/>
</command>
```

### 错误3：特殊字符未转义

```xml
<!-- ✗ 错误 -->
<input a0="题目内容"ABCD"..."/>

<!-- ✓ 正确 -->
<input a0="&quot;题目内容ABCD...&quot;"/>
```

### 错误4：手动计算垂足坐标

```xml
<!-- ✗ 错误 -->
<element type="point" label="H">
    <coords x="2" y="1" z="1"/>  <!-- 手算投影 -->
</element>

<!-- ✓ 正确 -->
<command name="PerpendicularLine">
    <input a0="C"/>
    <input a1="sideAB"/>
    <output a0="perp"/>
</command>
<command name="Intersect">
    <input a0="perp" a1="sideAB"/>
    <output a0="H"/>
</command>
```

### 错误5：手动计算平行线

```xml
<!-- ✗ 错误：通过斜率相同手动设点 -->
<element type="point" label="D">
    <coords x="5" y="2" z="1"/>  <!-- 假设斜率相同 -->
</element>

<!-- ✓ 正确：使用Line工具的平行模式 -->
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>
<command name="Line">
    <input a0="C"/>
    <input a1="lineAB"/>
    <output a0="parallel"/>
</command>
```

---

## 完整三角形示例

```xml
<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<euclidianView>
    <viewNumber viewNo="1"/>
    <coordSystem xZero="400" yZero="300" scale="50"/>
    <evSettings axes="false" grid="true"/>
</euclidianView>
<construction>
    <!-- 三个顶点 -->
    <element type="point" label="A">
        <show object="true" label="true"/>
        <coords x="0" y="0" z="1"/>
    </element>
    <element type="point" label="B">
        <show object="true" label="true"/>
        <coords x="5" y="0" z="1"/>
    </element>
    <element type="point" label="C">
        <show object="true" label="true"/>
        <coords x="2.5" y="4.33" z="1"/>
    </element>
    
    <!-- 三条边 -->
    <command name="Segment"><input a0="A" a1="B"/><output a0="c"/></command>
    <element type="segment" label="c">
        <show object="true" label="false"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <command name="Segment"><input a0="B" a1="C"/><output a0="a"/></command>
    <element type="segment" label="a">
        <show object="true" label="false"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <command name="Segment"><input a0="C" a1="A"/><output a0="b"/></command>
    <element type="segment" label="b">
        <show object="true" label="false"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <!-- OCR文本框 -->
    <command name="Text">
        <input a0="&quot;三角形ABC，求面积&quot;"/>
        <input a0="(-2, 6)"/>
        <output a0="text1"/>
    </command>
    <element type="text" label="text1">
        <show object="true" label="false"/>
        <fontSize val="14"/>
    </element>
</construction>
</geogebra>
```
