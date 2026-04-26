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
- 对感受要具体，不要用模糊的描述"""

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
        
        # 调用 LLM 进行重写
        # 这里需要根据实际使用的 LLM API 进行实现
        # 示例使用 OpenAI API
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
        except ImportError:
            # 如果没有安装 openai，返回提示信息
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
        }
        
        return f"""请重写以下文本，去除 AI 写作痕迹。

## 检测到的 AI 模式

{pattern_text}

## 目标语调

{tone_guide.get(tone, tone_guide['neutral'])}

## 原文

{text}

## 要求

1. 保留核心信息和含义
2. 去除所有检测到的 AI 模式
3. 注入真实的个性和语调
4. 变化句子长度和结构
5. 使用具体细节而非模糊描述

请直接输出重写后的文本，不要添加解释。"""
    
    def _fallback_rewrite(self, text: str, patterns: Dict[str, Any]) -> str:
        """降级重写方案（不使用 LLM）"""
        # 简单的规则替换
        import re
        
        result = text
        
        # 移除常见的填充词
        fillers = [
            r"此外[，,]",
            r"值得注意的是[，,]",
            r"需要指出的是[，,]",
            r"总而言之[，,]",
            r"综上所述[，,]",
        ]
        
        for filler in fillers:
            result = re.sub(filler, "", result)
        
        return result.strip()
