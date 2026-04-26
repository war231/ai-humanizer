"""
测试 AI 模式检测器
"""

import pytest
from ai_humanizer.detector import Detector


def test_detector_initialization():
    """测试检测器初始化"""
    detector = Detector()
    assert detector.patterns is not None
    assert "content" in detector.patterns
    assert "language" in detector.patterns
    assert "style" in detector.patterns
    assert "communication" in detector.patterns


def test_detect_ai_vocabulary():
    """测试检测 AI 词汇"""
    detector = Detector()
    
    text = "此外，这个项目至关重要，我们需要深入探讨其复杂性。"
    results = detector.detect(text)
    
    assert results["total_patterns"] > 0
    assert any("AI 词汇" in d.pattern_name for d in results["details"])


def test_detect_promotional_language():
    """测试检测宣传性语言"""
    detector = Detector()
    
    text = "这是一个充满活力的项目，拥有丰富的文化遗产。"
    results = detector.detect(text)
    
    assert results["total_patterns"] > 0
    assert any("宣传" in d.pattern_name for d in results["details"])


def test_detect_no_patterns():
    """测试检测无 AI 模式的文本"""
    detector = Detector()
    
    text = "今天天气不错。我去公园散步。"
    results = detector.detect(text)
    
    # 简单的日常对话应该很少有 AI 模式
    assert results["total_patterns"] < 3


def test_get_pattern_summary():
    """测试获取模式摘要"""
    detector = Detector()
    
    text = "此外，这个项目至关重要。"
    summary = detector.get_pattern_summary(text)
    
    assert "检测到" in summary
    assert "AI 写作模式" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
