# 动态演示标准模式库

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 题目理解要点和陷阱
> - [常见理解偏差](common-misunderstandings.md) - 偏差识别与修正
> - [常见几何构造](common-patterns.md) - 几何构造XML模式
> - [XML快速参考](xml-cheatsheet.md) - XML语法速查
> - [质量复查机制](quality-check.md) - 检查清单



> 本库提供人教版初中数学各类数形结合问题的GeoGebra动态演示标准实现模式，直接复制使用。

---

## 模式0：文本布局与间距规范

### 0.1 文本框间距标准

**核心原则：相邻文本框 y 坐标差 ≥ 1.5，分组间距 ≥ 2**

```xml
<!-- ====== 正确示例：间距充足 ====== -->

<!-- 题目第一行 -->
<command name="Text">
    <input a0="&quot;【题目】在平面直角坐标系xOy中...&quot;"/>
    <input a1="(-12, 9)"/>       <!-- y=9 -->
    <output a0="line1"/>
</command>
<element type="text" label="line1"><show object="true" label="false"/><fontSize val="11"/></element>

<!-- 题目第二行（间距2） -->
<command name="Text">
    <input a0="&quot;一次函数y=kx+b(k≠0)的图象经过点(4,1)和(0,-1)。&quot;"/>
    <input a1="(-12, 7)"/>       <!-- y=7，与上行差2 -->
    <output a0="line2"/>
</command>
<element type="text" label="line2"><show object="true" label="false"/><fontSize val="11"/></element>

<!-- 答案（与题目间距2） -->
<command name="Text">
    <input a0="&quot;【答案】y = 0.5x - 1&quot;"/>
    <input a1="(-12, 5)"/>       <!-- y=5，与上行差2 -->
    <output a0="answer"/>
</command>
<element type="text" label="answer"><show object="true" label="false"/><objColor r="255" g="0" b="0"/><fontSize val="13"/></element>

<!-- 分析提示（与答案间距2） -->
<command name="Text">
    <input a0="&quot;【提示】拖动滑块改变m值观察变化&quot;"/>
    <input a1="(-12, 3)"/>       <!-- y=3，与上行差2 -->
    <output a0="hint"/>
</command>
<element type="text" label="hint"><show object="true" label="false"/><objColor r="128" g="128" b="128"/><fontSize val="10"/></element>

<!-- 图形区域（y≤2） -->
<!-- ... 几何图形 ... -->
```

**间距速查表：**

| 元素类型 | 最小间距 | 推荐间距 |
|----------|----------|----------|
| 题目行之间 | 1.5 | 2.0 |
| 题目→答案 | 2.0 | 2.5 |
| 答案→分析 | 1.5 | 2.0 |
| 文本→图形 | 1.0 | 1.5 |
| 滑块之间 | 1.0 | 1.5 |

---

### 0.2 图形方向与原图一致

**核心原则：按原图方向设置坐标，不要旋转**

```xml
<!-- ====== 菱形示例：AC水平，BD竖直 ====== -->
<!-- 原图方向：AC水平（左右），BD竖直（上下） -->

<!-- 正确：保持原图方向 -->
<element type="point" label="A"><coords x="-6.928" y="0" z="1"/></element>   <!-- 左 -->
<element type="point" label="C"><coords x="6.928" y="0" z="1"/></element>    <!-- 右 -->
<element type="point" label="B"><coords x="0" y="-4" z="1"/></element>      <!-- 下 -->
<element type="point" label="D"><coords x="0" y="4" z="1"/></element>       <!-- 上 -->

<!-- 错误：旋转90°，与原图不一致 -->
<!-- <element type="point" label="A"><coords x="0" y="6.928" z="1"/></element> -->   <!-- ❌ 上 -->
<!-- <element type="point" label="C"><coords x="0" y="-6.928" z="1"/></element> -->  <!-- ❌ 下 -->
<!-- <element type="point" label="B"><coords x="-4" y="0" z="1"/></element> -->     <!-- ❌ 左 -->
<!-- <element type="point" label="D"><coords x="4" y="0" z="1"/></element> -->      <!-- ❌ 右 -->
```

**方向检查清单：**

| 检查项 | 原图特征 | 生成要求 |
|--------|----------|----------|
| 底边 | 水平放置 | A在左，B在右，y坐标相同 |
| 对称轴 | 竖直/水平 | 保持相同方向 |
| 顶点顺序 | 顺时针A→B→C→D | 按相同顺序定义坐标 |
| 上下关系 | D在上，B在下 | y(D) > y(B) |

---

## 模式1：参数滑块控制

### 1.1 一次函数 y=kx+b 参数控制

**适用场景：**
- 一次函数中k或b的参数范围问题
- 两条直线位置关系随参数变化
- y=mx型过原点旋转问题

**XML模板：**
```xml
<!-- ====== 滑块控制模式 ====== -->

<!-- 滑块控制斜率k，范围-3到3 -->
<element type="numeric" label="k">
    <value val="1"/>
    <slider min="-3" max="3" step="0.1" type="number" sliderStyle="0"/>
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
    <sliderBlobSize val="10"/>
    <sliderWidth val="200"/>
    <coords x="-350" y="250" z="1"/>
</element>

<!-- 滑块控制截距b，范围-5到5 -->
<element type="numeric" label="b">
    <value val="0"/>
    <slider min="-5" max="5" step="0.5" type="number" sliderStyle="0"/>
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
    <sliderBlobSize val="10"/>
    <sliderWidth val="200"/>
    <coords x="-350" y="200" z="1"/>
</element>

<!-- 动态直线 y = kx + b -->
<element type="function" label="f_dynamic">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
</element>
<expression label="f_dynamic" exp="k*x + b" type="function"/>

<!-- 当前参数值显示 -->
<command name="Text">
    <input a0="&quot;k = &quot; + k"/>
    <input a1="(-350, 150)"/>
    <output a0="k_value"/>
</command>
<element type="text" label="k_value">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <fontSize val="14"/>
</element>

<command name="Text">
    <input a0="&quot;b = &quot; + b"/>
    <input a1="(-350, 120)"/>
    <output a0="b_value"/>
</command>
<element type="text" label="b_value">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <fontSize val="14"/>
</element>
```

**关键说明：**
- sliderStyle="0" 表示水平滑块
- sliderWidth 控制滑块长度
- coords 设置滑块位置（像素坐标）
- 表达式 exp 中使用滑块变量名

---

### 1.2 二次函数 y=ax²+bx+c 参数控制

**XML模板：**
```xml
<!-- 滑块控制a（开口），范围-2到2 -->
<element type="numeric" label="a">
    <value val="1"/>
    <slider min="-2" max="2" step="0.1" type="number"/>
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <sliderWidth val="150"/>
    <coords x="-350" y="280" z="1"/>
</element>

<!-- 滑块控制b，范围-5到5 -->
<element type="numeric" label="b">
    <value val="0"/>
    <slider min="-5" max="5" step="0.5" type="number"/>
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <sliderWidth val="150"/>
    <coords x="-350" y="230" z="1"/>
</element>

<!-- 滑块控制c，范围-5到5 -->
<element type="numeric" label="c">
    <value val="0"/>
    <slider min="-5" max="5" step="0.5" type="number"/>
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <sliderWidth val="150"/>
    <coords x="-350" y="180" z="1"/>
</element>

<!-- 二次函数 -->
<element type="function" label="parabola">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
</element>
<expression label="parabola" exp="a*x^2 + b*x + c" type="function"/>

<!-- 顶点坐标（自动计算） -->
<element type="point" label="Vertex">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <pointSize val="6"/>
    <coords x="-b/(2*a)" y="c - b^2/(4*a)" z="1"/>
</element>

<!-- 对称轴 -->
<element type="line" label="axis">
    <show object="true" label="false"/>
    <objColor r="128" g="128" b="128" alpha="0"/>
    <lineStyle thickness="1" type="1"/>
    <coords x="-b/(2*a)" y="0" z="0"/>
</element>
```

---

### 1.3 反比例函数 y=k/x 参数控制

**XML模板：**
```xml
<!-- 滑块控制k，范围-10到10，不包含0 -->
<element type="numeric" label="k">
    <value val="6"/>
    <slider min="-10" max="10" step="0.5" type="number"/>
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="128" alpha="0"/>
    <sliderWidth val="200"/>
    <coords x="-350" y="250" z="1"/>
</element>

<!-- 反比例函数（自动处理k的正负） -->
<element type="function" label="hyperbola">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="128" alpha="0"/>
    <lineStyle thickness="3" type="0"/>
</element>
<expression label="hyperbola" exp="k/x" type="function"/>

<!-- k值显示 -->
<command name="Text">
    <input a0="&quot;k = &quot; + k + &quot; (k&gt;0时在一三象限，k&lt;0时在二四象限)&quot;"/>
    <input a1="(-350, 200)"/>
    <output a0="k_info"/>
</command>
<element type="text" label="k_info">
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="128" alpha="0"/>
    <fontSize val="11"/>
</element>
```

---

## 模式2：动点约束

### 2.1 点在线段上移动

**适用场景：**
- 动点在三角形边上
- 矩形边上的动点
- 线段上的最值问题

**XML模板：**
```xml
<!-- ====== 动点约束模式 ====== -->

<!-- 1. 创建基础图形（以矩形为例） -->
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

<!-- 2. 创建矩形四边 -->
<command name="Segment"><input a0="A" a1="B"/><output a0="sideAB"/></command>
<element type="segment" label="sideAB"><show object="true" label="false"/><lineStyle thickness="2"/></element>

<command name="Segment"><input a0="B" a1="C"/><output a0="sideBC"/></command>
<element type="segment" label="sideBC"><show object="true" label="false"/><lineStyle thickness="2"/></element>

<command name="Segment"><input a0="C" a1="D"/><output a0="sideCD"/></command>
<element type="segment" label="sideCD"><show object="true" label="false"/><lineStyle thickness="2"/></element>

<command name="Segment"><input a0="D" a1="A"/><output a0="sideDA"/></command>
<element type="segment" label="sideDA"><show object="true" label="false"/><lineStyle thickness="2"/></element>

<!-- 3. 动点E约束在BC上（关键！） -->
<command name="Point">
    <input a0="sideBC"/>  <!-- 约束到线段 -->
    <output a0="E"/>
</command>
<element type="point" label="E">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 4. 动点P约束在CD上 -->
<command name="Point">
    <input a0="sideCD"/>
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 5. 连接AE、PE形成动态几何 -->
<command name="Segment"><input a0="A" a1="E"/><output a0="segAE"/></command>
<element type="segment" label="segAE"><show object="true" label="false"/><objColor r="0" g="128" b="0"/></element>

<command name="Segment"><input a0="P" a1="E"/><output a0="segPE"/></command>
<element type="segment" label="segPE"><show object="true" label="false"/><objColor r="0" g="128" b="0"/></element>

<!-- 6. 中点M、N（随动点自动变化） -->
<command name="Midpoint"><input a0="A" a1="E"/><output a0="M"/></command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="5"/>
</element>

<command name="Midpoint"><input a0="P" a1="E"/><output a0="N"/></command>
<element type="point" label="N">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="5"/>
</element>

<!-- 7. 连接MN（动态线段） -->
<command name="Segment"><input a0="M" a1="N"/><output a0="segMN"/></command>
<element type="segment" label="segMN">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="4" type="0"/>
</element>

<!-- 8. 显示MN长度（实时更新） -->
<command name="Text">
    <input a0="&quot;MN长度 = &quot; + segMN"/>
    <input a1="(9, 8)"/>
    <output a0="mn_length"/>
</command>
<element type="text" label="mn_length">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <fontSize val="14"/>
</element>
```

**关键说明：**
- Point工具约束后，拖动时自动限制在线段上
- 所有依赖该点的元素（如中点、连线）自动跟随
- 显示长度时使用 `+ segMN` 自动计算

---

### 2.2 点在圆上移动

**XML模板：**
```xml
<!-- 圆心 -->
<element type="point" label="O">
    <coords x="0" y="0" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 圆上一点（用于定义半径） -->
<element type="point" label="R">
    <coords x="5" y="0" z="1"/>
    <show object="true" label="false"/>
</element>

<!-- 圆 -->
<command name="Circle">
    <input a0="O"/>
    <input a1="R"/>
    <output a0="circle1"/>
</command>
<element type="conic" label="circle1">
    <show object="true" label="false"/>
    <objColor r="0" g="0" b="0" alpha="0"/>
</element>

<!-- 动点P在圆上 -->
<command name="Point">
    <input a0="circle1"/>
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 连接OP -->
<command name="Segment"><input a0="O" a1="P"/><output a0="radius"/></command>
<element type="segment" label="radius">
    <show object="true" label="false"/>
    <objColor r="128" g="128" b="128"/>
    <lineStyle thickness="1" type="1"/>
</element>
```

---

## 模式3：几何变换

### 3.1 轴对称（Mirror）

**适用场景：**
- 折叠问题
- 对称图形
- 最短路径（将军饮马）

**XML模板：**
```xml
<!-- ====== 轴对称模式 ====== -->

<!-- 对称轴（直线） -->
<element type="line" label="axisLine">
    <show object="true" label="false"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="2" type="1"/>  <!-- 虚线 -->
    <coords x="0" y="1" z="-3"/>  <!-- 例如 y = 3 -->
</element>

<!-- 原点 -->
<element type="point" label="A">
    <coords x="2" y="5" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 对称点A' -->
<command name="Mirror">
    <input a0="A"/>
    <input a1="axisLine"/>
    <output a0="A_prime"/>
</command>
<element type="point" label="A_prime">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 连线AA'（被对称轴垂直平分） -->
<command name="Segment"><input a0="A" a1="A_prime"/><output a0="AA_prime"/></command>
<element type="segment" label="AA_prime">
    <show object="true" label="false"/>
    <objColor r="128" g="128" b="128"/>
    <lineStyle thickness="1" type="1"/>
</element>

<!-- 交点（垂足） -->
<command name="Intersect">
    <input a0="AA_prime"/>
    <input a1="axisLine"/>
    <output a0="M"/>
</command>
<element type="point" label="M">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="255" alpha="0"/>
    <pointSize val="4"/>
</element>
```

---

### 3.2 旋转（Rotate）

**适用场景：**
- 旋转问题
- 等边三角形、正方形旋转
- 旋转最值问题

**XML模板：**
```xml
<!-- ====== 旋转模式 ====== -->

<!-- 滑块控制旋转角度 -->
<element type="numeric" label="angle">
    <value val="30"/>
    <slider min="0" max="360" step="1" type="angle"/>
    <show object="true" label="true"/>
    <objColor r="255" g="128" b="0" alpha="0"/>
    <sliderWidth val="200"/>
    <coords x="-350" y="250" z="1"/>
</element>

<!-- 旋转中心 -->
<element type="point" label="O">
    <coords x="0" y="0" z="1"/>
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 原点 -->
<element type="point" label="A">
    <coords x="5" y="0" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 旋转后的点A' -->
<command name="Rotate">
    <input a0="A"/>
    <input a1="angle"/>  <!-- 滑块控制的角度 -->
    <input a2="O"/>      <!-- 旋转中心 -->
    <output a0="A_rotated"/>
</command>
<element type="point" label="A_rotated">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 旋转轨迹（圆弧） -->
<command name="Circle">
    <input a0="O"/>
    <input a1="A"/>
    <output a0="trailCircle"/>
</command>
<element type="conic" label="trailCircle">
    <show object="true" label="false"/>
    <objColor r="200" g="200" b="200"/>
</element>

<!-- 连线OA和OA' -->
<command name="Segment"><input a0="O" a1="A"/><output a0="OA"/></command>
<element type="segment" label="OA"><show object="true"/><objColor r="0" g="0" b="0"/></element>

<command name="Segment"><input a0="O" a1="A_rotated"/><output a0="OA_rotated"/></command>
<element type="segment" label="OA_rotated"><show object="true"/><objColor r="255" g="0" b="0"/></element>

<!-- 当前角度显示 -->
<command name="Text">
    <input a0="&quot;旋转角 = &quot; + angle + &quot;°&quot;"/>
    <input a1="(-350, 200)"/>
    <output a0="angle_display"/>
</command>
<element type="text" label="angle_display">
    <show object="true" label="false"/>
    <objColor r="255" g="128" b="0" alpha="0"/>
    <fontSize val="14"/>
</element>
```

---

### 3.3 平移（Translate）

**XML模板：**
```xml
<!-- 平移向量终点 -->
<element type="point" label="V">
    <coords x="3" y="2" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 原点 -->
<element type="point" label="A">
    <coords x="1" y="1" z="1"/>
    <show object="true" label="true"/>
</element>

<!-- 平移后的点 -->
<command name="Translate">
    <input a0="A"/>
    <input a1="V"/>
    <output a0="A_translated"/>
</command>
<element type="point" label="A_translated">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
</element>
```

---

## 模式4：函数与几何综合

### 4.1 函数交点与几何图形

**XML模板：**
```xml
<!-- ====== 函数交点模式 ====== -->

<!-- 一次函数 -->
<element type="function" label="f1">
    <expression label="f1" exp="0.5*x + 1" type="function"/>
    <show object="true" label="true"/>
    <objColor r="0" g="0" b="255"/>
    <lineStyle thickness="2"/>
</element>

<!-- 二次函数 -->
<element type="function" label="f2">
    <expression label="f2" exp="0.25*x^2" type="function"/>
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0"/>
    <lineStyle thickness="2"/>
</element>

<!-- 求交点 -->
<command name="Intersect">
    <input a0="f1"/>
    <input a1="f2"/>
    <output a0="A"/>
</command>
<element type="point" label="A">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 第二个交点（如果有） -->
<command name="Intersect">
    <input a0="f1"/>
    <input a1="f2"/>
    <output a0="B"/>
</command>
<element type="point" label="B">
    <show object="true" label="true"/>
    <objColor r="0" g="128" b="0" alpha="0"/>
    <pointSize val="6"/>
</element>

<!-- 与x轴交点 -->
<command name="Root">
    <input a0="f1"/>
    <output a0="X_intercept"/>
</command>
<element type="point" label="X_intercept">
    <show object="true" label="true"/>
    <objColor r="255" g="128" b="0" alpha="0"/>
</element>
```

---

## 模式5：轨迹追踪

### 5.1 动点轨迹

**XML模板：**
```xml
<!-- ====== 轨迹追踪模式 ====== -->

<!-- 滑块控制参数t -->
<element type="numeric" label="t">
    <value val="0"/>
    <slider min="0" max="1" step="0.01" type="number"/>
</element>

<!-- 动点P在线段AB上移动 -->
<element type="point" label="A"><coords x="0" y="0" z="1"/></element>
<element type="point" label="B"><coords x="10" y="0" z="1"/></element>

<command name="Segment"><input a0="A" a1="B"/><output a0="segAB"/></command>

<command name="Point">
    <input a0="segAB"/>
    <input a1="t"/>  <!-- 用滑块控制位置 -->
    <output a0="P"/>
</command>
<element type="point" label="P">
    <show object="true" label="true"/>
    <objColor r="255" g="0" b="0"/>
</element>

<!-- 从P点引出的点Q形成轨迹 -->
<element type="point" label="Q">
    <!-- Q点坐标随P点变化 -->
    <coords x="x(P)" y="sqrt(25 - (x(P)-5)^2)" z="1"/>
    <show object="true" label="false"/>
    <objColor r="0" g="128" b="0"/>
    <pointSize val="3"/>
</element>

<!-- 连线PQ -->
<command name="Segment"><input a0="P" a1="Q"/><output a0="PQ"/></command>
```

---

## 快速选择指南

| 题目类型 | 推荐模式 | 关键工具 |
|----------|----------|----------|
| 一次函数参数范围 | 模式1.1 | 滑块+动态函数 |
| 二次函数顶点问题 | 模式1.2 | 滑块+顶点计算 |
| y=mx旋转问题 | 模式1.1 | 滑块控制斜率m |
| 点在线段上移动 | 模式2.1 | Point约束工具 |
| 矩形折叠 | 模式3.1 | Mirror工具 |
| 等边三角形旋转 | 模式3.2 | Rotate+滑块 |
| 圆上动点 | 模式2.2 | 圆+Point约束 |
| 函数交点 | 模式4.1 | Intersect工具 |
| 轨迹问题 | 模式5.1 | 滑块+参数方程 |

---

*文档版本：v1.0*  
*更新日期：2026-04-19*
