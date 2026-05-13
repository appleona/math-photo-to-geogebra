# 图片嵌入与图形校对

> 📚 **相关文档：**
> - [题目理解指南](problem-analysis-guide.md) - 题目理解要点
> - [动态演示模式](dynamic-demo-patterns.md) - XML模板
> - [常见理解偏差](common-misunderstandings.md) - 偏差修正
> - [XML快速参考](xml-cheatsheet.md) - XML语法
> - [质量复查机制](quality-check.md) - 检查清单
> - [常见几何构造](common-patterns.md) - 几何模式



## 功能说明

将原题图片嵌入GeoGebra文件，与生成的几何图形并排显示，方便对比校对。

## 使用场景

1. **校对验证** - 对比生成图形与原题图片是否一致
2. **参考作图** - 在原图基础上绘制几何图形
3. **教学演示** - 展示从题目到图形的转换过程

## 实现步骤

### 1. 图片转Base64

```python
from image_utils import image_to_base64

# 将图片转为base64编码
base64_data = image_to_base64("problem.jpg")
# 返回: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...
```

### 2. 创建图片嵌入XML

```python
from image_utils import create_image_xml

# 创建图片嵌入的XML片段
image_xml = create_image_xml(
    base64_data,
    label="originalFigure",
    pos=(-2, -8),   # 左下角坐标
    width=14,       # 图片宽度
    height=10       # 图片高度
)
```

生成的XML：

```xml
<command name="Image">
    <input a0="&quot;data:image/png;base64,iVBORw0KGgo...&quot;"/>
    <input a1="(-2, -8)"/>
    <input a2="(14, 0)"/>
    <input a3="(0, 10)"/>
    <output a0="originalFigure"/>
</command>
<element type="image" label="originalFigure">
    <show object="true" label="false"/>
</element>
```

### 3. 组合到完整ggb

```xml
<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<euclidianView>
    <viewNumber viewNo="1"/>
    <coordSystem xZero="700" yZero="500" scale="45"/>
    <evSettings axes="true" grid="true"/>
</euclidianView>
<construction>

    <!-- 上方：生成的几何图形 -->
    <command name="Text">
        <input a0="&quot;【生成图形】&quot;"/>
        <input a1="(3, 8)"/>
        <output a0="labelGenerated"/>
    </command>
    <!-- ... 几何图形 ... -->
    
    <!-- 分隔线 -->
    <command name="Segment">
        <input a0="(-2, -1)" a1="(12, -1)"/>
        <output a0="divider"/>
    </command>
    
    <!-- 下方：原题图片 -->
    <command name="Text">
        <input a0="&quot;【原题图片】&quot;"/>
        <input a1="(3, -2)"/>
        <output a0="labelOriginal"/>
    </command>
    
    <!-- 图片嵌入 -->
    <command name="Image">
        <input a0="&quot;data:image/png;base64,...&quot;"/>
        <input a1="(-2, -8)"/>
        <input a2="(14, 0)"/>
        <input a3="(0, 10)"/>
        <output a0="originalFigure"/>
    </command>
    <element type="image" label="originalFigure">
        <show object="true" label="false"/>
    </element>
    
</construction>
</geogebra>
```

## 命令行工具

### 使用 create_with_image.py

```bash
# 基本用法
python create_with_image.py problem.jpg my_problem

# 这将生成：
# - my_problem.ggb
# - my_problem.xml
```

### 功能说明

生成的ggb文件包含：
1. 上方：生成的几何图形（蓝色）
2. 中间：分隔线和说明
3. 下方：原题图片
4. 用户可以对比两者是否一致

## 图形校对清单

打开ggb文件后，检查：

- [ ] **顶点位置** - 生成图形的顶点与原图是否对应
- [ ] **边线** - 线段连接关系是否正确
- [ ] **角度** - 特殊角度（直角、等角）是否正确
- [ ] **比例** - 边长比例是否大致正确
- [ ] **标注** - 点和线的标签是否对应

## 代码示例

### 完整流程

```python
import zipfile
from image_utils import image_to_base64, create_image_xml

# 1. 读取图片
image_path = "problem.jpg"
base64_data = image_to_base64(image_path)

# 2. 创建图片XML
image_xml = create_image_xml(
    base64_data,
    label="originalFigure",
    pos=(-2, -8),
    width=14,
    height=10
)

# 3. 几何图形XML（示例）
geometry_xml = '''
<element type="point" label="A">
    <coords x="5" y="6" z="1"/>
    <show object="true" label="true"/>
</element>
<!-- ... 其他几何元素 ... -->
'''

# 4. 组合完整XML
full_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic">
<construction>
    {geometry_xml}
    {image_xml}
</construction>
</geogebra>'''

# 5. 打包为ggb
with zipfile.ZipFile('output.ggb', 'w') as zf:
    zf.writestr('geogebra.xml', full_xml.encode('utf-8'))
```

## 注意事项

1. **图片大小** - Base64编码后体积增大约33%，建议使用适当压缩的图片
2. **坐标调整** - 根据图片比例调整pos、width、height参数
3. **格式支持** - 支持PNG、JPEG、GIF等常见格式
4. **特殊字符** - base64字符串中的引号需要转义为 `&quot;`

## 完整示例文件

- `demo_image_embedding.ggb` - 图片嵌入演示
- `create_with_image.py` - 完整命令行工具
- `image_utils.py` - 图片处理工具函数
