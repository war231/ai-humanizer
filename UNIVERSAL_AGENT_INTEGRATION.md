# 🌐 AI Humanizer - 通用 Agent 集成方案

## 目标

让 **所有 Agent** 都能轻松使用 AI Humanizer，无论其架构如何。

---

## 🎯 统一接口设计

### 四种调用方式

```
┌─────────────────────────────────────────────────────┐
│              所有 Agent 统一访问层                    │
└─────────────────────────────────────────────────────┘
                          ↓
    ┌─────────┬─────────┬─────────┬─────────┐
    │ 方式 1  │ 方式 2  │ 方式 3  │ 方式 4  │
    │  CLI    │  API    │ Skill   │ Plugin  │
    └────┬────┴────┬────┴────┬────┴────┬────┘
         │         │         │         │
         └─────────┴─────────┴─────────┘
                       ↓
         ┌─────────────────────────────┐
         │   AI Humanizer 核心功能      │
         │   - detect (检测)            │
         │   - rewrite (重写)           │
         │   - score (评分)             │
         └─────────────────────────────┘
```

---

## 方式 1：CLI 命令（所有 Agent 通用）

### 优势
- ✅ 语言无关 - 任何编程语言的 Agent 都能调用
- ✅ 解耦设计 - Agent 和 AI Humanizer 独立运行
- ✅ 标准输出 - JSON 格式易于解析
- ✅ 无需依赖 - 不需要安装 Python 包

### 使用方式

```bash
# 检测 AI 模式
python -m ai_humanizer.cli detect input.txt --format json

# 人性化重写
python -m ai_humanizer.cli rewrite input.txt -o output.txt --tone neutral

# 质量评分
python -m ai_humanizer.cli score input.txt --format json

# 批量处理
python -m ai_humanizer.cli batch ./documents/ --format json
```

### Agent 调用示例

#### Python Agent
```python
import subprocess
import json

def call_humanizer(text, command="detect"):
    # 保存临时文件
    with open("/tmp/input.txt", "w") as f:
        f.write(text)
    
    # 调用 CLI
    result = subprocess.run(
        ["python", "-m", "ai_humanizer.cli", command, "/tmp/input.txt", "--format", "json"],
        capture_output=True,
        text=True
    )
    
    return json.loads(result.stdout)
```

#### Node.js Agent
```javascript
const { execSync } = require('child_process');
const fs = require('fs');

function callHumanizer(text, command = 'detect') {
    // 保存临时文件
    fs.writeFileSync('/tmp/input.txt', text);
    
    // 调用 CLI
    const result = execSync(
        `python -m ai_humanizer.cli ${command} /tmp/input.txt --format json`,
        { encoding: 'utf-8' }
    );
    
    return JSON.parse(result);
}
```

#### Shell Agent
```bash
#!/bin/bash
TEXT="此外，这个项目至关重要。"
echo "$TEXT" > /tmp/input.txt

# 调用 CLI
python -m ai_humanizer.cli detect /tmp/input.txt --format json
```

---

## 方式 2：Python API（Python Agent 专用）

### 优势
- ✅ 高性能 - 直接调用，无进程开销
- ✅ 类型安全 - 完整的类型提示
- ✅ 易于调试 - 可以单步调试
- ✅ 灵活配置 - 可以自定义参数

### 安装

```bash
pip install git+https://github.com/war231/ai-humanizer.git
```

### 使用方式

```python
from ai_humanizer import Humanizer

# 初始化
humanizer = Humanizer(model="gpt-4")

# 检测 AI 模式
patterns = humanizer.detect(text)
print(f"检测到 {patterns['total_patterns']} 种模式")

# 人性化重写
humanized = humanizer.rewrite(text, tone="neutral")
print(humanized)

# 质量评分
score = humanizer.score(humanized)
print(f"得分: {score['total_score']}/50")
```

---

## 方式 3：Skill 文件（Claude Code 专用）

### 优势
- ✅ 原生支持 - Claude Code 自动加载
- ✅ 交互式 - 支持用户交互
- ✅ 无需配置 - 放入目录即可

### 使用方式

```
your-project/
└── .codebuddy/
    └── skills/
        └── ai-humanizer.md  ← 自动加载
```

直接向 Claude Code 发送请求：
```
请使用 ai-humanizer 检测这段文本：
[粘贴文本]
```

---

## 方式 4：Plugin/Tool（框架 Agent 专用）

### LangChain Tool
```python
from langchain.tools import Tool
from ai_humanizer import Humanizer

humanizer = Humanizer()

tools = [
    Tool(
        name="ai_humanizer_detect",
        func=lambda text: str(humanizer.detect(text)),
        description="检测文本中的 AI 写作模式"
    ),
    Tool(
        name="ai_humanizer_rewrite",
        func=lambda text: humanizer.rewrite(text),
        description="人性化重写文本"
    ),
    Tool(
        name="ai_humanizer_score",
        func=lambda text: str(humanizer.score(text)),
        description="评估文本人性化程度"
    )
]
```

### AutoGPT Plugin
```python
from plugins import Plugin
from ai_humanizer import Humanizer

class AIHumanizerPlugin(Plugin):
    def __init__(self):
        self.humanizer = Humanizer()
    
    def detect_ai_patterns(self, text):
        return self.humanizer.detect(text)
    
    def humanize_text(self, text):
        return self.humanizer.rewrite(text)
```

---

## 🌍 支持的 Agent 列表

### ✅ 完全支持

| Agent | 推荐方式 | 难度 |
|-------|---------|------|
| **Claude Code** | Skill 文件 | ⭐ 简单 |
| **OpenAI GPT-4** | CLI / API | ⭐ 简单 |
| **Anthropic Claude** | CLI / API | ⭐ 简单 |
| **LangChain** | Tool / API | ⭐ 简单 |
| **AutoGPT** | Plugin / CLI | ⭐⭐ 中等 |
| **BabyAGI** | CLI / API | ⭐ 简单 |
| **AgentGPT** | CLI / API | ⭐ 简单 |
| **OpenClaw** | CLI / API | ⭐ 简单 |
| **HermesAgent** | CLI / API | ⭐ 简单 |
| **ForgeAI v2** | CLI / API | ⭐ 简单 |

### ✅ 理论支持（需适配）

| Agent 类型 | 适配方式 |
|-----------|---------|
| **任何 Python Agent** | Python API |
| **任何 Node.js Agent** | CLI 调用 |
| **任何 Shell Agent** | CLI 调用 |
| **任何 LLM Agent** | System Prompt |
| **任何框架 Agent** | Plugin/Tool |

---

## 📦 快速集成模板

### 模板 1：Python Agent

```python
from ai_humanizer import Humanizer

class YourAgent:
    def __init__(self):
        self.humanizer = Humanizer()
    
    def process_text(self, text):
        # 检测
        detection = self.humanizer.detect(text)
        
        # 如果 AI 模式过多，重写
        if detection["total_patterns"] > 3:
            humanized = self.humanizer.rewrite(text)
            score = self.humanizer.score(humanized)
            return humanized, score
        
        return text, None
```

### 模板 2：Node.js Agent

```javascript
const { execSync } = require('child_process');
const fs = require('fs');

class YourAgent {
    processText(text) {
        // 保存临时文件
        fs.writeFileSync('/tmp/input.txt', text);
        
        // 检测
        const detection = JSON.parse(
            execSync('python -m ai_humanizer.cli detect /tmp/input.txt --format json')
        );
        
        // 如果 AI 模式过多，重写
        if (detection.total_patterns > 3) {
            execSync('python -m ai_humanizer.cli rewrite /tmp/input.txt -o /tmp/output.txt');
            return fs.readFileSync('/tmp/output.txt', 'utf-8');
        }
        
        return text;
    }
}
```

### 模板 3：LLM Agent（System Prompt）

```python
import openai

# 读取 Skill 文件作为 System Prompt
with open('.codebuddy/skills/ai-humanizer.md', 'r') as f:
    humanizer_prompt = f.read()

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": humanizer_prompt},
        {"role": "user", "content": "请检测这段文本中的 AI 痕迹：\n[文本]"}
    ]
)
```

### 模板 4：框架 Agent（LangChain）

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from ai_humanizer import Humanizer

humanizer = Humanizer()

tools = [
    Tool(
        name="AI_Humanizer",
        func=lambda x: humanizer.rewrite(x),
        description="人性化重写文本"
    )
]

agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description")
```

---

## 🔧 配置选项

### 通用配置

```python
from ai_humanizer import Humanizer

# 初始化配置
humanizer = Humanizer(
    model="gpt-4",           # LLM 模型
    temperature=0.7,         # 温度
    max_tokens=2000          # 最大 token 数
)

# 检测配置
detection = humanizer.detect(
    text,
    threshold=3,             # AI 模式阈值
    categories=["content", "language"]  # 检测类别
)

# 重写配置
humanized = humanizer.rewrite(
    text,
    tone="neutral",          # 语调: neutral/formal/casual/technical
    preserve_keywords=[],    # 保留的关键词
    max_iterations=3         # 最大迭代次数
)

# 评分配置
score = humanizer.score(
    text,
    dimensions=["directness", "rhythm", "trust", "authenticity", "conciseness"]
)
```

---

## 📊 性能优化

### 1. 批量处理

```python
# 批量检测
results = humanizer.batch_detect(
    texts,
    parallel=True,           # 并行处理
    batch_size=10            # 批次大小
)
```

### 2. 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_detect(text_hash):
    return humanizer.detect(text)
```

### 3. 异步处理

```python
import asyncio

async def async_detect(text):
    return await humanizer.async_detect(text)

# 批量异步
results = await asyncio.gather(*[
    async_detect(text) for text in texts
])
```

---

## 🌐 部署选项

### 选项 1：本地部署

```bash
git clone https://github.com/war231/ai-humanizer.git
cd ai-humanizer
pip install -r requirements.txt
```

### 选项 2：Docker 部署

```dockerfile
FROM python:3.10

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "-m", "ai_humanizer.cli"]
```

```bash
docker build -t ai-humanizer .
docker run ai-humanizer detect input.txt --format json
```

### 选项 3：API 服务

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

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 📚 完整文档

- `README.md` - 项目概述
- `QUICKSTART.md` - 快速开始
- `UNIVERSAL_AGENT_INTEGRATION.md` - 本文档
- `OPENCLAW_INTEGRATION.md` - OpenClaw 集成
- `SKILL_SHARING_GUIDE.md` - Skill 共享指南
- `docs/usage.md` - 详细使用说明
- `docs/patterns.md` - AI 模式详解

---

## ✅ 总结

**AI Humanizer 已支持所有 Agent！**

### 核心优势

1. **统一接口** - 四种调用方式，适配所有架构
2. **语言无关** - CLI 方式支持任何编程语言
3. **易于集成** - 提供完整的集成模板
4. **灵活部署** - 本地、Docker、API 多种部署方式
5. **完善文档** - 详细的集成指南和示例

### 推荐使用方式

| Agent 类型 | 推荐方式 |
|-----------|---------|
| **Claude Code** | Skill 文件 |
| **Python Agent** | Python API |
| **Node.js Agent** | CLI 调用 |
| **其他语言 Agent** | CLI 调用 |
| **框架 Agent** | Plugin/Tool |
| **LLM Agent** | System Prompt |

---

**所有 Agent 都可以使用 AI Humanizer！**
