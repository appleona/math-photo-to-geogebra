# 质量复查机制

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 题目理解要点和常见陷阱
> - [动态演示模式](dynamic-demo-patterns.md) - 动态演示标准模式
> - [常见理解偏差](common-misunderstandings.md) - 偏差识别与修正
> - [常见几何构造](common-patterns.md) - 几何构造XML模式
> - [XML快速参考](xml-cheatsheet.md) - XML语法速查



## 复查清单

生成ggb文件后，必须逐项检查以下内容：

### 1. 几何元素完整性

- [ ] **所有顶点** - 是否都有定义且显示
- [ ] **所有边线** - 是否都正确连接
- [ ] **特殊点** - 中点、交点、垂足等是否正确计算
- [ ] **约束关系** - 点是否在线段上、平行垂直关系等

### 2. 标注信息

- [ ] **点标签** - A、B、C、D等是否正确标注
- [ ] **长度标注** - AB=10、AC=6等已知长度是否显示
- [ ] **所求线段** - DF=?等是否突出显示（加粗/颜色）
- [ ] **角度标注** - 直角、特殊角度是否标注

### 3. 工具使用正确性

| 功能 | 必须使用的工具 | 检查项 |
|------|---------------|--------|
| 中点 | Midpoint | 不是手动计算坐标 |
| 角平分线 | AngleBisector | 不是手动画线 |
| 垂线 | PerpendicularLine | 不是斜率计算 |
| 交点 | Intersect | 不是估算坐标 |
| 点在线段上 | Point工具约束 | 不是自由点 |

### 4. 文本信息

- [ ] **OCR题目** - 是否完整显示在文本框
- [ ] **答案** - 答案是否正确显示
- [ ] **证明过程** - 证明步骤是否完整（如有）
- [ ] **提示信息** - 题目提示是否显示

### 5. 图片嵌入

- [ ] **原题图片** - 是否嵌入（如有）
- [ ] **图片位置** - 是否放在合适位置（通常底部）
- [ ] **图片清晰度** - 是否能看清原题

### 6. 视觉呈现

- [ ] **颜色区分** - 不同元素用不同颜色区分
- [ ] **线型区分** - 实线、虚线使用恰当
- [ ] **粗细区分** - 重要线段加粗显示
- [ ] **布局合理** - 图形、文本、图片布局不重叠

---

## 复查流程

```
生成XML → 逐项检查 → 修正问题 → 打包ggb → 最终验证
    ↑___________________________________________↓
```

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

### 错误3：缺少长度标注

**症状：** AB=10未在图中显示

**解决：** 添加caption或使用文本框
```xml
<element type="segment" label="sideAB">
    <caption val="AB=10"/>
</element>
```

### 错误4：图片未嵌入

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

---

## 自动检查脚本

```python
def check_ggb_quality(xml_content):
    """
    自动检查ggb质量
    """
    checks = {
        'midpoint_tool': '<command name="Midpoint">' in xml_content,
        'angle_bisector_tool': '<command name="AngleBisector">' in xml_content,
        'perpendicular_tool': '<command name="PerpendicularLine">' in xml_content,
        'intersect_tool': '<command name="Intersect">' in xml_content,
        'text_element': '<element type="text"' in xml_content,
        'image_element': '<element type="image"' in xml_content,
        'segment_caption': '<caption val=' in xml_content,
    }
    
    for check_name, result in checks.items():
        status = "OK" if result else "MISSING"
        print(f"{check_name}: {status}")
    
    return all(checks.values())
```

---

## 用户验证步骤

打开ggb文件后，用户应验证：

1. **拖动测试** - 拖动点A、B、C，看约束是否保持
2. **中点测试** - 检查中点是否始终在正确位置
3. **长度对比** - 对比生成图形与原题图片
4. **答案核对** - 检查答案文本是否正确

---

## 复查记录表

| 检查项 | 检查结果 | 备注 |
|--------|----------|------|
| 几何元素完整 | | |
| 标注信息完整 | | |
| 工具使用正确 | | |
| 文本信息完整 | | |
| 图片嵌入 | | |
| 视觉呈现良好 | | |
| **整体通过** | | |
