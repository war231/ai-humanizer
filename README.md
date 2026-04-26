# AI Humanizer - AI 文本检测与人性化 Skill

一个专门用于检测和去除 AI 生成文本痕迹的 **Claude Code Skill**，让文字听起来更自然、更有人味。

## 🎯 功能特性

- **AI 文本检测** - 识别 24 种 AI 写作模式
- **人性化重写** - 去除 AI 痕迹，注入真实个性
- **质量评分** - 5 维度评估文本人性化程度
- **改进建议** - 提供具体的修改建议

## 📦 安装

### 作为 Skill 使用（推荐）

将项目放在任意目录，Claude Code 会自动识别 `.codebuddy/skills/` 目录中的 Skill 文件。

```bash
# 项目已包含 Skill 定义文件
# 位置: .codebuddy/skills/ai-humanizer.md
```

### 作为 Python 包使用（可选）

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 在 Claude Code 中使用 Skill

直接向 Claude Code 发送请求，会自动加载 Skill：

```
请使用 ai-humanizer 检测这段文本中的 AI 痕迹：
[粘贴文本]
```

或者：

```
帮我人性化重写这段文本：
[粘贴文本]
```

### 命令行使用（可选）

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

### Python API 使用（可选）

```python
from ai_humanizer import Humanizer

humanizer = Humanizer()

# 检测 AI 模式
patterns = humanizer.detect(ai_text)
print(patterns)

# 人性化重写
humanized = humanizer.rewrite(ai_text)
print(humanized)

# 质量评分
score = humanizer.score(humanized)
print(score)
```

## AI 写作模式

本工具基于维基百科的 [AI 写作特征](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 指南，检测以下 24 种模式：

### 内容模式
1. 过度强调意义和遗产
2. 过度强调知名度和媒体报道
3. 以 -ing 结尾的肤浅分析
4. 宣传和广告式语言
5. 模糊归因和含糊措辞
6. 提纲式的"挑战与未来展望"

### 语言模式
7. 过度使用的"AI 词汇"
8. 避免使用"是"（系动词回避）
9. 否定式排比
10. 三段式法则过度使用
11. 刻意换词（同义词循环）
12. 虚假范围

### 风格模式
13. 破折号过度使用
14. 粗体过度使用
15. 内联标题垂直列表
16. 标题中的标题大写
17. 表情符号
18. 弯引号

### 交流模式
19. 协作交流痕迹
20. 知识截止日期免责声明
21. 谄媚/卑躬屈膝的语气

### 填充词和回避
22. 填充短语
23. 过度限定
24. 通用积极结论

## 质量评分维度

| 维度 | 评估标准 |
|------|----------|
| **直接性** | 直接陈述事实还是绕圈宣告？ |
| **节奏** | 句子长度是否变化？ |
| **信任度** | 是否尊重读者智慧？ |
| **真实性** | 听起来像真人说话吗？ |
| **精炼度** | 还有可删减的内容吗？ |

总分 50 分，45-50 分为优秀，35-44 分为良好，低于 35 分需要重新修订。

## 📁 项目结构

```
ai-humanizer/
├── .codebuddy/
│   └── skills/
│       └── ai-humanizer.md    # ⭐ Skill 定义文件（主要）
├── ai_humanizer/              # Python 核心模块（可选）
│   ├── __init__.py
│   ├── detector.py            # AI 模式检测器
│   ├── rewriter.py            # 人性化重写器
│   ├── scorer.py              # 质量评分器
│   ├── cli.py                 # 命令行工具
│   └── patterns/              # 模式定义
│       ├── content.py         # 内容模式
│       ├── language.py        # 语言模式
│       ├── style.py           # 风格模式
│       └── communication.py   # 交流模式
├── tests/                     # 测试用例
├── examples/                  # 示例文档
├── docs/                      # 文档
├── requirements.txt           # 依赖
├── pyproject.toml            # 项目配置
└── README.md
```

## 💡 Skill 使用示例

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

## 参考

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- 翻译自 [blader/humanizer](https://github.com/blader/humanizer)
- 参考 [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)

## 许可证

MIT License
