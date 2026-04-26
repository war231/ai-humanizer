"""
交流模式定义

检测交流层面的 AI 写作特征。
"""

COMMUNICATION_PATTERNS = {
    "collaborative_traces": {
        "name": "协作交流痕迹",
        "regex": r"(希望这对您有帮助|当然！|一定！|您说得完全正确！|您想要.*|请告诉我|这是一个.*)",
        "description": "作为聊天机器人对话的文本被粘贴为内容",
        "suggestion": "删除对话痕迹，直接陈述内容",
    },
    "knowledge_cutoff": {
        "name": "知识截止日期免责声明",
        "regex": r"(截至.*|根据我最后的训练更新|虽然具体细节有限|基于可用信息)",
        "description": "关于信息不完整的 AI 免责声明留在文本中",
        "suggestion": "删除免责声明，提供具体信息或删除不确定的陈述",
    },
    "sycophantic_tone": {
        "name": "谄媚/卑躬屈膝的语气",
        "regex": r"(好问题！|您说得完全正确|这是一个很好的观点|非常好的建议)",
        "description": "过于积极、讨好的语言",
        "suggestion": "删除谄媚语言，保持中性专业",
    },
    "filler_phrases": {
        "name": "填充短语",
        "regex": r"(为了实现这一目标|由于.*的事实|在这个时间点|在您需要帮助的情况下|具有.*的能力|值得注意的是数据显示)",
        "description": "不必要的填充短语",
        "suggestion": "删除填充短语，简化表达",
    },
    "over_qualification": {
        "name": "过度限定",
        "regex": r"(可以潜在地|可能被认为|可能会对.*产生一些影响)",
        "description": "过度限定陈述",
        "suggestion": "删除过度限定，直接陈述",
    },
    "generic_positive_conclusion": {
        "name": "通用积极结论",
        "regex": r"(未来看起来光明|激动人心的时代|继续追求卓越|向正确方向迈出.*一步)",
        "description": "模糊的乐观结尾",
        "suggestion": "删除模糊结尾，用具体计划或事实替代",
    },
}
