"""
AI Humanizer - AI 文本检测与人性化工具

基于维基百科的 AI 写作特征指南，检测并修复 AI 生成文本的痕迹。
"""

__version__ = "1.0.0"
__author__ = "AI Humanizer Team"

from ai_humanizer.detector import Detector
from ai_humanizer.rewriter import Rewriter
from ai_humanizer.scorer import Scorer


class Humanizer:
    """AI 文本人性化工具主类"""
    
    def __init__(self, model: str = "gpt-4"):
        """
        初始化 Humanizer
        
        Args:
            model: 使用的 LLM 模型
        """
        self.detector = Detector()
        self.rewriter = Rewriter(model=model)
        self.scorer = Scorer()
    
    def detect(self, text: str) -> dict:
        """
        检测文本中的 AI 写作模式
        
        Args:
            text: 待检测的文本
            
        Returns:
            检测结果字典，包含发现的模式列表
        """
        return self.detector.detect(text)
    
    def rewrite(self, text: str, tone: str = "neutral") -> str:
        """
        人性化重写文本
        
        Args:
            text: 待重写的文本
            tone: 目标语调 (neutral/formal/casual/technical)
            
        Returns:
            重写后的文本
        """
        patterns = self.detector.detect(text)
        return self.rewriter.rewrite(text, patterns, tone)
    
    def score(self, text: str) -> dict:
        """
        评估文本人性化程度
        
        Args:
            text: 待评估的文本
            
        Returns:
            评分结果字典，包含各维度得分和总分
        """
        # 先检测 AI 模式，再将结果传给评分器
        patterns = self.detector.detect(text)
        return self.scorer.score(text, patterns)


__all__ = ["Humanizer", "Detector", "Rewriter", "Scorer"]
