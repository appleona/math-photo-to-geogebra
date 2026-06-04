# 图片嵌入与图形校对

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 题目理解要点
> - [动态演示模式](dynamic-demo-patterns.md) - XML模板
> - [常见理解偏差](common-misunderstandings.md) - 偏差修正
> - [XML快速参考](xml-cheatsheet.md) - XML语法
> - [质量复查机制](quality-check.md) - 检查清单
> - [常见几何构造](common-patterns.md) - 几何模式

---

## ⚠️ 重要限制说明

### 图片嵌入在GeoGebra 6.0中的问题

**现状：直接嵌入原题图片（base64编码）到.ggb文件中，在GeoGebra 6.0 Classic中大概率会加载失败。**

**原因：**
- 原题图片通常为 100KB ~ 1MB
- Base64编码后体积膨胀约33%
- GeoGebra 6.0 对XML中内嵌大字符串的支持不稳定
- 超过 ~10KB 的base64图片基本无法加载

**错误表现：**
- 打开.ggb文件后图片区域空白
- 显示红色错误标记或"加载失败"
- GeoGebra控制台报错

---

## 推荐的替代方案

### 方案1：文本描述替代图片（推荐）

**在GeoGebra中用Text命令显示题目文字，而非嵌入原图。**

```xml
<!-- 方案1A：简单文本 -->
<command name="Text">
    <input a0="&quot;【原题】菱形ABCD边长8，∠ABC=120°，E是AB中点，M是AC上动点，求BM+EM最小值&quot;"/>
    <input a1="(-8, 8)"/>
    <output a0="problemText"/>
</command>
<element type="text" label="problemText">
    <show object="true" label="false"/>
    <fontSize val="11"/>
</element>
```

```xml
<!-- 方案1B：分行显示长文本 -->
<command name="Text">
    <input a0="&quot;【原题】在平面直角坐标系xOy中，一次函数y=kx+b(k≠0)&quot;"/>
    <input a1="(-10, 8)"/>
    <output a0="line1"/>
</command>
<element type="text" label="line1"><show object="true" label="false"/><fontSize val="10"/></element>

<command name="Text">
    <input a0="&quot;的图象经过点(4,1)和(0,-1)。&quot;"/>
    <input a1="(-10, 6.5)"/>
    <output a0="line2"/>
</command>
<element type="text" label="line2"><show object="true" label="false"/><fontSize val="10"/></element>
```

**优点：**
- ✅ 文件体积小（<2KB）
- ✅ 加载速度快
- ✅ 文字清晰可搜索
- ✅ 可配合坐标系调整位置

---

### 方案2：外部图片链接（实验性）

**将图片上传到图床，在GeoGebra中使用URL引用。**

```xml
<command name="Image">
    <input a0="&quot;https://your-image-host.com/problem.jpg&quot;"/>
    <input a1="(-2, -8)"/>
    <input a2="(14, 0)"/>
    <input a3="(0, 10)"/>
    <output a0="originalFigure"/>
</command>
```

**限制：**
- ⚠️ 需要联网才能加载
- ⚠️ 需要可靠的图床（GitHub Raw URL等）
- ⚠️ 图片URL可能失效

**步骤：**
1. 将图片上传到GitHub Issue、Gist或其他图床
2. 获取图片的直接访问URL（以 .jpg/.png 结尾）
3. 将URL写入XML

---

### 方案3：极简压缩图片（有限支持）

**将原图压缩到 <1KB 后嵌入。**

```python
from PIL import Image
import io, base64

def compress_to_tiny_image(input_path, output_size=(50, 35), quality=10):
    """
    将图片压缩到极小尺寸（<1KB），可能可用于GeoGebra嵌入
    注意：压缩后图片可能无法辨认文字，仅能看大致图形轮廓
    """
    img = Image.open(input_path)
    img = img.convert('RGB')
    img = img.resize(output_size, Image.LANCZOS)
    
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    
    data = buffer.getvalue()
    print(f"Compressed size: {len(data)} bytes")
    
    if len(data) > 1000:
        print("WARNING: Still >1KB, may not load in GeoGebra")
    
    return base64.b64encode(data).decode('utf-8')
```

**限制：**
- ⚠️ 图片极小，文字无法辨认
- ⚠️ 仅能显示大致图形轮廓
- ⚠️ 实际效果不稳定

---

### 方案4：Side-by-Side 分屏查看（最佳实践）

**不嵌入图片，而是分屏显示。**

| 屏幕左侧 | 屏幕右侧 |
|---------|---------|
| 原始题目图片（PDF/照片查看器） | GeoGebra交互图形 |

**实现：**
- 无需嵌入图片到.ggb文件
- 在电脑上并排打开两个窗口
- 左眼看原题，右眼操作GeoGebra

**优点：**
- ✅ 最稳定可靠
- ✅ 原图清晰度不受损
- ✅ 文件体积极小
- ✅ 适合课堂投影（左题右图）

---

## 图片嵌入XML语法（备用参考）

如果将来GeoGebra修复了大图片支持，语法如下：

```xml
<command name="Image">
    <input a0="&quot;data:image/png;base64,iVBORw0KGgo...&quot;"/>
    <input a1="(-2, -8)"/>    <!-- 左下角坐标 -->
    <input a2="(14, 0)"/>     <!-- 宽度向量 -->
    <input a3="(0, 10)"/>     <!-- 高度向量 -->
    <output a0="originalFigure"/>
</command>
<element type="image" label="originalFigure">
    <show object="true" label="false"/>
</element>
```

---

## 图形校对建议

由于原图无法可靠嵌入，建议采用以下校对方式：

1. **Text命令显示题目** - 在GeoGebra上方显示关键题目信息
2. **分屏对比** - 左题右图，手动对比
3. **关键数据标注** - 在GeoGebra中标出已知条件（边长、角度等）
4. **截图对比** - 将GeoGebra图形截图，与原题图片对比

---

## 总结

| 方案 | 可行性 | 推荐度 | 适用场景 |
|------|--------|--------|----------|
| **文本描述** | ✅ 高 | ⭐⭐⭐⭐⭐ | 所有场景，首选 |
| **外部链接** | ⚠️ 中 | ⭐⭐⭐ | 有稳定图床时 |
| **极简压缩** | ⚠️ 低 | ⭐⭐ | 仅需图形轮廓 |
| **分屏查看** | ✅ 高 | ⭐⭐⭐⭐⭐ | 课堂/家庭学习 |
| **base64嵌入** | ❌ 低 | ⭐ | 目前不推荐 |

---

*文档版本：v2.0（已更新限制说明）*  
*更新日期：2026-04-19*
