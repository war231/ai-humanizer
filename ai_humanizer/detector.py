"""
AI 写作模式检测器

检测文本中的 24 种 AI 写作模式。
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass

from ai_humanizer.patterns.content import CONTENT_PATTERNS
from ai_humanizer.patterns.language import LANGUAGE_PATTERNS
from ai_humanizer.patterns.style import STYLE_PATTERNS
from ai_humanizer.patterns.communication import COMMUNICATION_PATTERNS


@dataclass
class PatternMatch:
    """模式匹配结果"""
    pattern_id: str
    pattern_name: str
    category: str
    matches: List[str]
    description: str
    suggestion: str


class Detector:
    """AI 写作模式检测器"""
    
    def __init__(self):
        """初始化检测器，加载所有模式"""
        self.patterns = {
            "content": CONTENT_PATTERNS,
            "language": LANGUAGE_PATTERNS,
            "style": STYLE_PATTERNS,
            "communication": COMMUNICATION_PATTERNS,
        }
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        检测文本中的 AI 写作模式
        
        Args:
            text: 待检测的文本
            
        Returns:
            检测结果字典
        """
        results = {
            "total_patterns": 0,
            "total_matches": 0,
            "categories": {},
            "details": [],
        }
        
        for category, patterns in self.patterns.items():
            category_matches = []
            
            for pattern_id, pattern_data in patterns.items():
                matches = self._find_matches(text, pattern_data["regex"])
                
                if matches:
                    match_result = PatternMatch(
                        pattern_id=pattern_id,
                        pattern_name=pattern_data["name"],
                        category=category,
                        matches=matches,
                        description=pattern_data["description"],
                        suggestion=pattern_data["suggestion"],
                    )
                    category_matches.append(match_result)
                    results["details"].append(match_result)
            
            results["categories"][category] = {
                "count": len(category_matches),
                "patterns": [m.pattern_name for m in category_matches],
            }
            results["total_patterns"] += len(category_matches)
        
        # 统计总匹配数
        results["total_matches"] = sum(
            len(m.matches) for m in results["details"]
        )
        
        return results
    
    def _find_matches(self, text: str, pattern: str) -> List[str]:
        """
        在文本中查找模式匹配
        
        Args:
            text: 待搜索的文本
            pattern: 正则表达式模式
            
        Returns:
            匹配的字符串列表
        """
        try:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            return list(set(matches)) if matches else []
        except re.error:
            return []
    
    def get_pattern_summary(self, text: str) -> str:
        """
        获取模式检测摘要
        
        Args:
            text: 待检测的文本
            
        Returns:
            摘要字符串
        """
        results = self.detect(text)
        
        summary_lines = [
            f"检测到 {results['total_patterns']} 种 AI 写作模式",
            f"总计 {results['total_matches']} 处匹配",
            "",
        ]
        
        for category, data in results["categories"].items():
            if data["count"] > 0:
                summary_lines.append(f"【{category.upper()}】{data['count']} 种模式:")
                for pattern in data["patterns"]:
                    summary_lines.append(f"  - {pattern}")
        
        return "\n".join(summary_lines)
