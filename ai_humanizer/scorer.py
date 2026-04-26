"""
质量评分器

评估文本人性化程度。
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ScoreDimension:
    """评分维度"""
    name: str
    description: str
    score: int
    max_score: int = 10
    feedback: str = ""


class Scorer:
    """质量评分器"""
    
    DIMENSIONS = {
        "directness": {
            "name": "直接性",
            "description": "直接陈述事实还是绕圈宣告？",
            "criteria": {
                10: "直截了当，无铺垫",
                7: "基本直接，有少量铺垫",
                4: "有较多铺垫和修饰",
                1: "充满铺垫和修饰",
            },
        },
        "rhythm": {
            "name": "节奏",
            "description": "句子长度是否变化？",
            "criteria": {
                10: "长短交错，节奏自然",
                7: "有一定变化",
                4: "变化较少",
                1: "机械重复",
            },
        },
        "trust": {
            "name": "信任度",
            "description": "是否尊重读者智慧？",
            "criteria": {
                10: "简洁明了，信任读者",
                7: "基本信任",
                4: "有过度解释",
                1: "过度解释，不信任读者",
            },
        },
        "authenticity": {
            "name": "真实性",
            "description": "听起来像真人说话吗？",
            "criteria": {
                10: "自然流畅，有人味",
                7: "较为自然",
                4: "有些生硬",
                1: "机械生硬",
            },
        },
        "conciseness": {
            "name": "精炼度",
            "description": "还有可删减的内容吗？",
            "criteria": {
                10: "无冗余，精炼",
                7: "基本精炼",
                4: "有冗余",
                1: "大量废话",
            },
        },
    }
    
    def score(self, text: str) -> Dict[str, Any]:
        """
        评估文本人性化程度
        
        Args:
            text: 待评估的文本
            
        Returns:
            评分结果字典
        """
        dimensions = []
        total_score = 0
        
        for dim_id, dim_data in self.DIMENSIONS.items():
            dim_score = self._evaluate_dimension(text, dim_id)
            total_score += dim_score
            
            dimensions.append(
                ScoreDimension(
                    name=dim_data["name"],
                    description=dim_data["description"],
                    score=dim_score,
                    feedback=self._get_feedback(dim_score, dim_data["criteria"]),
                )
            )
        
        # 评级
        if total_score >= 45:
            grade = "优秀"
            comment = "已去除 AI 痕迹"
        elif total_score >= 35:
            grade = "良好"
            comment = "仍有改进空间"
        else:
            grade = "需改进"
            comment = "需要重新修订"
        
        return {
            "total_score": total_score,
            "max_score": 50,
            "grade": grade,
            "comment": comment,
            "dimensions": [
                {
                    "name": d.name,
                    "description": d.description,
                    "score": d.score,
                    "max_score": d.max_score,
                    "feedback": d.feedback,
                }
                for d in dimensions
            ],
        }
    
    def _evaluate_dimension(self, text: str, dimension: str) -> int:
        """
        评估单个维度
        
        这里使用简单的启发式规则，实际应用中可以使用 LLM 进行评估
        """
        # 简单的启发式评分
        score = 7  # 默认中等分数
        
        if dimension == "directness":
            # 检查填充词
            fillers = ["此外", "值得注意的是", "需要指出的是", "总而言之"]
            filler_count = sum(1 for f in fillers if f in text)
            score = max(1, 10 - filler_count * 2)
        
        elif dimension == "rhythm":
            # 检查句子长度变化
            sentences = [s.strip() for s in text.split("。") if s.strip()]
            if len(sentences) < 2:
                score = 5
            else:
                lengths = [len(s) for s in sentences]
                avg_length = sum(lengths) / len(lengths)
                variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
                score = min(10, int(5 + variance / 50))
        
        elif dimension == "trust":
            # 检查过度解释
            explanations = ["也就是说", "换句话说", "这意味着", "这表明"]
            exp_count = sum(1 for e in explanations if e in text)
            score = max(1, 10 - exp_count * 2)
        
        elif dimension == "authenticity":
            # 检查 AI 词汇
            ai_words = ["至关重要", "不可或缺", "充满活力", "深刻体现"]
            ai_count = sum(1 for w in ai_words if w in text)
            score = max(1, 10 - ai_count * 2)
        
        elif dimension == "conciseness":
            # 检查冗余表达
            redundancies = ["进行", "实施", "开展", "作出"]
            red_count = sum(1 for r in redundancies if r in text)
            score = max(1, 10 - red_count)
        
        return score
    
    def _get_feedback(self, score: int, criteria: Dict[int, str]) -> str:
        """获取反馈"""
        for threshold, feedback in sorted(criteria.items(), reverse=True):
            if score >= threshold:
                return feedback
        return criteria[1]
