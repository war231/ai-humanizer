"""
网文 AI 写作模式定义

检测网文特有的 AI 生成痕迹。
"""

WEBNOVEL_PATTERNS = {
    "formulaic_opening": {
        "name": "套路化开头",
        "regex": r"(夕阳如血|夕阳西沉|夕阳西下|天色渐暗|夜幕降临|晨光熹微|旭日东升|夕阳西下)",
        "description": "AI 网文常用套路化环境描写开头",
        "suggestion": "使用更具体、有细节的环境描写",
    },
    "system_prompt": {
        "name": "系统提示语",
        "regex": r"【.*?】",
        "description": "系统文常见的系统提示格式",
        "suggestion": "保持格式但减少频率",
    },
    "cultivation_numerical": {
        "name": "数值堆砌",
        "regex": r"(\d+级|\d+层|\d+阶|\d+星|\d+品|\d+点|\d+%)",
        "description": "AI 喜欢堆砌具体数值来展示等级体系",
        "suggestion": "适当减少数值展示，用描写替代",
    },
    "cliche_transitions": {
        "name": "套路化过渡",
        "regex": r"(刹那间|说时迟那时快|就在此时|正在这时|恰逢此时|千钧一发之际|电光火石之间|眨眼间|转瞬间)",
        "description": "AI 使用大量套路化时间过渡词",
        "suggestion": "减少使用频率，或用更自然的过渡",
    },
    "dramatic_punctuation": {
        "name": "戏剧性标点",
        "regex": r"(!{2,}|\?{2,}|！{2,}|？{2,})",
        "description": "AI 过度使用多重标点制造戏剧效果",
        "suggestion": "使用单个标点，通过文字表达情感",
    },
    "repetitive_descriptions": {
        "name": "重复性描写",
        "regex": r"(眼中闪过一丝.*?|嘴角勾起一抹.*?|心中一震|心中狂喜|心中震撼|心中一凛|心中一沉)",
        "description": "AI 重复使用相同的心理/表情描写模板",
        "suggestion": "变化描写方式，避免模板化",
    },
    "info_dump": {
        "name": "信息堆砌",
        "regex": r"(要知道|须知|值得一提的是|众所周知|众所周知的是|需要知道的是)",
        "description": "AI 通过旁白强行插入背景信息",
        "suggestion": "通过对话或情节自然展现背景",
    },
    "cliche_ending": {
        "name": "套路化结尾",
        "regex": r"(命运的齿轮|新的篇章|传奇|序幕|即将开始|拉开序幕|正式开启|由此展开)",
        "description": "AI 常用套路化结尾制造悬念",
        "suggestion": "用更自然的结尾，避免过度戏剧化",
    },
    "overused_metaphors": {
        "name": "过度使用的比喻",
        "regex": r"(如血|如墨|如银|如练|如虹|如龙|如虎|如狼|如鬼|如神|如仙|如魔)",
        "description": "AI 过度使用'如X'的比喻句式",
        "suggestion": "减少比喻频率，或使用更具体的描写",
    },
    "formulaic_dialogue": {
        "name": "套路化对话",
        "regex": r"(晚辈.*敢问|前辈.*这是|小子.*你|吾乃.*这便是|罢了.*吾便)",
        "description": "AI 生成的对话过于套路化",
        "suggestion": "让对话更自然，符合人物性格",
    },
}
