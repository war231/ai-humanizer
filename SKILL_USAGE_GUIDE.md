# 🎯 AI Humanizer Skill 使用指南

## 📍 Skill 文件位置

```
ai-humanizer/
└── .codebuddy/
    └── skills/
        └── ai-humanizer.md  ⭐ Skill 定义文件
```

**GitHub 地址：** https://github.com/war231/ai-humanizer/blob/main/.codebuddy/skills/ai-humanizer.md

---

## 🚀 如何使用 Skill

### 方式 1：Claude Code（自动加载）

#### 步骤 1：克隆仓库

```bash
git clone https://github.com/war231/ai-humanizer.git
```

#### 步骤 2：在 Claude Code 中使用

直接向 Claude Code 发送请求，会自动加载 Skill：

```
请使用 ai-humanizer 检测这段文本中的 AI 痕迹：
此外，这个项目至关重要。我们需要深入探讨其复杂性。
```

**Claude Code 会自动：**
1. 扫描 `.codebuddy/skills/` 目录
2. 加载 `ai-humanizer.md` Skill 文件
3. 使用 Skill 中定义的功能处理文本

---

### 方式 2：复制 Skill 文件到您的项目

如果您想在其他项目中使用：

```bash
# 复制 Skill 文件到您的项目
mkdir -p your-project/.codebuddy/skills
cp ai-humanizer/.codebuddy/skills/ai-humanizer.md your-project/.codebuddy/skills/
```

然后在您的项目中：

```
请使用 ai-humanizer 检测这段文本...
```

---

### 方式 3：其他 Agent 使用 Skill

#### OpenAI GPT-4

```python
import openai

# 读取 Skill 文件
with open('.codebuddy/skills/ai-humanizer.md', 'r', encoding='utf-8') as f:
    skill_prompt = f.read()

# 使用 Skill
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": skill_prompt},
        {"role": "user", "content": "请检测这段文本中的 AI 痕迹：\n[文本]"}
    ]
)
```

#### Anthropic Claude

```python
import anthropic

# 读取 Skill 文件
with open('.codebuddy/skills/ai-humanizer.md', 'r', encoding='utf-8') as f:
    skill_prompt = f.read()

# 使用 Skill
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=skill_prompt,
    messages=[
        {"role": "user", "content": "请人性化重写这段文本：\n[文本]"}
    ]
)
```

#### LangChain

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

# 读取 Skill 文件
with open('.codebuddy/skills/ai-humanizer.md', 'r', encoding='utf-8') as f:
    skill_prompt = f.read()

# 创建 Tool
tools = [
    Tool(
        name="AI_Humanizer",
        func=lambda text: f"{skill_prompt}\n\n请处理：{text}",
        description="AI 文本检测与人性化工具"
    )
]

# 创建 Agent
agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description")
```

---

## 📋 Skill 文件内容

Skill 文件包含：

### 1. YAML 元数据

```yaml
---
name: ai-humanizer
description: |
  AI 文本检测与人性化工具 - 检测并修复 AI 生成文本的痕迹
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  trigger: 检测 AI 写作痕迹、人性化重写文本、评估文本人性化程度
  version: 1.0.0
---
```

### 2. 核心功能

- **检测 AI 模式** - 24 种 AI 写作模式
- **人性化重写** - 去除 AI 痕迹
- **质量评分** - 5 维度评估
- **改进建议** - 具体修改建议

### 3. 详细指南

- 24 种 AI 写作模式详解
- 每种模式的示例和改写建议
- 质量评分标准
- 处理流程

---

## 🎯 使用示例

### 示例 1：检测 AI 痕迹

**用户输入：**
```
请检测这段文本中的 AI 痕迹：
新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。
```

**Skill 输出：**
```
检测结果：
- 过度强调意义和遗产（"作为...的证明"）
- AI 词汇（"此外"）
- 三段式法则（"无缝、直观和强大"）
- 宣传性语言（"无缝、直观和强大"）
- 肤浅分析（"—确保..."）

质量评分：28/50（需改进）
```

### 示例 2：人性化重写

**用户输入：**
```
请人性化重写这段文本：
新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。
```

**Skill 输出：**
```
软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的，大多数报告任务完成速度更快。

质量评分：45/50（优秀）

所做更改：
- 删除了"作为...的证明"（夸大的象征意义）
- 删除了"此外"（AI 词汇）
- 删除了"无缝、直观和强大"（三段式法则 + 宣传性）
- 添加了具体功能和具体反馈
```

---

## 🔧 高级用法

### 1. 批量处理

```bash
# 使用 CLI 批量处理
python -m ai_humanizer.cli batch ./documents/ --rewrite --output ./humanized/
```

### 2. API 调用

```bash
# 启动 API 服务器
python templates/api/fastapi_server.py

# 调用 API
curl -X POST http://localhost:8000/detect -d '{"text":"..."}'
```

### 3. 集成到工作流

```python
# OpenClaw 工作流
class HumanizerWorkflow:
    def run(self, text):
        detection = self.detect(text)
        if detection["total_patterns"] > 3:
            return self.rewrite(text)
        return text
```

---

## 📚 相关文档

- `README.md` - 项目概述
- `QUICKSTART.md` - 快速开始
- `UNIVERSAL_AGENT_INTEGRATION.md` - 所有 Agent 集成指南
- `docs/usage.md` - 详细使用说明
- `docs/patterns.md` - AI 模式详解

---

## ✅ 总结

### Skill 文件已包含在项目中

✅ `.codebuddy/skills/ai-humanizer.md` - Skill 定义文件

### 所有 Agent 都可以使用

✅ **Claude Code** - 自动加载
✅ **OpenAI GPT-4** - 作为 System Prompt
✅ **Anthropic Claude** - 作为 System Prompt
✅ **LangChain** - 作为 Tool
✅ **其他 Agent** - CLI / API / System Prompt

### 使用方式

1. **克隆仓库** - `git clone https://github.com/war231/ai-humanizer.git`
2. **直接使用** - 向 Claude Code 发送请求
3. **复制 Skill** - 复制到其他项目
4. **集成到 Agent** - 作为 System Prompt 或 Tool

---

**Skill 文件已完整推送到 GitHub，所有 Agent 都可以使用！**
