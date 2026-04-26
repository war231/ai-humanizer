# AI Humanizer - AI 文本检测与人性化工具

一个专门用于检测和去除 AI 生成文本痕迹的工具，让文字听起来更自然、更有人味。

**✨ 所有 Agent 都可以使用！**

- ✅ **Claude Code** - Skill 文件自动加载
- ✅ **OpenAI GPT-4** - CLI / API 调用
- ✅ **Anthropic Claude** - CLI / API 调用
- ✅ **LangChain** - Tool 集成
- ✅ **任何 Python Agent** - Python API
- ✅ **任何 Node.js Agent** - CLI 调用
- ✅ **任何其他 Agent** - CLI / API 调用

## 🎯 功能特性

- **AI 文本检测** - 识别 24 种 AI 写作模式
- **人性化重写** - 去除 AI 痕迹，注入真实个性
- **质量评分** - 5 维度评估文本人性化程度
- **改进建议** - 提供具体的修改建议

## 📦 安装

```bash
pip install -e .
```

## 🚀 使用方法

### 在 Claude Code 中使用 Skill

直接向 Claude Code 发送请求，会自动加载 Skill：

```
请使用 ai-humanizer 检测这段文本中的 AI 痕迹：
[粘贴文本]
```

### 命令行使用

```bash
# 检测 AI 痕迹
python -m ai_humanizer.cli detect input.txt

# 人性化重写
python -m ai_humanizer.cli rewrite input.txt -o output.txt

# 质量评分
python -m ai_humanizer.cli score input.txt

# 批量处理
python -m ai_humanizer.cli batch ./documents/
```

### Python API 使用

```python
from ai_humanizer import Humanizer

humanizer = Humanizer()

# 检测 AI 模式
patterns = humanizer.detect(text)

# 人性化重写
humanized = humanizer.rewrite(text)

# 质量评分
score = humanizer.score(humanized)
```

## 📚 文档

- **Skill 文件**: `.codebuddy/skills/ai-humanizer.md` - 最完整的文档
- **使用说明**: `docs/usage.md`
- **AI 模式详解**: `docs/patterns.md`
- **集成模板**: `templates/` 目录

## 🤝 Agent 集成

| Agent 类型 | 推荐方式 | 模板 |
|-----------|---------|------|
| Claude Code | Skill 文件 | 自动加载 |
| Python Agent | Python API | `templates/python/basic_agent.py` |
| Node.js Agent | CLI 调用 | `templates/nodejs/basic_agent.js` |
| LangChain | Tool | `templates/langchain/tool.py` |
| REST API | FastAPI | `templates/api/fastapi_server.py` |

## AI 写作模式

本工具基于维基百科的 [AI 写作特征](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 指南，检测 24 种模式：

**内容模式**：过度强调意义、过度强调知名度、肤浅分析、宣传性语言、模糊归因、公式化展望

**语言模式**：AI 词汇、系动词回避、否定式排比、三段式法则、同义词循环、虚假范围

**风格模式**：破折号过度使用、粗体过度使用、内联标题列表、标题大写、表情符号、弯引号

**交流模式**：协作痕迹、知识截止声明、谄媚语气、填充短语、过度限定、通用积极结论

## 质量评分

| 维度 | 评估标准 |
|------|----------|
| **直接性** | 直接陈述事实还是绕圈宣告？ |
| **节奏** | 句子长度是否变化？ |
| **信任度** | 是否尊重读者智慧？ |
| **真实性** | 听起来像真人说话吗？ |
| **精炼度** | 还有可删减的内容吗？ |

总分 50 分：45-50 优秀，35-44 良好，<35 需修订

## 💡 最佳实践

1. **先检测后重写** - 了解文本中有哪些 AI 模式
2. **保留核心信息** - 重写时确保不丢失关键内容
3. **人工审核** - 重写后仍需人工审核
4. **多次迭代** - 可能需要多次重写才能达到理想效果
5. **结合上下文** - 考虑文本的使用场景和目标受众

## 📁 项目结构

```
ai-humanizer/
├── .codebuddy/skills/ai-humanizer.md  # ⭐ Skill 定义文件
├── ai_humanizer/                      # Python 核心模块
├── templates/                         # Agent 集成模板
├── docs/                              # 文档
├── examples/                          # 示例
└── tests/                             # 测试
```

## 参考

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)

## 许可证

MIT License
