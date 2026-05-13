# GeoGebra XML 快速参考

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 各题型理解要点
> - [动态演示模式](dynamic-demo-patterns.md) - 完整XML模板
> - [常见理解偏差](common-misunderstandings.md) - 常见错误避免
> - [常见几何构造](common-patterns.md) - 几何构造模式
> - [质量复查机制](quality-check.md) - 检查清单



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
<command name="Circle">
    <input a0="O" a1="3"/>  <!-- 圆心+半径 -->
    <output a0="c1"/>
</command>
<element type="conic" label="c1">
    <show object="true" label="false"/>
</element>
```

---

### 角度

```xml
<command name="Angle">
    <input a0="B" a1="A" a2="C"/>  <!-- ∠BAC -->
    <output a0="alpha"/>
</command>
<element type="angle" label="alpha">
    <show object="true" label="true"/>
</element>
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
        <input a1="(-2, 6)"/>
        <output a0="text1"/>
    </command>
    <element type="text" label="text1">
        <show object="true" label="false"/>
        <fontSize val="14"/>
    </element>
</construction>
</geogebra>
```
