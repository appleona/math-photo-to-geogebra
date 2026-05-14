# 常见几何构造模式

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 人教版各章节题目理解要点
> - [动态演示模式](dynamic-demo-patterns.md) - 标准XML模板和实现模式
> - [常见理解偏差](common-misunderstandings.md) - 偏差类型与修正方法
> - [XML快速参考](xml-cheatsheet.md) - XML语法速查
> - [质量复查机制](quality-check.md) - 检查清单和验证流程



## 基础图形

### 矩形

```xml
<!-- 矩形ABCD -->
<element type="point" label="A">
    <coords x="0" y="6" z="1"/>
    <show object="true" label="true"/>
</element>
<element type="point" label="B">
    <coords x="0" y="0" z="1"/>
    <show object="true" label="true"/>
</element>
<element type="point" label="C">
    <coords x="8" y="0" z="1"/>
    <show object="true" label="true"/>
</element>
<element type="point" label="D">
    <coords x="8" y="6" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 四边 -->
<command name="Segment"><input a0="A" a1="B"/><output a0="sideAB"/></command>
<element type="segment" label="sideAB">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>

<command name="Segment"><input a0="B" a1="C"/><output a0="sideBC"/></command>
<element type="segment" label="sideBC">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>

<command name="Segment"><input a0="C" a1="D"/><output a0="sideCD"/></command>
<element type="segment" label="sideCD">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>

<command name="Segment"><input a0="D" a1="A"/><output a0="sideDA"/></command>
<element type="segment" label="sideDA">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

---

## 点约束

### 点在线段上（可拖动）

```xml
<!-- E在BC上 -->
<command name="Point">
    <input a0="sideBC"/>
    <output a0="E"/>
</command>
<element type="point" label="E">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <pointSize val="5"/>
</element>
```

### 点在线段上（固定位置）

```xml
<!-- E在BC上，距离B为2（BC总长8，比例为0.25） -->
<command name="Point">
    <input a0="sideBC"/>
    <input a1="0.25"/>
    <output a0="E"/>
</command>
<element type="point" label="E">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <pointSize val="5"/>
</element>
```

---

## 中点构造

### 两点的中点

```xml
<command name="Midpoint">
    <input a0="A" a1="B"/>
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="4"/>
</element>
```

### 中位线（三角形两边中点连线）

```xml
<!-- 三角形ABC，D是AB中点，E是AC中点 -->
<command name="Midpoint">
    <input a0="A" a1="B"/>
    <output a0="D"/>
</command>
<element type="point" label="D">
    <show object="true" label="true"/>
</element>

<command name="Midpoint">
    <input a0="A" a1="C"/>
    <output a0="E"/>
</command>
<element type="point" label="E">
    <show object="true" label="true"/>
</element>

<!-- 中位线DE -->
<command name="Segment">
    <input a0="D" a1="E"/>
    <output a0="midline"/>
</command>
<element type="segment" label="midline">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>  <!-- 虚线 -->
</element>
```

---

## 动态几何

### 动点在线段上移动

```xml
<!-- P在CD上移动 -->
<command name="Point">
    <input a0="sideCD"/>
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <pointSize val="5"/>
</element>

<!-- 连接AP -->
<command name="Segment">
    <input a0="A" a1="P"/>
    <output a0="segAP"/>
</command>
<element type="segment" label="segAP">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

---

## 几何关系

### 平行线

```xml
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>
<element type="line" label="lineAB">
    <show object="false" label="false"/>  <!-- 隐藏辅助线 -->
</element>

<!-- 过C作AB的平行线 -->
<command name="Line">
    <input a0="C"/>
    <input a1="lineAB"/>
    <output a0="parallel"/>
</command>
<element type="line" label="parallel">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="1"/>  <!-- 虚线 -->
</element>
```

### 垂线

```xml
<command name="PerpendicularLine">
    <input a0="C" a1="sideAB"/>
    <output a0="perp"/>
</command>
<element type="line" label="perp">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="1"/>
</element>
```

### 交点

```xml
<command name="Intersect">
    <input a0="line1" a1="line2"/>
    <output a0="D"/>
</command>
<element type="point" label="D">
    <show object="true" label="true"/>
</element>
```

---

## 函数图像

### 一次函数

```xml
<element type="function" label="f">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
<expression label="f" exp="2*x+1" type="function"/>
```

### 二次函数

```xml
<element type="function" label="f">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
<expression label="f" exp="x^2-2*x-3" type="function"/>
```

---

## 完整示例：动态几何证明题

```xml
<!-- 矩形ABCD，E在BC上，P在CD上动点，M、N为AE、PE中点，求MN范围 -->
<construction title="动态几何题" author="OCR">
    <!-- 矩形顶点 -->
    <element type="point" label="A"><coords x="0" y="6" z="1"/><show object="true" label="true"/></element>
    <element type="point" label="B"><coords x="0" y="0" z="1"/><show object="true" label="true"/></element>
    <element type="point" label="C"><coords x="8" y="0" z="1"/><show object="true" label="true"/></element>
    <element type="point" label="D"><coords x="8" y="6" z="1"/><show object="true" label="true"/></element>
    
    <!-- 矩形四边 -->
    <command name="Segment"><input a0="A" a1="B"/><output a0="sideAB"/></command>
    <element type="segment" label="sideAB"><show object="true" label="false"/><lineStyle thickness="2" type="0"/></element>
    <command name="Segment"><input a0="B" a1="C"/><output a0="sideBC"/></command>
    <element type="segment" label="sideBC"><show object="true" label="false"/><lineStyle thickness="2" type="0"/></element>
    <command name="Segment"><input a0="C" a1="D"/><output a0="sideCD"/></command>
    <element type="segment" label="sideCD"><show object="true" label="false"/><lineStyle thickness="2" type="0"/></element>
    <command name="Segment"><input a0="D" a1="A"/><output a0="sideDA"/></command>
    <element type="segment" label="sideDA"><show object="true" label="false"/><lineStyle thickness="2" type="0"/></element>
    
    <!-- E在BC上（可拖动） -->
    <command name="Point"><input a0="sideBC"/><output a0="E"/></command>
    <element type="point" label="E"><show object="true" label="true"/><objColor r="255" g="0" b="0" alpha="0"/></element>
    
    <!-- P在CD上（可拖动动点） -->
    <command name="Point"><input a0="sideCD"/><output a0="P"/></command>
    <element type="point" label="P"><show object="true" label="true"/><objColor r="0" g="0" b="255" alpha="0"/></element>
    
    <!-- 连线 -->
    <command name="Segment"><input a0="A" a1="E"/><output a0="segAE"/></command>
    <element type="segment" label="segAE"><show object="true" label="false"/><objColor r="0" g="128" b="0" alpha="0"/></element>
    
    <command name="Segment"><input a0="P" a1="E"/><output a0="segPE"/></command>
    <element type="segment" label="segPE"><show object="true" label="false"/><objColor r="0" g="128" b="0" alpha="0"/></element>
    
    <!-- 中点（Midpoint工具） -->
    <command name="Midpoint"><input a0="A" a1="E"/><output a0="M"/></command>
    <element type="point" label="M"><show object="true" label="true"/><objColor r="255" g="0" b="255" alpha="0"/></element>
    
    <command name="Midpoint"><input a0="P" a1="E"/><output a0="N"/></command>
    <element type="point" label="N"><show object="true" label="true"/><objColor r="255" g="0" b="255" alpha="0"/></element>
    
    <!-- MN连线 -->
    <command name="Segment"><input a0="M" a1="N"/><output a0="segMN"/></command>
    <element type="segment" label="segMN"><show object="true" label="true"/><objColor r="255" g="0" b="0" alpha="0"/><lineStyle thickness="4" type="0"/></element>
</construction>
```
