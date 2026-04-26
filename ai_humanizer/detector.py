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
from ai_humanizer.patterns.webnovel import WEBNOVEL_PATTERNS


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
            "webnovel": WEBNOVEL_PATTERNS,
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
        
        # 添加基于代码逻辑的检测（不依赖正则）
        self._detect_advanced_patterns(text, results)
        
        return results
    
    def _detect_advanced_patterns(self, text: str, results: Dict[str, Any]) -> None:
        """
        检测需要代码逻辑分析的高级 AI 模式
        """
        # 1. 句长均匀度检测
        sentences = [s.strip() for s in re.split(r"[。！？\n]", text) if s.strip()]
        if len(sentences) >= 5:
            lengths = [len(s) for s in sentences]
            import statistics
            try:
                std_dev = statistics.stdev(lengths)
                avg_len = statistics.mean(lengths)
                # 变异系数 = 标准差 / 平均值，反映相对离散程度
                cv = std_dev / avg_len if avg_len > 0 else 0
                # CV < 0.3 说明句子长度过于均匀（AI 特征）
                if cv < 0.3:
                    uniform_sentences = [s for s in sentences if abs(len(s) - avg_len) / avg_len < 0.2]
                    match_result = PatternMatch(
                        pattern_id="sentence_length_uniform",
                        pattern_name="句长过于均匀",
                        category="webnovel",
                        matches=uniform_sentences[:5],  # 最多展示5个示例
                        description="AI 生成的句子长度过于均匀，节奏单调乏味",
                        suggestion="刻意制造长短句的剧烈变化，用短句表达紧张，用长句描写",
                    )
                    results["details"].append(match_result)
                    results["categories"]["webnovel"]["count"] += 1
                    results["categories"]["webnovel"]["patterns"].append("句长过于均匀")
                    results["total_patterns"] += 1
                    results["total_matches"] += len(uniform_sentences)
            except statistics.StatisticsError:
                pass
        
        # 2. 感官描写单调检测
        sensory_words = {
            "visual": ["看", "见", "望", "瞧", "视", "盯", "瞥", "观", "见", "见", "见", "如", "似", "像", "仿佛"],
            "auditory": ["听", "闻", "响", "鸣", "叫", "喊", "吼", "泣", "啼", "嗡", "哗", "噼", "啪"],
            "tactile": ["摸", "触", "碰", "撞", "疼", "痛", "痒", "麻", "暖", "热", "冷", "凉", "烫", "冰"],
            "olfactory": ["闻", "嗅", "香", "臭", "腥", "臊", "馊", "霉", "潮", "味", "气", "芬芳", "恶臭"],
            "gustatory": ["尝", "吃", "喝", "品", "舔", "甜", "酸", "苦", "辣", "咸", "涩", "甘", "醇"],
        }
        
        sensory_counts = {sense: 0 for sense in sensory_words}
        for sense, words in sensory_words.items():
            for word in words:
                sensory_counts[sense] += text.count(word)
        
        total_sensory = sum(sensory_counts.values())
        if total_sensory >= 5:  # 有足够的感官描写才检测
            visual_ratio = sensory_counts["visual"] / total_sensory
            # 如果视觉占比超过 75%，说明感官单调
            if visual_ratio > 0.75:
                # 找出具体的视觉描写例子
                visual_examples = []
                for word in sensory_words["visual"]:
                    if word in text and len(visual_examples) < 5:
                        # 提取包含该词的一句
                        idx = text.find(word)
                        start = max(0, idx - 15)
                        end = min(len(text), idx + 15)
                        visual_examples.append(text[start:end])
                
                match_result = PatternMatch(
                    pattern_id="sensory_monotony",
                    pattern_name="感官描写单调",
                    category="webnovel",
                    matches=visual_examples,
                    description="AI 过度依赖视觉描写，缺少听觉、嗅觉、触觉、味觉",
                    suggestion="调动五感：听觉（声音）、嗅觉（气味）、触觉（温度/质感）、味觉",
                )
                results["details"].append(match_result)
                results["categories"]["webnovel"]["count"] += 1
                results["categories"]["webnovel"]["patterns"].append("感官描写单调")
                results["total_patterns"] += 1
                results["total_matches"] += len(visual_examples)
        
        # 3. 情绪单一检测
        emotion_words = {
            "positive": ["喜", "乐", "笑", "欢", "悦", "兴奋", "激动", "高兴", "开心", "狂喜", "振奋"],
            "negative": ["怒", "恨", "悲", "哀", "愤", "仇", "怨", "悔", "绝望", "痛苦", "悲伤", "愤怒"],
            "fear": ["怕", "惧", "恐", "惊", "慌", "吓", "畏", "颤", "发抖", "哆嗦", "心悸", "胆寒"],
            "calm": ["静", "平", "淡", "宁", "安", "稳", "定", "从容", "镇定", "冷静", "平和"],
        }
        
        emotion_counts = {emotion: 0 for emotion in emotion_words}
        for emotion, words in emotion_words.items():
            for word in words:
                emotion_counts[emotion] += text.count(word)
        
        total_emotion = sum(emotion_counts.values())
        if total_emotion >= 3:  # 有足够的情绪描写才检测
            max_emotion = max(emotion_counts.values())
            # 如果某种情绪占比超过 80%，说明情绪单一
            if max_emotion / total_emotion > 0.8:
                dominant_emotion = max(emotion_counts, key=emotion_counts.get)
                match_result = PatternMatch(
                    pattern_id="emotional_simplicity",
                    pattern_name="情绪描写单一",
                    category="webnovel",
                    matches=[f"主导情绪: {dominant_emotion} ({max_emotion}次)"],
                    description="AI 的情绪描写过于单一，缺少复杂性和矛盾感",
                    suggestion="展现情绪的复杂性：屈辱中夹杂不甘，兴奋中带着恐惧",
                )
                results["details"].append(match_result)
                results["categories"]["webnovel"]["count"] += 1
                results["categories"]["webnovel"]["patterns"].append("情绪描写单一")
                results["total_patterns"] += 1
                results["total_matches"] += 1
    
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
