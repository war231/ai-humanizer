"""
测试质量评分器
"""

import pytest
from ai_humanizer.scorer import Scorer


def test_scorer_initialization():
    """测试评分器初始化"""
    scorer = Scorer()
    assert scorer.DIMENSIONS is not None
    assert len(scorer.DIMENSIONS) == 5


def test_score_simple_text():
    """测试评分简单文本"""
    scorer = Scorer()
    
    text = "今天天气不错。我去公园散步。"
    results = scorer.score(text)
    
    assert "total_score" in results
    assert "grade" in results
    assert "dimensions" in results
    assert 0 <= results["total_score"] <= 50


def test_score_ai_text():
    """测试评分 AI 生成文本"""
    scorer = Scorer()
    
    text = """
    此外，这个项目至关重要。我们需要深入探讨其复杂性。
    这不仅仅是一个项目，而是我们思考方式的革命。
    行业专家认为这将对整个行业产生持久影响。
    """
    results = scorer.score(text)
    
    # AI 文本应该得分较低
    assert results["total_score"] < 40


def test_score_human_text():
    """测试评分人类文本"""
    scorer = Scorer()
    
    text = """
    我真的不知道该怎么看待这件事。
    300 万行代码，在人类大概睡觉的时候生成的。
    开发社区有一半人疯了，另一半人在解释为什么这不算数。
    真相可能在无聊的中间某处。
    """
    results = scorer.score(text)
    
    # 人类文本应该得分较高
    assert results["total_score"] >= 35


def test_score_dimensions():
    """测试评分维度"""
    scorer = Scorer()
    
    text = "测试文本"
    results = scorer.score(text)
    
    assert len(results["dimensions"]) == 5
    
    for dim in results["dimensions"]:
        assert "name" in dim
        assert "score" in dim
        assert "feedback" in dim
        assert 1 <= dim["score"] <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
