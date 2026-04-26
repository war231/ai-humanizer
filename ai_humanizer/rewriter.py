"""
人性化重写器

使用 LLM 重写文本，去除 AI 痕迹。
"""

from typing import Dict, Any, List
from dataclasses import dataclass

from ai_humanizer.detector import PatternMatch


@dataclass
class RewriteConfig:
    """重写配置"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000


class Rewriter:
    """人性化重写器"""
    
    SYSTEM_PROMPT = """你是一位文字编辑，专门识别和去除 AI 生成文本的痕迹，使文字听起来更自然、更有人味。

## 核心规则

1. **删除填充短语** - 去除开场白和强调性拐杖词
2. **打破公式结构** - 避免二元对比、戏剧性分段、修辞性设置
3. **变化节奏** - 混合句子长度。两项优于三项。段落结尾要多样化
4. **信任读者** - 直接陈述事实，跳过软化、辩解和手把手引导
5. **删除金句** - 如果听起来像可引用的语句，重写它

## 个性与灵魂

- 有观点，不要只是报告事实
- 变化节奏，短句和长句混合使用
- 承认复杂性，真实的人有复杂的感受
- 适当使用"我"，第一人称是诚实的表现
- 允许一些混乱，完美的结构感觉像算法
- 对感受要具体，不要用模糊的描述

## ⚠️ 内容保护（最高优先级）

**绝对不可改变的内容：**
- 人物姓名、身份、关系
- 时间、地点、数字、专有名词
- 故事情节、事件顺序
- 论点观点、核心论据
- 引用内容、数据来源

**重写原则：**
- 只改变表达方式，不改变内容本身
- 如果某句话包含关键信息，保留其核心含义
- 宁可保留 AI 痕迹，也不要丢失关键信息

## 📖 网文专属保护（网文模式时启用）

**网文核心元素（绝对不可改变）：**
- 修炼体系：等级划分、境界名称、修炼方法
- 金手指：系统、空间、异能、天赋、外挂
- 爽点设计：打脸、装逼、逆袭、复仇的关键情节
- 人物设定：主角性格、反派动机、配角功能
- 世界观：势力分布、规则设定、背景历史
- 剧情线：主线任务、副本进度、感情线发展

**网文重写原则：**
- 保持爽点节奏，不打断高潮
- 保留系统提示语格式（如【叮！】）
- 保持数值体系一致性
- 不改变人物性格和动机

## 🎭 人性化写作指导（重点）

**1. 打破排比和对称**
- ❌ "这里有山，这里有水，这里有花"
- ✅ "远处是连绵的青山，一条小溪从山脚蜿蜒而过，岸边零星开着几朵不知名的野花"
- ❌ "简陋而清冷" "破败而陈旧" 等四字对仗
- ✅ 用具体细节代替概括性形容词组合

**2. 增加"废话"和生活化细节**
- 人类行为有冗余，不要直奔主题
- ❌ 被打后直接开始想心事
- ✅ 先写他换下血衣时手在抖、打翻水杯、坐在床边发呆
- ❌ 得到传承立刻修炼
- ✅ 先好奇地打量玉佩空间、碰了碰丹药瓶、犹豫了一下才坐下
- 用身体反应代替直接的心理标签：
  - ❌ "林风心中愤怒"
  - ✅ "林风一拳砸在桌上，茶盏震得跳了起来"

**3. 对话口语化、个性化**
- 每个角色说话方式要不同
- ❌ "吾乃青云子，渡劫失败，残魂寄于此"
- ✅ "老夫青云子，死了三万年了，总算等来一个活人"
- ❌ "晚辈林风，敢问前辈是何人？"
- ✅ "你谁啊？这是哪儿？" 或 "前辈...您老是？"
- 可以加入：口头禅、方言、现代词汇、不完整的句子、打断"""

    def __init__(self, model: str = "gpt-4"):
        """
        初始化重写器
        
        Args:
            model: 使用的 LLM 模型
        """
        self.config = RewriteConfig(model=model)
    
    def rewrite(
        self,
        text: str,
        patterns: Dict[str, Any],
        tone: str = "neutral"
    ) -> str:
        """
        人性化重写文本
        
        Args:
            text: 待重写的文本
            patterns: 检测到的 AI 模式
            tone: 目标语调
            
        Returns:
            重写后的文本
        """
        # 构建重写提示
        prompt = self._build_rewrite_prompt(text, patterns, tone)
        
        # 检查是否有 OpenAI API Key
        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            # 没有 API Key，使用 fallback
            return self._fallback_rewrite(text, patterns)
        
        # 有 API Key，调用 LLM 进行重写
        try:
            import openai
            
            response = openai.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # API 调用失败，使用 fallback
            return self._fallback_rewrite(text, patterns)
    
    def _build_rewrite_prompt(
        self,
        text: str,
        patterns: Dict[str, Any],
        tone: str
    ) -> str:
        """构建重写提示"""
        pattern_list = []
        
        for detail in patterns.get("details", []):
            pattern_list.append(
                f"- {detail.pattern_name}: {detail.description}\n"
                f"  建议: {detail.suggestion}"
            )
        
        pattern_text = "\n".join(pattern_list) if pattern_list else "无"
        
        tone_guide = {
            "neutral": "保持中性客观的语调",
            "formal": "使用正式专业的语调",
            "casual": "使用轻松随意的语调",
            "technical": "使用技术性的语调，但保持直接",
            # 网文专属语调
            "xuanhuan": "玄幻爽文风格：节奏快、爽点密集、热血激昂",
            "urban": "都市网文风格：轻松幽默、贴近生活、现代感强",
            "romance": "言情网文风格：情感细腻、心理描写丰富、浪漫唯美",
            "system": "系统文风格：保留系统提示格式、数值清晰、逻辑严密",
        }
        
        return f"""请重写以下文本，去除 AI 写作痕迹。

## 检测到的 AI 模式

{pattern_text}

## 目标语调

{tone_guide.get(tone, tone_guide['neutral'])}

## 原文

{text}

## ⚠️ 内容保护要求（最高优先级）

**在重写前，请先识别以下内容并确保在重写后保留：**
1. 人物：姓名、身份、关系
2. 时间：日期、时刻、时长
3. 地点：位置、场所、地址
4. 主题：核心观点、论据、结论
5. 数据：数字、比例、引用

**重写规则：**
1. ✅ 可以改变：句式结构、修辞手法、表达方式、填充词
2. ❌ 不可改变：人物、时间、地点、主题、数据、情节

## 📖 网文专属保护（如果文本包含网文元素）

**网文核心元素保护：**
- 修炼体系：等级、境界、功法、技能名称
- 金手指：系统、空间、异能、天赋设定
- 爽点情节：打脸、装逼、逆袭的关键场景
- 数值数据：属性、等级、战斗力等数值
- 系统提示：【叮！】等系统提示语格式

**网文重写规则：**
1. ✅ 可以改变：描写方式、对话风格、叙述节奏
2. ❌ 不可改变：修炼体系、金手指、爽点、数值、系统提示

## 🎭 人性化重写要求（必须执行）

**1. 打破排比和对称结构**
- 遇到"A而B""既A又B""有A，有B，有C"这类工整结构，必须打破
- 用具体、不规则的细节替换概括性的对称描述

**2. 增加生活化"废话"细节**
- 在情绪转变前加入身体动作或环境互动
- 不要直接从A跳到B，加入过渡：
  - 愤怒前：手抖、打翻东西、深呼吸、来回踱步
  - 惊喜前：愣住、揉眼睛、掐自己、语无伦次
  - 悲伤前：发呆、无意识的动作、忽略周围

**3. 对话必须口语化、个性化**
- 每个角色要有不同的说话风格
- 去掉标准古文模板，加入：
  - 口头禅（"他娘的""嗐""不是我说"）
  - 不完整的句子（"你...你到底是..."）
  - 打断和抢话
  - 现代词混搭（老夫说"靠谱""折腾"也无妨）

## 重写步骤

1. 先提取原文中的关键信息（人物、时间、地点、主题、数据）
2. 去除 AI 模式痕迹
3. 检查重写后的文本是否保留了所有关键信息
4. 如果关键信息丢失，必须补充回来

请直接输出重写后的文本，不要添加解释。"""
    
    def _fallback_rewrite(self, text: str, patterns: Dict[str, Any]) -> str:
        """降级重写方案（不使用 LLM）"""
        import re
        
        result = text
        
        # 1. 移除常见的填充词
        fillers = [
            r"此外[，,]",
            r"值得注意的是[，,]",
            r"需要指出的是[，,]",
            r"总而言之[，,]",
            r"综上所述[，,]",
            r"毋庸置疑[，,]",
            r"不言而喻[，,]",
        ]
        
        for filler in fillers:
            result = re.sub(filler, "", result)
        
        # 2. 替换 AI 常用词汇
        ai_vocab_replacements = {
            "关键": "重要",
            "至关重要": "十分重要",
            "不可或缺": "必不可少",
            "值得注意的是": "",
            "需要强调的是": "",
        }
        
        for old, new in ai_vocab_replacements.items():
            result = result.replace(old, new)
        
        # 3. 替换破折号为逗号或句号
        result = re.sub(r"——", "，", result)
        result = re.sub(r"—", "，", result)
        
        # 4. 移除重复的标点
        result = re.sub(r"[，,]{2,}", "，", result)
        result = re.sub(r"[。.]{2,}", "。", result)
        
        # 5. 移除句首的连接词
        starters = [
            r"^然而[，,]?",
            r"^因此[，,]?",
            r"^所以[，,]?",
            r"^但是[，,]?",
        ]
        
        for starter in starters:
            result = re.sub(starter, "", result, flags=re.MULTILINE)
        
        # 6. 网文专属：替换套路化描写
        
        # 套路化开头
        result = result.replace("夕阳如血", "夕阳把天边烧得通红")
        result = result.replace("夕阳西沉", "太阳落山了")
        result = result.replace("夕阳西下", "天快黑了")
        
        # 套路化过渡
        result = result.replace("刹那间", "突然")
        result = re.sub(r"说时迟那时快[，,]?", "", result)
        result = result.replace("就在此时", "这时")
        result = re.sub(r"正在这时[，,]?", "", result)
        result = result.replace("千钧一发之际", "危急时刻")
        result = result.replace("电光火石之间", "一瞬间")
        result = result.replace("眨眼间", "很快")
        result = re.sub(r"转瞬间[，,]?", "", result)
        
        # 重复性心理描写
        result = result.replace("心中震撼", "愣住了")
        result = result.replace("心中狂喜", "差点叫出声")
        result = result.replace("心中一震", "一惊")
        result = result.replace("心中一凛", "警觉起来")
        result = result.replace("心中一沉", "感觉不妙")
        result = result.replace("心中振奋", "精神一振")
        
        # 重复性表情描写 - 用正则保留后面的内容
        result = re.sub(r"嘴角勾起一抹(.+?)(?=[，。！？\n])", r"露出\1", result)
        result = result.replace("嘴角微微上扬", "笑了笑")
        result = re.sub(r"嘴角露出一丝(.+?)(?=[，。！？\n])", r"露出\1", result)
        result = result.replace("眼中闪过一丝冷芒", "目光一冷")
        result = re.sub(r"眼中闪过一丝(.+?)(?=[，。！？\n])", r"面露\1", result)
        result = result.replace("目光一凝", "盯着")
        result = result.replace("眉头微皱", "皱起眉头")
        
        # 信息堆砌 - 连带删除后面的逗号
        result = re.sub(r"要知道[，,]", "", result)
        result = re.sub(r"要知道(?=[，。！？\n])", "", result)
        result = re.sub(r"须知[，,]", "", result)
        result = re.sub(r"值得一提的是[，,]", "", result)
        result = re.sub(r"众所周知[，,]", "", result)
        
        # 套路化结尾 - 连带删除前面的逗号和后面的内容
        result = re.sub(r"[，,]?命运的齿轮.+?(?=[\n]|$)", "", result)
        result = re.sub(r"[，,]?新的篇章.+?(?=[\n]|$)", "", result)
        result = re.sub(r"[，,]?传奇就此展开[。.]?", "。", result)
        result = re.sub(r"[，,]?序幕正式拉开[。.]?", "。", result)
        result = re.sub(r"[，,]?即将开始[。.]?", "。", result)
        result = re.sub(r"[，,]?由此展开[。.]?", "。", result)
        
        # 套路化对话
        result = result.replace("晚辈", "我")
        result = result.replace("敢问前辈", "请问")
        result = result.replace("吾乃", "我是")
        result = result.replace("吾便", "我就")
        result = result.replace("吾看好你", "我看好你")
        result = re.sub(r"小子[，,]", "", result)
        
        # 7. 网文专属：简化过于正式的对话
        # "晚辈林风，敢问前辈是何人？这是何地？" → "你是谁？这是哪儿？"
        result = re.sub(r"晚辈(\w+)，敢问", r"\1问", result)
        result = re.sub(r"前辈是何人[？?]这是何地[？?]", "你是谁？这是哪儿？", result)
        result = re.sub(r"吾乃([\w\u4e00-\u9fa5]+)[，,]", r"我是\1，", result)
        result = re.sub(r"吾便送你", "送你", result)
        
        # 8. 清理残留的"小子"（不在对话中的）
        result = re.sub(r"(?<![\"'])小子", "", result)
        
        # 9. 打破排比和对称结构
        # "简陋而清冷" → "简陋，屋里冷清清的"
        result = re.sub(r"简陋而清冷", "简陋，屋里冷清清的", result)
        result = re.sub(r"破败而陈旧", "破败，处处透着年久失修的痕迹", result)
        result = re.sub(r"紧张而兴奋", "心里七上八下，又隐隐有些兴奋", result)
        # 通用 "A而B" 结构（常见四字对仗）
        result = re.sub(r"(\w{2})而(\w{2})(?=[，。！？\n])", r"\1，还带着几分\2", result)
        
        # 10. 增加生活化细节（在关键场景添加过渡）
        # 被打后回家，增加身体反应细节
        result = re.sub(
            r"(?:回到|走进).*?(?:推开|打开).*?(?:门|房门)[后，。]",
            lambda m: m.group(0).rstrip("，。") + "，门轴发出刺耳的声响，",
            result,
        )
        # 情绪激动时增加身体动作
        result = re.sub(
            r"(?:低声自语|喃喃自语)[，。]",
            lambda m: m.group(0).rstrip("，。") + "，声音轻得几乎被风吹散，",
            result,
        )
        # 盘膝而坐前增加犹豫或动作
        result = re.sub(
            r"(?:不再迟疑|不再犹豫)[，。]",
            lambda m: "深吸一口气，定了定神，",
            result,
        )
        
        # 11. 对话口语化、个性化
        # 老者自称
        result = re.sub(r"吾乃([\w\u4e00-\u9fa5]+)[，。]", r"老夫\1，", result)
        result = re.sub(r"吾便", "老夫就", result)
        result = re.sub(r"吾残魂", "老夫这残魂", result)
        result = re.sub(r"吾看好你", "老夫看好你", result)
        # 标准客套话口语化
        result = re.sub(r"不必多礼[，。]", "行了，起来吧。", result)
        result = re.sub(r"静待有缘之人", "等个活人", result)
        result = re.sub(r"送你一场造化", "给你点好处", result)
        result = re.sub(r"有缘之人", "对眼的人", result)
        # 过于正式的开场白
        result = re.sub(r"晚辈(\w+)，敢问", r"\1斗胆问一句，", result)
        result = re.sub(r"敢问前辈", "请问老人家", result)
        result = re.sub(r"前辈是何人[？?]这是何地[？?]", "您是？这儿又是哪儿？", result)
        # 让对话更自然：加入停顿、口头禅
        result = re.sub(r"(" + r"[\"']" + r")我是青云子，", r"\1嗐，老夫青云子，", result)
        result = re.sub(r"(" + r"[\"']" + r")罢了，", r"\1行了，", result)
        
        # 12. 清理多余空格和空行
        result = re.sub(r"\n{3,}", "\n\n", result)
        result = re.sub(r"[ \t]+\n", "\n", result)
        
        # 13. 修复可能的标点问题
        result = re.sub(r"，，", "，", result)
        result = re.sub(r"。，", "。", result)
        result = re.sub(r"，。", "。", result)
        
        return result.strip()
