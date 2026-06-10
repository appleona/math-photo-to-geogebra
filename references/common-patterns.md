# 常见几何构造模式

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

### 延长线上的点

```xml
<!-- 先创建直线（无限延伸） -->
<command name="Line">
    <input a0="A" a1="B"/>
    <output a0="lineAB"/>
</command>
<element type="line" label="lineAB">
    <show object="false" label="false"/>
</element>

<!-- F在AB的延长线上（t>1时在B外侧，t<0时在A外侧） -->
<command name="Point">
    <input a0="lineAB"/>
    <input a1="1.3"/>
    <output a0="F"/>
</command>
<element type="point" label="F">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
</element>

<!-- 延长线部分用虚线表示 -->
<command name="Segment">
    <input a0="B" a1="F"/>
    <output a0="extBF"/>
</command>
<element type="segment" label="extBF">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>
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

### 动点轨迹/最值探究

```xml
<!-- P在BC上移动，M是AP中点，追踪M的轨迹 -->
<command name="Point">
    <input a0="sideBC"/>
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
</element>

<command name="Segment">
    <input a0="A" a1="P"/>
    <output a0="segAP"/>
</command>
<element type="segment" label="segAP">
    <show object="true" label="false"/>
    <lineStyle thickness="1" type="0"/>
</element>

<command name="Midpoint">
    <input a0="A" a1="P"/>
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="5"/>
    <trace val="true"/>  <!-- 开启轨迹追踪 -->
</element>

<!-- 显示MN长度（假设N是固定点） -->
<command name="Segment">
    <input a0="M" a1="N"/>
    <output a0="segMN"/>
</command>
<element type="segment" label="segMN">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
    <caption val="MN"/>
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
<!-- 过C作AB的垂线 -->
<command name="PerpendicularLine">
    <input a0="C" a1="sideAB"/>
    <output a0="perp"/>
</command>
<element type="line" label="perp">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="1"/>
</element>

<!-- 垂足（垂线与AB的交点） -->
<command name="Intersect">
    <input a0="perp" a1="sideAB"/>
    <output a0="H"/>
</command>
<element type="point" label="H">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="4"/>
</element>
```

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

<!-- 角平分线与对边的交点 -->
<command name="Intersect">
    <input a0="bisector" a1="sideBC"/>
    <output a0="D"/>
</command>
<element type="point" label="D">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
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

## 圆相关

### 圆（圆心+半径）

```xml
<!-- 圆心O，半径3 -->
<element type="point" label="O">
    <coords x="5" y="5" z="1"/>
    <show object="true" label="true"/>
</element>

<command name="Circle">
    <input a0="O"/>
    <input a1="3"/>
    <output a0="c1"/>
</command>
<element type="conic" label="c1">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

### 圆（圆心+圆上一点）

```xml
<command name="Circle">
    <input a0="O"/>
    <input a1="A"/>     <!-- A在圆上 -->
    <output a0="c1"/>
</command>
<element type="conic" label="c1">
    <show object="true" label="false"/>
</element>
```

### 圆的切线（过圆上一点）

```xml
<!-- 过圆上一点A作圆的切线 -->
<command name="Tangent">
    <input a0="A"/>
    <input a1="c1"/>
    <output a0="tangent"/>
</command>
<element type="line" label="tangent">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

### 圆的切线（过圆外一点）

```xml
<!-- P在圆外，作两条切线 -->
<command name="Tangent">
    <input a0="P"/>
    <input a1="c1"/>
    <output a0="t1"/>
    <output a0="t2"/>
</command>
<element type="line" label="t1">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
<element type="line" label="t2">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

### 直径与圆周角

```xml
<!-- AB是直径，C在圆上，∠ACB=90°自动满足 -->
<command name="Segment">
    <input a0="A" a1="B"/>
    <output a0="diameter"/>
</command>
<element type="segment" label="diameter">
    <show object="true" label="false"/>
    <lineStyle thickness="2" type="0"/>
</element>

<!-- 标注直角 -->
<command name="Angle">
    <input a0="A" a1="C" a2="B"/>
    <output a0="angleACB"/>
</command>
<element type="angle" label="angleACB">
    <show object="true" label="true"/>
</element>
```

---

## 角度标注

### 标注角度

```xml
<!-- ∠BAC -->
<command name="Angle">
    <input a0="B" a1="A" a2="C"/>
    <output a0="alpha"/>
</command>
<element type="angle" label="alpha">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
</element>
```

### 直角标记

```xml
<!-- ∠ABC = 90° -->
<command name="Angle">
    <input a0="A" a1="B" a2="C"/>
    <output a0="rightAngle"/>
</command>
<element type="angle" label="rightAngle">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
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

### 函数交点

```xml
<!-- y=2x+1 与 y=x^2-2x-3 的交点 -->
<command name="Intersect">
    <input a0="f" a1="g"/>
    <output a0="A"/>
    <output a0="B"/>
</command>
<element type="point" label="A">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
</element>
<element type="point" label="B">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
</element>
```

---

## 标注与文本

### 线段长度标注

```xml
<!-- 在边AB上标注长度 -->
<element type="segment" label="sideAB">
    <show object="true" label="false"/>
    <caption val="10"/>
    <lineStyle thickness="2" type="0"/>
</element>
```

### 已知条件文本框

```xml
<!-- 已知条件 -->
<command name="Text">
    <input a0="&quot;已知：AB=AC，∠B=60°&quot;"/>
    <input a1="(-10, 9)"/>
    <output a0="textGiven"/>
</command>
<element type="text" label="textGiven">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="0" alpha="0"/>
    <fontSize val="12"/>
</element>
```

### 所求目标文本框

```xml
<!-- 所求 -->
<command name="Text">
    <input a0="&quot;求：DE的长度&quot;"/>
    <input a1="(-10, 7)"/>
    <output a0="textGoal"/>
</command>
<element type="text" label="textGoal">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <fontSize val="14"/>
</element>
```

---

## 完整示例

### 示例1：动态几何证明题

矩形ABCD，E在BC上，P在CD上动点，M、N为AE、PE中点，求MN范围。

```xml
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
    
    <!-- MN连线（所求目标 - 红色加粗） -->
    <command name="Segment"><input a0="M" a1="N"/><output a0="segMN"/></command>
    <element type="segment" label="segMN"><show object="true" label="true"/><objColor r="255" g="0" b="0" alpha="0"/><lineStyle thickness="4" type="0"/></element>
</construction>
```

### 示例2：圆与切线题

圆O半径为5，P在圆外，PA、PB是切线，A、B为切点，求∠APB。

```xml
<construction title="圆的切线" author="OCR">
    <!-- 圆心 -->
    <element type="point" label="O">
        <coords x="0" y="0" z="1"/>
        <show object="true" label="true"/>
    </element>
    
    <!-- 圆 -->
    <command name="Circle">
        <input a0="O"/>
        <input a1="5"/>
        <output a0="c1"/>
    </command>
    <element type="conic" label="c1">
        <show object="true" label="false"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <!-- 圆外一点P -->
    <element type="point" label="P">
        <coords x="8" y="6" z="1"/>
        <show object="true" label="true"/>
        <objColor r="0" g="0" b="255" alpha="0"/>
    </element>
    
    <!-- 两条切线 -->
    <command name="Tangent">
        <input a0="P"/>
        <input a1="c1"/>
        <output a0="t1"/>
        <output a0="t2"/>
    </command>
    <element type="line" label="t1">
        <show object="true" label="false"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    <element type="line" label="t2">
        <show object="true" label="false"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <!-- 切点A、B（切线与圆的交点） -->
    <command name="Intersect">
        <input a0="t1" a1="c1"/>
        <output a0="A"/>
    </command>
    <element type="point" label="A">
        <show object="true" label="true"/>
    </element>
    
    <command name="Intersect">
        <input a0="t2" a1="c1"/>
        <output a0="B"/>
    </command>
    <element type="point" label="B">
        <show object="true" label="true"/>
    </element>
    
    <!-- 半径OA、OB -->
    <command name="Segment">
        <input a0="O" a1="A"/>
        <output a0="radiusOA"/>
    </command>
    <element type="segment" label="radiusOA">
        <show object="true" label="false"/>
        <objColor r="0" g="128" b="0" alpha="0"/>
        <lineStyle thickness="1" type="1"/>
    </element>
    
    <command name="Segment">
        <input a0="O" a1="B"/>
        <output a0="radiusOB"/>
    </command>
    <element type="segment" label="radiusOB">
        <show object="true" label="false"/>
        <objColor r="0" g="128" b="0" alpha="0"/>
        <lineStyle thickness="1" type="1"/>
    </element>
    
    <!-- 所求角∠APB -->
    <command name="Angle">
        <input a0="A" a1="P" a2="B"/>
        <output a0="angleAPB"/>
    </command>
    <element type="angle" label="angleAPB">
        <show object="true" label="true"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
    </element>
</construction>
```

### 示例3：等腰三角形+角平分线

等腰△ABC中AB=AC，AD平分∠BAC交BC于D，求证BD=DC。

```xml
<construction title="等腰三角形角平分线" author="OCR">
    <!-- 等腰三角形（对称放置） -->
    <element type="point" label="A">
        <coords x="4" y="6" z="1"/>
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
    
    <!-- 三边 -->
    <command name="Segment"><input a0="A" a1="B"/><output a0="sideAB"/></command>
    <element type="segment" label="sideAB">
        <show object="true" label="false"/>
        <caption val="AB"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <command name="Segment"><input a0="B" a1="C"/><output a0="sideBC"/></command>
    <element type="segment" label="sideBC">
        <show object="true" label="false"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <command name="Segment"><input a0="C" a1="A"/><output a0="sideAC"/></command>
    <element type="segment" label="sideAC">
        <show object="true" label="false"/>
        <caption val="AC"/>
        <lineStyle thickness="2" type="0"/>
    </element>
    
    <!-- 角平分线AD -->
    <command name="AngleBisector">
        <input a0="B" a1="A" a2="C"/>
        <output a0="bisector"/>
    </command>
    <element type="line" label="bisector">
        <show object="true" label="false"/>
        <objColor r="0" g="128" b="0" alpha="0"/>
        <lineStyle thickness="2" type="1"/>
    </element>
    
    <!-- D为角平分线与BC交点 -->
    <command name="Intersect">
        <input a0="bisector" a1="sideBC"/>
        <output a0="D"/>
    </command>
    <element type="point" label="D">
        <show object="true" label="true"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
        <pointSize val="5"/>
    </element>
    
    <!-- 辅助线AD -->
    <command name="Segment">
        <input a0="A" a1="D"/>
        <output a0="segAD"/>
    </command>
    <element type="segment" label="segAD">
        <show object="true" label="false"/>
        <objColor r="0" g="128" b="0" alpha="0"/>
        <lineStyle thickness="2" type="1"/>
    </element>
    
    <!-- 标注BD和DC（所求证） -->
    <command name="Segment">
        <input a0="B" a1="D"/>
        <output a0="segBD"/>
    </command>
    <element type="segment" label="segBD">
        <show object="true" label="false"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
        <lineStyle thickness="3" type="0"/>
        <caption val="BD"/>
    </element>
    
    <command name="Segment">
        <input a0="D" a1="C"/>
        <output a0="segDC"/>
    </command>
    <element type="segment" label="segDC">
        <show object="true" label="false"/>
        <objColor r="255" g="0" b="0" alpha="0"/>
        <lineStyle thickness="3" type="0"/>
        <caption val="DC"/>
    </element>
</construction>
```
