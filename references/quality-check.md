# 质量复查机制

## 复查原则

**约束正确性 > 视觉美观 > 功能完整**

生成ggb文件后，必须逐项检查以下内容。任何约束工具使用错误都必须在打包前修正。

---

## 复查清单

### 阶段1：题目理解正确性（必须在生成XML前完成）

#### 1.1 题目类型判断

- [ ] **类型识别正确** - 静态几何 / 动态几何 / 函数图像 / 尺规作图 / 证明题
- [ ] **核心对象完整** - 所有顶点、边、特殊点都已识别
- [ ] **隐藏条件发现** - 等腰/等边/直角/平行/相似/中点等隐含条件已提取

#### 1.2 约束条件提取

| 约束类型 | 检查项 | 常见遗漏 |
|----------|--------|----------|
| 位置约束 | 点在线上/延长线上/圆上 | "E在BC上"是否识别 |
| 度量约束 | 长度、角度、半径 | AB=10 是否记录 |
| 关系约束 | 中点、平行、垂直、角平分 | 是否用工具实现 |
| 动态约束 | 动点、范围、最值 | 是否标记为动态 |

#### 1.3 已知/未知区分

- [ ] **已知条件** - 黑色实线，已标注
- [ ] **所求目标** - 红色粗线（thickness="4"），突出显示
- [ ] **辅助线** - 虚线（type="1"），绿色或灰色
- [ ] **隐藏条件** - 文本标注说明（如"AB=AC"）

---

### 阶段2：几何元素完整性

- [ ] **所有顶点** - 是否都有定义且显示
- [ ] **所有边线** - 是否都正确连接
- [ ] **特殊点** - 中点、交点、垂足等是否正确计算
- [ ] **约束关系** - 点是否在线段上、平行垂直关系等
- [ ] **圆和弧** - 圆心、半径、切线是否正确
- [ ] **函数图像** - 表达式、关键点、交点是否正确

---

### 阶段3：工具使用正确性（最关键！）

| 功能 | 必须使用的工具 | 检查项 | 错误示例 |
|------|---------------|--------|----------|
| 中点 | `Midpoint` | 不是手动计算坐标 | `<coords x="1" y="3"/>` |
| 角平分线 | `AngleBisector` | 不是手动画线 | 手动创建两点连线 |
| 垂线 | `PerpendicularLine` | 不是斜率计算 | 通过斜率-1计算 |
| 交点 | `Intersect` | 不是估算坐标 | 手动写交点坐标 |
| 点在线段上 | `Point`工具约束 | 不是自由点 | `<coords>`直接定义 |
| 平行线 | `Line`（点+平行线） | 不是斜率相同 | 手动算平行斜率 |
| 垂足 | `PerpendicularLine`+`Intersect` | 不是投影计算 | 手算垂足坐标 |
| 圆 | `Circle`工具 | 不是手动画弧 | 多段线段拼圆 |
| 切线 | `Tangent`工具 | 不是目测画线 | 手动画一条近似线 |
| 延长线 | `Line`+`Point`（参数>1） | 不是随意放远点 | 远处随意坐标 |

**验证方法：** 打开ggb文件后，尝试拖动基础点，检查约束是否保持。

---

### 阶段4：标注信息

- [ ] **点标签** - A、B、C、D等是否正确标注
- [ ] **长度标注** - AB=10、AC=6等已知长度是否显示（caption或文本）
- [ ] **所求线段** - DF=?等是否突出显示（加粗/颜色）
- [ ] **角度标注** - 直角、特殊角度是否标注（Angle工具）
- [ ] **函数标注** - 函数表达式是否显示

---

### 阶段5：文本信息

- [ ] **OCR题目** - 是否完整显示在文本框
- [ ] **已知条件** - "已知：..."是否单独标注
- [ ] **所求目标** - "求：..."是否红色标注
- [ ] **答案** - 答案是否正确显示（如有）
- [ ] **证明步骤** - 证明步骤是否完整（如有）

---

### 阶段6：图片嵌入

- [ ] **原题图片** - 是否嵌入（如有）
- [ ] **图片位置** - 是否放在合适位置（通常底部）
- [ ] **图片清晰度** - 是否能看清原题
- [ ] **布局不重叠** - 图片与图形不重叠

---

### 阶段7：视觉呈现

- [ ] **颜色区分** - 不同元素用不同颜色区分
- [ ] **线型区分** - 实线、虚线使用恰当
- [ ] **粗细区分** - 重要线段加粗显示
- [ ] **布局合理** - 图形、文本、图片布局不重叠
- [ ] **坐标轴** - 函数题显示坐标轴，几何题通常隐藏

---

## 复查流程

```
题目理解检查 → 约束工具检查 → 生成XML → 逐项复查 → 修正问题 → 打包ggb → 最终验证
     ↑___________________________________________________________↓
```

**强制要求：** 阶段3（工具使用正确性）的任何失败都必须在打包前修正。

---

## 常见错误检查

### 错误1：点不在线段上

**症状：** 点可以拖到线段外

**解决：** 使用Point工具约束
```xml
<command name="Point">
    <input a0="sideBC"/>
    <output a0="E"/>
</command>
```

### 错误2：中点坐标错误

**症状：** 中点不在正确位置

**解决：** 使用Midpoint工具
```xml
<command name="Midpoint">
    <input a0="A" a1="B"/>
    <output a0="M"/>
</command>
```

### 错误3：垂足位置错误

**症状：** 垂足不在垂线上

**解决：** PerpendicularLine + Intersect
```xml
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

### 错误4：缺少长度标注

**症状：** AB=10未在图中显示

**解决：** 添加caption或使用文本框
```xml
<element type="segment" label="sideAB">
    <caption val="10"/>
</element>
```

### 错误5：图片未嵌入

**症状：** 打开ggb看不到原题图片

**解决：** 使用Image命令嵌入
```xml
<command name="Image">
    <input a0="&quot;data:image/png;base64,...&quot;"/>
    <input a1="(-3, -8)"/>
    <input a2="(16, 0)"/>
    <input a3="(0, 10)"/>
    <output a0="originalFigure"/>
</command>
```

### 错误6：平行线不平行

**症状：** 拖动点后平行线不再平行

**解决：** 使用Line工具的平行模式
```xml
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

### 错误7：角平分线不正确

**症状：** 角平分线不是准确平分

**解决：** 使用AngleBisector工具
```xml
<command name="AngleBisector">
    <input a0="B" a1="A" a2="C"/>
    <output a0="bisector"/>
</command>
```

### 错误8：圆的切线不垂直于半径

**症状：** 切线与半径不垂直

**解决：** 使用Tangent工具
```xml
<command name="Tangent">
    <input a0="P"/>
    <input a1="c1"/>
    <output a0="t1"/>
    <output a0="t2"/>
</command>
```

### 错误9：所求目标未突出

**症状：** 所求线段/角与其他元素无区分

**解决：** 使用红色加粗
```xml
<element type="segment" label="segMN">
    <objColor r="255" g="0" b="0" alpha="0"/>
    <lineStyle thickness="4" type="0"/>
</element>
```

### 错误10：动态点不能拖动

**症状：** 动点固定不动

**解决：** 确保使用Point工具约束到线段/圆
```xml
<command name="Point">
    <input a0="sideCD"/>     <!-- 不是 coords -->
    <output a0="P"/>
</command>
```

---

## 自动检查脚本

```python
def check_ggb_quality(xml_content):
    """
    自动检查ggb质量
    """
    checks = {
        # 基础约束工具
        'midpoint_tool': '<command name="Midpoint">' in xml_content,
        'angle_bisector_tool': '<command name="AngleBisector">' in xml_content,
        'perpendicular_tool': '<command name="PerpendicularLine">' in xml_content,
        'intersect_tool': '<command name="Intersect">' in xml_content,
        'parallel_tool': '<command name="Line">' in xml_content and 'line' in xml_content,
        'circle_tool': '<command name="Circle">' in xml_content,
        'tangent_tool': '<command name="Tangent">' in xml_content,
        'angle_tool': '<command name="Angle">' in xml_content,

        # 基本元素
        'text_element': '<element type="text"' in xml_content,
        'image_element': '<element type="image"' in xml_content,
        'segment_caption': '<caption val=' in xml_content,

        # 约束正确性（负面检查）
        'no_manual_midpoint': 'Midpoint' in xml_content or '<coords' not in xml_content,
    }

    # 检查是否有手动坐标替代约束工具
    manual_issues = []
    if '<coords' in xml_content and '<command name="Midpoint">' not in xml_content:
        # 有点坐标但没有中点工具 - 可能手动计算了中点
        pass  # 需要进一步人工检查

    for check_name, result in checks.items():
        status = "OK" if result else "MISSING"
        print(f"{check_name}: {status}")

    return all(checks.values())
```

---

## 约束正确性验证（关键！）

打开生成的ggb文件，执行以下验证：

### 1. 拖动测试
- [ ] 拖动顶点A、B、C，看整体图形是否保持约束关系
- [ ] 检查点是否始终在线段上（如E在BC上）
- [ ] 检查中点是否始终在中点位置

### 2. 平行垂直测试
- [ ] 拖动基础点后，平行线是否仍平行
- [ ] 拖动基础点后，垂线是否仍垂直
- [ ] 垂足是否始终在正确位置

### 3. 圆相关测试
- [ ] 拖动圆心，圆是否跟随移动
- [ ] 拖动圆上点，半径是否保持不变
- [ ] 切线是否始终与半径垂直

### 4. 角度测试
- [ ] 角平分线是否始终平分角度
- [ ] 直角标记是否始终为90°

### 5. 动态测试（动态几何题）
- [ ] 动点是否可以沿线段/圆拖动
- [ ] 依赖动点的元素是否自动更新
- [ ] 轨迹是否可见（如开启trace）

---

## 复查记录表

| 检查项 | 检查结果 | 备注 |
|--------|----------|------|
| 题目类型判断正确 | | |
| 隐藏条件已提取 | | |
| 已知/未知已区分 | | |
| 几何元素完整 | | |
| 约束工具使用正确 | | |
| 标注信息完整 | | |
| 文本信息完整 | | |
| 图片嵌入（如有） | | |
| 视觉呈现良好 | | |
| 拖动测试通过 | | |
| **整体通过** | | |
