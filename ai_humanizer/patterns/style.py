"""
风格模式定义

检测风格层面的 AI 写作特征。
"""

STYLE_PATTERNS = {
    "dash_overuse": {
        "name": "破折号过度使用",
        "regex": r"—",
        "description": "LLM 使用破折号（—）比人类更频繁，模仿有力的销售文案",
        "suggestion": "删除破折号，使用逗号或句号",
    },
    "bold_overuse": {
        "name": "粗体过度使用",
        "regex": r"\*\*[^*]+\*\*",
        "description": "AI 聊天机器人机械地用粗体强调短语",
        "suggestion": "删除粗体，使用自然文本",
    },
    "inline_header_list": {
        "name": "内联标题垂直列表",
        "regex": r"[-*]\s*\*\*[^*]+\*\*[:：]",
        "description": "AI 输出列表，其中项目以粗体标题开头，后跟冒号",
        "suggestion": "改为自然段落或简单列表",
    },
    "title_case": {
        "name": "标题中的标题大写",
        "regex": r"#{1,6}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
        "description": "AI 聊天机器人将标题中的所有主要单词大写",
        "suggestion": "使用句子大小写（仅首字母大写）",
    },
    "emoji_overuse": {
        "name": "表情符号",
        "regex": r"[🚀💡✅🎯📊🔥💪🌟⭐🎉📝📌]",
        "description": "AI 聊天机器人经常用表情符号装饰标题或项目符号",
        "suggestion": "删除表情符号",
    },
    "curly_quotes": {
        "name": "弯引号",
        "regex": r"[""]",
        "description": "ChatGPT 使用弯引号（""）而不是直引号（\"\"）",
        "suggestion": "使用直引号或中文引号",
    },
}
