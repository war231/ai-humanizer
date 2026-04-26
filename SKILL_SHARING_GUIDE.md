# 🤝 AI Humanizer Skill 共享指南

## ✅ 其他 Agent 可以使用此 Skill

### 方式 1：克隆仓库（推荐）

其他 Agent 可以通过克隆您的 GitHub 仓库来使用这个 Skill：

```bash
# 克隆仓库
git clone https://github.com/war231/ai-humanizer.git

# 进入目录
cd ai-humanizer

# Skill 文件位置
# .codebuddy/skills/ai-humanizer.md
```

### 方式 2：复制 Skill 文件

只需要复制核心 Skill 文件到其他项目的 `.codebuddy/skills/` 目录：

```
ai-humanizer/.codebuddy/skills/ai-humanizer.md
    ↓
your-project/.codebuddy/skills/ai-humanizer.md
```

---

## 🎯 使用场景

### 1. Claude Code（原生支持）

Claude Code 会自动识别 `.codebuddy/skills/` 目录中的 Skill：

```
your-project/
└── .codebuddy/
    └── skills/
        └── ai-humanizer.md  ← Claude Code 自动加载
```

**使用方式：**
```
请使用 ai-humanizer 检测这段文本：
[粘贴文本]
```

### 2. 其他 AI Agent（需要适配）

#### OpenAI GPT-4 / ChatGPT

需要将 Skill 内容作为 System Prompt：

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

#### LangChain Agent

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# 读取 Skill 文件
with open('.codebuddy/skills/ai-humanizer.md', 'r', encoding='utf-8') as f:
    skill_prompt = f.read()

# 定义工具
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

## 📦 打包为 Python 包

如果其他 Agent 需要使用 Python API：

### 安装

```bash
pip install git+https://github.com/war231/ai-humanizer.git
```

### 使用

```python
from ai_humanizer import Humanizer

# 初始化
humanizer = Humanizer()

# 检测 AI 模式
patterns = humanizer.detect(text)

# 人性化重写
humanized = humanizer.rewrite(text)

# 质量评分
score = humanizer.score(humanized)
```

---

## 🔧 集成到其他工具

### 1. VS Code 扩展

可以创建 VS Code 扩展，在编辑器中直接使用：

```typescript
// extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('aiHumanizer.detect', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const text = editor.document.getText();
            // 调用 AI Humanizer API
            detectAIPatterns(text);
        }
    });

    context.subscriptions.push(disposable);
}
```

### 2. 命令行工具

已包含 CLI 工具，可以直接使用：

```bash
# 安装
pip install -r requirements.txt

# 使用
python -m ai_humanizer.cli detect input.txt
python -m ai_humanizer.cli rewrite input.txt -o output.txt
python -m ai_humanizer.cli score input.txt
```

### 3. Web API

可以创建 REST API 供其他 Agent 调用：

```python
from fastapi import FastAPI
from ai_humanizer import Humanizer

app = FastAPI()
humanizer = Humanizer()

@app.post("/detect")
def detect(text: str):
    return humanizer.detect(text)

@app.post("/rewrite")
def rewrite(text: str, tone: str = "neutral"):
    return humanizer.rewrite(text, tone=tone)

@app.post("/score")
def score(text: str):
    return humanizer.score(text)
```

---

## 🌐 发布到 Skill 市场

### 发布到 Claude Code Skill 市场（未来功能）

如果 Claude Code 未来支持 Skill 市场，可以：

1. 添加 `skill.json` 元数据文件
2. 发布到官方 Skill 仓库
3. 其他用户可以直接安装

### 发布到 npm（JavaScript 项目）

```bash
# 创建 package.json
npm init -y

# 发布
npm publish
```

### 发布到 PyPI（Python 包）

```bash
# 构建
python -m build

# 上传到 PyPI
twine upload dist/*
```

---

## 📋 Skill 兼容性矩阵

| Agent/工具 | 兼容性 | 使用方式 |
|-----------|--------|---------|
| **Claude Code** | ✅ 完全支持 | 自动加载 `.codebuddy/skills/` |
| **OpenAI GPT-4** | ✅ 支持 | 作为 System Prompt |
| **Anthropic Claude** | ✅ 支持 | 作为 System Prompt |
| **LangChain** | ✅ 支持 | 作为 Tool 或 Prompt |
| **AutoGPT** | ✅ 支持 | 作为 Plugin |
| **BabyAGI** | ✅ 支持 | 作为 Tool |
| **其他 LLM** | ✅ 支持 | 作为 System Prompt |

---

## 💡 最佳实践

### 1. 版本控制

在 Skill 文件中添加版本号：

```yaml
---
name: ai-humanizer
version: 1.0.0
metadata:
  version: 1.0.0
  last_updated: 2026-04-26
---
```

### 2. 文档完整性

确保 README.md 包含：
- 安装说明
- 使用示例
- API 文档
- 贡献指南

### 3. 测试覆盖

提供测试用例，确保 Skill 在不同环境下正常工作。

### 4. 持续更新

定期更新 Skill，修复问题，添加新功能。

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/war231/ai-humanizer
- **Skill 文件**: `.codebuddy/skills/ai-humanizer.md`
- **Python API**: `ai_humanizer/`
- **CLI 工具**: `ai_humanizer/cli.py`

---

## 📞 获取帮助

如果其他 Agent 在使用此 Skill 时遇到问题：

1. 检查 Skill 文件是否完整
2. 确认 Agent 支持 System Prompt 或 Skill 加载
3. 查看 GitHub Issues: https://github.com/war231/ai-humanizer/issues
4. 提交新 Issue 描述问题

---

**总结**：其他 Agent 可以通过克隆仓库、复制 Skill 文件或安装 Python 包来使用此 Skill。Claude Code 原生支持，其他 Agent 需要将 Skill 内容作为 System Prompt 使用。
