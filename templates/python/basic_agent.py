"""
AI Humanizer - 基础 Python Agent 模板

适用于任何 Python Agent 项目
"""

from ai_humanizer import Humanizer
from typing import Dict, Any, Optional


class BasicHumanizerAgent:
    """基础 AI Humanizer Agent"""

    def __init__(self, model: str = "gpt-4"):
        """
        初始化 Agent

        Args:
            model: 使用的 LLM 模型
        """
        self.humanizer = Humanizer(model=model)

    def detect(self, text: str) -> Dict[str, Any]:
        """
        检测文本中的 AI 写作模式

        Args:
            text: 待检测的文本

        Returns:
            检测结果
        """
        return self.humanizer.detect(text)

    def rewrite(self, text: str, tone: str = "neutral") -> str:
        """
        人性化重写文本

        Args:
            text: 待重写的文本
            tone: 目标语调 (neutral/formal/casual/technical)

        Returns:
            重写后的文本
        """
        return self.humanizer.rewrite(text, tone=tone)

    def score(self, text: str) -> Dict[str, Any]:
        """
        评估文本人性化程度

        Args:
            text: 待评估的文本

        Returns:
            评分结果
        """
        return self.humanizer.score(text)

    def process(self, text: str, auto_rewrite: bool = True) -> Dict[str, Any]:
        """
        完整处理流程：检测 → 重写 → 评分

        Args:
            text: 待处理的文本
            auto_rewrite: 是否自动重写（当 AI 模式过多时）

        Returns:
            处理结果
        """
        # Step 1: 检测
        detection = self.detect(text)

        # Step 2: 决定是否重写
        if auto_rewrite and detection["total_patterns"] > 3:
            humanized = self.rewrite(text)
            score = self.score(humanized)
            return {
                "original": text,
                "humanized": humanized,
                "detection": detection,
                "score": score,
                "rewritten": True
            }
        else:
            score = self.score(text)
            return {
                "original": text,
                "humanized": text,
                "detection": detection,
                "score": score,
                "rewritten": False
            }


# 使用示例
if __name__ == "__main__":
    # 初始化 Agent
    agent = BasicHumanizerAgent()

    # 示例文本
    text = """
    此外，这个项目至关重要。我们需要深入探讨其复杂性。
    这不仅仅是一个项目，而是我们思考方式的革命。
    行业专家认为这将对整个行业产生持久影响。
    """

    # 检测
    detection = agent.detect(text)
    print(f"检测到 {detection['total_patterns']} 种 AI 模式")

    # 重写
    humanized = agent.rewrite(text)
    print(f"重写结果: {humanized}")

    # 评分
    score = agent.score(humanized)
    print(f"质量评分: {score['total_score']}/50")

    # 完整处理
    result = agent.process(text)
    print(f"处理结果: {result}")
