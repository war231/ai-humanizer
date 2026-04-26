# 使用指南

## 快速开始

### 1. 安装依赖

```bash
cd ai-humanizer
pip install -r requirements.txt
```

### 2. 基本使用

#### 检测 AI 模式

```bash
python -m ai_humanizer.cli detect examples/ai_text_example.txt
```

输出示例：
```
╭─────────────────── 检测结果 ───────────────────╮
│ 检测到 8 种 AI 写作模式                        │
│ 总计 15 处匹配                                 │
╰────────────────────────────────────────────────╯

┌───────────── 检测到的模式 ─────────────┐
│ 类别      │ 模式             │ 匹配数 │ 建议... │
├───────────┼──────────────────┼────────┼─────────┤
│ content   │ 过度强调意义...  │   3    │ 删除... │
│ language  │ AI 词汇          │   5    │ 使用... │
│ style     │ 破折号过度使用   │   2    │ 删除... │
└───────────────────────────────────────┘
```

#### 人性化重写

```bash
python -m ai_humanizer.cli rewrite examples/ai_text_example.txt -o output.txt
```

#### 质量评分

```bash
python -m ai_humanizer.cli score examples/human_text_example.txt
```

### 3. Python API

```python
from ai_humanizer import Humanizer

# 初始化
humanizer = Humanizer(model="gpt-4")

# 检测 AI 模式
text = "此外，这个项目至关重要。"
patterns = humanizer.detect(text)
print(f"检测到 {patterns['total_patterns']} 种模式")

# 人性化重写
humanized = humanizer.rewrite(text, tone="neutral")
print(humanized)

# 质量评分
score = humanizer.score(humanized)
print(f"得分: {score['total_score']}/50")
```

## 高级用法

### 批量处理

```bash
python -m ai_humanizer.cli batch ./documents/
```

### 自定义语调

```python
# 正式语调
humanized = humanizer.rewrite(text, tone="formal")

# 轻松语调
humanized = humanizer.rewrite(text, tone="casual")

# 技术语调
humanized = humanizer.rewrite(text, tone="technical")
```

### 仅检测特定模式

```python
from ai_humanizer.detector import Detector

detector = Detector()

# 仅检测内容模式
content_patterns = detector.patterns["content"]
for pattern_id, pattern_data in content_patterns.items():
    matches = detector._find_matches(text, pattern_data["regex"])
    if matches:
        print(f"{pattern_data['name']}: {matches}")
```

## 集成到工作流

### 与编辑器集成

可以创建编辑器插件，在保存文件前自动检测 AI 模式。

### 与 CI/CD 集成

```yaml
# .github/workflows/ai-check.yml
name: AI Content Check
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for AI patterns
        run: |
          pip install -e .
          python -m ai_humanizer.cli batch ./docs/
```

### 与 LLM 集成

```python
import openai
from ai_humanizer import Humanizer

# 在 LLM 生成文本后自动检测和重写
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "写一篇文章"}]
)

generated_text = response.choices[0].message.content

# 检测和重写
humanizer = Humanizer()
patterns = humanizer.detect(generated_text)

if patterns["total_patterns"] > 3:
    humanized = humanizer.rewrite(generated_text)
    print("已重写 AI 生成内容")
else:
    print("内容质量良好")
```

## 最佳实践

1. **先检测后重写** - 了解文本中有哪些 AI 模式
2. **保留核心信息** - 重写时确保不丢失关键内容
3. **人工审核** - 重写后仍需人工审核
4. **多次迭代** - 可能需要多次重写才能达到理想效果
5. **结合上下文** - 考虑文本的使用场景和目标受众
