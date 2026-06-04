# Math Photo to GeoGebra - Agent Guide

## Skill Information

- **Name**: math-photo-to-geogebra
- **Version**: 1.0.0
- **Target**: Hermes Agent
- **Language**: 中文 / English

## When to Use

Use this skill when the user wants to:
1. Convert photographed math problems to GeoGebra diagrams
2. Create interactive geometry figures from text descriptions
3. Generate .ggb files with OCR text and dynamic demonstrations
4. Handle plane geometry or coordinate function problems (grades 7-9)

## Key Capabilities

### Supported Problem Types

| Category | Examples | Dynamic Features |
|----------|----------|------------------|
| Triangles | Isosceles, right, equilateral | Drag vertices, midpoints |
| Quadrilaterals | Parallelogram, rectangle, rhombus | Fold, rotate transformations |
| Functions | Linear, quadratic, inverse proportional | Slider-controlled parameters |
| Circles | Tangents, chords, positions | Dynamic points on circumference |
| Transformations | Symmetry, rotation, translation | Animated transformations |

### Core Tools

```python
# Essential tools in scripts/
pack_ggb.py          # Pack XML to .ggb
image_utils.py       # Process images
```

## Workflow

```
User Input
    ↓
Analyze Problem (use references/problem-analysis-guide.md)
    ↓
Determine Dynamic Approach (use references/dynamic-demo-patterns.md)
    ↓
Generate XML (use references/xml-cheatsheet.md)
    ↓
Pack to .ggb (use scripts/pack_ggb.py)
    ↓
Verify (use references/quality-check.md)
```

## Golden Rules

### 1. Native Tools Only

| Task | Correct | Incorrect |
|------|---------|-----------|
| Point on segment | `Point` command | Fixed coordinates |
| Midpoint | `Midpoint` command | Coordinate formula |
| Intersection | `Intersect` command | Manual calculation |
| Perpendicular | `PerpendicularLine` | Slope calculation |

### 2. Dynamic Over Static

- **Parameter problems** → Use sliders
- **Moving points** → Use constrained points
- **Transformation** → Use transformation tools

### 3. Common Patterns

```xml
<!-- Constrained moving point -->
<command name="Point">
    <input a0="segmentAB"/>
    <output a0="M"/>
</command>

<!-- Slider for parameter -->
<element type="numeric" label="k">
    <slider min="-3" max="3" step="0.1"/>
</element>

<!-- Dynamic function -->
<element type="function" label="f">
    <expression exp="k*x + b"/>
</element>
```

## Reference Documents

### Primary References

1. **problem-analysis-guide.md** - Problem type analysis for all grades 7-9
2. **dynamic-demo-patterns.md** - XML templates for dynamic demos
3. **common-misunderstandings.md** - Pitfalls and corrections

### Secondary References

4. **common-patterns.md** - Common geometry constructions
5. **xml-cheatsheet.md** - Quick XML syntax reference
6. **quality-check.md** - Verification checklist
7. **image-embedding.md** - Image embedding guide

## Common Mistakes to Avoid

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Static lines for y=mx | User can't explore | Use slider for m |
| Manual midpoint calc | Not dynamic | Use Midpoint tool |
| Free point for "on segment" | Can drag outside | Use Point constraint |
| Embed large images | GGB may fail | Use text or small images |

## Example Prompts

### Example 1: Linear Function with Parameter
```
User: "一次函数经过(4,1)和(0,-1)，当x>-2时mx>kx+b恒成立，求m范围"

Analysis: y=mx过原点，m controls rotation
Solution: Slider for m (0 to 1.5), show dynamic rotation
```

### Example 2: Rhombus Shortest Path
```
User: "菱形ABCD边长8，∠ABC=120°，E是AB中点，M在AC上动，求BM+EM最小值"

Analysis: General's Horse Drinking (将军饮马) problem
Solution: Symmetry transform, show BM+EM dynamic sum
```

### Example 3: Rectangle Folding
```
User: "矩形ABCD，将C沿EF折叠到AD上的C'"

Analysis: Fold = axis symmetry
Solution: Mirror tool with dynamic fold line
```

## Testing Checklist

Before delivering .ggb file:

- [ ] Drag test: Can points be dragged?
- [ ] Constraint test: Do constraints hold?
- [ ] Calculation test: Is answer correct?
- [ ] Visual test: Is display clear?
- [ ] Text test: Is OCR text complete?

## Dependencies

- Python 3.6+ (standard library only)
- GeoGebra 6.0+ (to view .ggb files)

No external packages required.
