# 🦀 OpenClaw 集成指南

## 架构理解

根据 ForgeAI v2 的设计，OpenClaw 通过 **CLI 命令层** 调用功能：

```
OpenClaw (Agent 编排层)
    ↓
CLI 命令层（自动化接口）
    ↓
核心功能层
    ↓
数据存储层
```

---

## ✅ OpenClaw 可以使用 AI Humanizer

### 方式 1：通过 CLI 命令（推荐）

OpenClaw 可以直接调用 AI Humanizer 的 CLI：

```bash
# 检测 AI 模式
python -m ai_humanizer.cli detect input.txt --format json

# 人性化重写
python -m ai_humanizer.cli rewrite input.txt -o output.txt --format json

# 质量评分
python -m ai_humanizer.cli score input.txt --format json

# 批量处理
python -m ai_humanizer.cli batch ./documents/ --format json
```

**返回格式**：JSON（适合 Agent 解析）

---

## 🔧 为 OpenClaw 添加专用 CLI 命令

### 修改 `ai_humanizer/cli.py`

添加 `--format json` 支持，使 OpenClaw 更容易解析：

```python
@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--format", type=click.Choice(["json", "text"]), default="text", help="输出格式")
def detect(file: str, format: str):
    """检测文件中的 AI 写作模式"""
    humanizer = Humanizer()

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    results = humanizer.detect(text)

    if format == "json":
        # JSON 格式输出（适合 OpenClaw）
        import json
        output = {
            "success": True,
            "total_patterns": results["total_patterns"],
            "total_matches": results["total_matches"],
            "categories": results["categories"],
            "details": [
                {
                    "pattern_id": d.pattern_id,
                    "pattern_name": d.pattern_name,
                    "category": d.category,
                    "matches": d.matches,
                    "suggestion": d.suggestion
                }
                for d in results["details"]
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出（适合人类阅读）
        console.print(...)
```

---

## 📦 OpenClaw 调用示例

### Python 调用

```python
import subprocess
import json

class OpenClawHumanizer:
    """OpenClaw 调用 AI Humanizer"""

    def __init__(self, humanizer_path: str = "e:/xiangmu/ai-humanizer"):
        self.humanizer_path = humanizer_path

    def detect(self, text: str) -> dict:
        """检测 AI 模式"""
        # 保存临时文件
        temp_file = "/tmp/ai_humanizer_input.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(text)

        # 调用 CLI
        result = subprocess.run(
            ["python", "-m", "ai_humanizer.cli", "detect", temp_file, "--format", "json"],
            cwd=self.humanizer_path,
            capture_output=True,
            text=True
        )

        # 解析 JSON 结果
        return json.loads(result.stdout)

    def rewrite(self, text: str, tone: str = "neutral") -> str:
        """人性化重写"""
        temp_input = "/tmp/ai_humanizer_input.txt"
        temp_output = "/tmp/ai_humanizer_output.txt"

        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(text)

        subprocess.run(
            ["python", "-m", "ai_humanizer.cli", "rewrite",
             temp_input, "-o", temp_output, "-t", tone],
            cwd=self.humanizer_path,
            capture_output=True
        )

        with open(temp_output, "r", encoding="utf-8") as f:
            return f.read()

    def score(self, text: str) -> dict:
        """质量评分"""
        temp_file = "/tmp/ai_humanizer_input.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(text)

        result = subprocess.run(
            ["python", "-m", "ai_humanizer.cli", "score", temp_file, "--format", "json"],
            cwd=self.humanizer_path,
            capture_output=True,
            text=True
        )

        return json.loads(result.stdout)


# 使用示例
if __name__ == "__main__":
    humanizer = OpenClawHumanizer()

    # 检测 AI 模式
    text = "此外，这个项目至关重要。我们需要深入探讨其复杂性。"
    result = humanizer.detect(text)
    print(f"检测到 {result['total_patterns']} 种 AI 模式")

    # 人性化重写
    humanized = humanizer.rewrite(text)
    print(f"重写结果: {humanized}")

    # 质量评分
    score = humanizer.score(humanized)
    print(f"质量评分: {score['total_score']}/50")
```

---

## 🎯 集成到 ForgeAI v2

### 作为审查 Agent 使用

在 ForgeAI v2 中，可以将 AI Humanizer 作为审查 Agent 之一：

```python
# forgeai/agents/humanizer_agent.py

import subprocess
import json
from typing import Dict, Any


class HumanizerAgent:
    """AI Humanizer 审查 Agent"""

    def __init__(self, humanizer_path: str = "e:/xiangmu/ai-humanizer"):
        self.humanizer_path = humanizer_path
        self.name = "HumanizerAgent"
        self.role = "AI 痕迹检测与人性化"

    def review(self, chapter_path: str) -> Dict[str, Any]:
        """审查章节"""
        # 读取章节内容
        with open(chapter_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 检测 AI 模式
        result = subprocess.run(
            ["python", "-m", "ai_humanizer.cli", "detect", chapter_path, "--format", "json"],
            cwd=self.humanizer_path,
            capture_output=True,
            text=True
        )

        detection = json.loads(result.stdout)

        # 质量评分
        result = subprocess.run(
            ["python", "-m", "ai_humanizer.cli", "score", chapter_path, "--format", "json"],
            cwd=self.humanizer_path,
            capture_output=True,
            text=True
        )

        score = json.loads(result.stdout)

        # 返回审查报告
        return {
            "agent": self.name,
            "chapter": chapter_path,
            "ai_patterns": detection["total_patterns"],
            "humanization_score": score["total_score"],
            "grade": score["grade"],
            "issues": [
                {
                    "type": "ai_pattern",
                    "pattern": detail["pattern_name"],
                    "count": len(detail["matches"]),
                    "suggestion": detail["suggestion"]
                }
                for detail in detection["details"]
            ],
            "recommendation": "需要人性化重写" if score["total_score"] < 35 else "质量良好"
        }


# 在 ForgeAI v2 CLI 中集成
# forgeai/cli.py

def handle_review(args) -> Dict[str, Any]:
    """处理 review 命令"""
    from forgeai.agents.humanizer_agent import HumanizerAgent

    # 调用 HumanizerAgent
    humanizer = HumanizerAgent()
    chapter_path = f"4-正文/第{args.chapter}章.md"
    humanizer_report = humanizer.review(chapter_path)

    # 合并其他 Agent 报告
    return {
        "success": True,
        "message": f"第 {args.chapter} 章审查完成",
        "reports": {
            "consistency": {"score": 85, "issues": []},
            "quality": {"score": 90, "issues": []},
            "plot": {"score": 88, "issues": []},
            "humanizer": humanizer_report  # 新增 AI Humanizer 报告
        }
    }
```

---

## 🔄 OpenClaw 编排示例

### 作为独立工具使用

```python
# openclaw/workflows/humanizer_workflow.py

from typing import Dict, Any
from openclaw import Agent, Task, Workflow


class HumanizerWorkflow(Workflow):
    """AI Humanizer 工作流"""

    def __init__(self):
        super().__init__()
        self.humanizer_path = "e:/xiangmu/ai-humanizer"

    def run(self, input_text: str) -> Dict[str, Any]:
        """执行工作流"""
        # Step 1: 检测 AI 模式
        detection = self.detect_ai_patterns(input_text)

        # Step 2: 如果 AI 模式过多，进行重写
        if detection["total_patterns"] > 3:
            humanized = self.humanize_text(input_text)
        else:
            humanized = input_text

        # Step 3: 质量评分
        score = self.score_text(humanized)

        # Step 4: 如果分数过低，再次重写
        if score["total_score"] < 35:
            humanized = self.humanize_text(humanized, tone="casual")
            score = self.score_text(humanized)

        return {
            "original": input_text,
            "humanized": humanized,
            "score": score,
            "detection": detection
        }

    def detect_ai_patterns(self, text: str) -> dict:
        """检测 AI 模式"""
        # 调用 AI Humanizer CLI
        ...

    def humanize_text(self, text: str, tone: str = "neutral") -> str:
        """人性化重写"""
        # 调用 AI Humanizer CLI
        ...

    def score_text(self, text: str) -> dict:
        """质量评分"""
        # 调用 AI Humanizer CLI
        ...
```

---

## 📋 OpenClaw 调用流程

```
OpenClaw 编排层
    ↓
调用 AI Humanizer CLI
    ↓
python -m ai_humanizer.cli detect --format json
    ↓
返回 JSON 结果
    ↓
OpenClaw 解析并决策
    ↓
调用 AI Humanizer CLI rewrite
    ↓
返回人性化文本
```

---

## 🎯 最佳实践

### 1. 使用 JSON 格式

OpenClaw 应始终使用 `--format json` 参数，便于解析：

```bash
python -m ai_humanizer.cli detect input.txt --format json
```

### 2. 错误处理

```python
result = subprocess.run(..., capture_output=True, text=True)

if result.returncode != 0:
    # 处理错误
    print(f"Error: {result.stderr}")
    return None

try:
    return json.loads(result.stdout)
except json.JSONDecodeError:
    print("Invalid JSON output")
    return None
```

### 3. 批量处理

对于大量文本，使用批量命令：

```bash
python -m ai_humanizer.cli batch ./documents/ --format json
```

### 4. 缓存结果

避免重复处理相同文本：

```python
import hashlib

def get_cache_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# 检查缓存
cache_key = get_cache_key(text)
if cache_key in cache:
    return cache[cache_key]

# 调用 AI Humanizer
result = humanizer.detect(text)

# 缓存结果
cache[cache_key] = result
return result
```

---

## 🔗 相关链接

- **AI Humanizer GitHub**: https://github.com/war231/ai-humanizer
- **ForgeAI v2**: e:/xiangmu/小说/forge-ai-v2/
- **OpenClaw 文档**: （待补充）

---

## ✅ 总结

**OpenClaw 完全可以使用 AI Humanizer！**

### 推荐方式

1. **通过 CLI 调用** - 使用 `python -m ai_humanizer.cli` 命令
2. **使用 JSON 格式** - 添加 `--format json` 参数
3. **集成到工作流** - 作为 OpenClaw 的一个工具或 Agent
4. **集成到 ForgeAI v2** - 作为审查 Agent 之一

### 优势

- ✅ 解耦设计 - OpenClaw 和 AI Humanizer 独立运行
- ✅ 标准接口 - JSON 格式易于解析
- ✅ 灵活调用 - 支持检测、重写、评分
- ✅ 易于扩展 - 可以集成到任何 Agent 系统
