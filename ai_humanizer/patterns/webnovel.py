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
    "parallel_structure": {
        "name": "排比/对称结构",
        "regex": r"([\u4e00-\u9fa5]{2}而[\u4e00-\u9fa5]{2})|(有[\u4e00-\u9fa5]+?[，；].*?有[\u4e00-\u9fa5]+?[，；].*?有[\u4e00-\u9fa5]+?)|(既.*?又.*?也)|(一边.*?一边.*?一边)|(不仅.*?而且.*?还)|(不是.*?而是.*?而是)",
        "description": "AI 喜欢使用工整的排比和对称结构",
        "suggestion": "打破对称，用具体细节代替概括性排比",
    },
    "missing_life_details": {
        "name": "缺少生活化细节",
        "regex": r"(回到.*(?:直接|立刻|马上|随即|立刻就).*?)|(?:坐在.*?(?:直接|立刻|马上))",
        "description": "场景切换或情绪转变缺少生活化的过渡细节",
        "suggestion": "加入身体动作、环境反应、下意识行为等过渡",
    },
    "classical_dialogue_template": {
        "name": "标准化古文对话",
        "regex": r"(吾乃|吾便|吾辈|尔等|汝|足矣|罢了|不必多礼|晚辈|前辈|敢问|造化|有缘之人|静待)",
        "description": "AI 生成的古文对话过于标准模板化，缺乏个性",
        "suggestion": "给角色设计独特的说话方式，可以带点口语、口头禅",
    },
    "safe_vocabulary": {
        "name": "安全词库堆砌",
        "regex": r"(坚毅|睥睨|傲然|淡然|冷笑|漠然|桀骜|不驯|从容|云淡风轻|气势如虹|不卑不亢|临危不乱|气定神闲)",
        "description": "AI 过度使用网文高频'安全词'，缺乏个性",
        "suggestion": "用更具体、更生僻或更具个人风格的词替换",
    },
    "linear_logic": {
        "name": "逻辑过于顺滑",
        "regex": r"(因为.*?所以|由于.*?因此|既然.*?就|.*?于是.*?就|.*?因此.*?便)",
        "description": "AI 的逻辑链条过于顺滑直接，缺少人类思维的跳跃和断裂",
        "suggestion": "加入插叙、倒叙，或突然蹦出的无关想法，打破线性逻辑",
    },
    "coincidence_trigger": {
        "name": "巧合堆砌触发",
        "regex": r"(刚好|恰好|正好|碰巧|无意间|无意中|正巧|不偏不倚|恰巧|适逢其会)",
        "description": "AI 常用'巧合'来推动关键情节（尤其是金手指触发）",
        "suggestion": "让关键事件由角色主动行为或环境因素自然引发，减少巧合",
    },
}
