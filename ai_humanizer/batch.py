"""
批量章节处理模块

支持批量处理网文章节，保持人物设定一致性。
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from ai_humanizer.detector import Detector
from ai_humanizer.rewriter import Rewriter


@dataclass
class Chapter:
    """章节数据"""
    index: int
    title: str
    content: str
    characters: List[str] = None
    key_info: Dict[str, Any] = None


class BatchProcessor:
    """批量章节处理器"""
    
    def __init__(self, model: str = "gpt-4"):
        """
        初始化批量处理器
        
        Args:
            model: 使用的 LLM 模型
        """
        self.detector = Detector()
        self.rewriter = Rewriter(model=model)
        self.chapters: List[Chapter] = []
        self.global_context: Dict[str, Any] = {
            "characters": {},  # 人物设定
            "worldbuilding": {},  # 世界观
            "plot_threads": [],  # 剧情线
        }
    
    def load_chapters(self, directory: str) -> int:
        """
        从目录加载章节文件
        
        Args:
            directory: 章节文件目录
            
        Returns:
            加载的章节数量
        """
        dir_path = Path(directory)
        chapter_files = sorted(dir_path.glob("*.txt"))
        
        for idx, file_path in enumerate(chapter_files, start=1):
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n", 1)
            title = lines[0] if lines else file_path.stem
            body = lines[1] if len(lines) > 1 else content
            
            self.chapters.append(Chapter(
                index=idx,
                title=title.strip(),
                content=body.strip()
            ))
        
        return len(self.chapters)
    
    def add_chapter(self, title: str, content: str) -> None:
        """
        添加单个章节
        
        Args:
            title: 章节标题
            content: 章节内容
        """
        self.chapters.append(Chapter(
            index=len(self.chapters) + 1,
            title=title,
            content=content
        ))
    
    def extract_key_info(self, chapter: Chapter) -> Dict[str, Any]:
        """
        提取章节关键信息
        
        Args:
            chapter: 章节对象
            
        Returns:
            关键信息字典
        """
        # 简单的关键信息提取（实际应用中可使用 NER 或 LLM）
        key_info = {
            "characters": [],  # 出场人物
            "locations": [],  # 地点
            "items": [],  # 物品/道具
            "events": [],  # 关键事件
            "cultivation": [],  # 修炼相关
            "system_prompts": [],  # 系统提示
        }
        
        # 提取系统提示语（如【叮！】）
        import re
        system_matches = re.findall(r"【.*?】", chapter.content)
        key_info["system_prompts"] = system_matches
        
        # 提取数值（如等级、属性）
        number_matches = re.findall(r"\d+级|\d+点|\d+阶", chapter.content)
        key_info["cultivation"] = number_matches
        
        return key_info
    
    def process_chapter(
        self,
        chapter: Chapter,
        tone: str = "xuanhuan",
        preserve_context: bool = True
    ) -> str:
        """
        处理单个章节
        
        Args:
            chapter: 章节对象
            tone: 目标语调
            preserve_context: 是否保持上下文一致性
            
        Returns:
            重写后的章节内容
        """
        # 提取关键信息
        key_info = self.extract_key_info(chapter)
        chapter.key_info = key_info
        
        # 检测 AI 模式
        patterns = self.detector.detect(chapter.content)
        
        # 构建上下文提示
        context_prompt = ""
        if preserve_context and self.global_context["characters"]:
            context_prompt = f"""
## 前文人物设定（必须保持一致）

{self._format_characters()}

请确保人物设定与前文保持一致。
"""
        
        # 重写章节
        full_prompt = self._build_chapter_prompt(
            chapter, patterns, tone, context_prompt
        )
        
        try:
            import openai
            
            response = openai.chat.completions.create(
                model=self.rewriter.config.model,
                messages=[
                    {"role": "system", "content": self.rewriter.SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt},
                ],
                temperature=self.rewriter.config.temperature,
                max_tokens=4000,  # 章节较长，增加 token 限制
            )
            
            rewritten = response.choices[0].message.content.strip()
            
            # 更新全局上下文
            if preserve_context:
                self._update_context(chapter, key_info)
            
            return rewritten
            
        except ImportError:
            # 降级处理
            return self.rewriter._fallback_rewrite(chapter.content, patterns)
    
    def _build_chapter_prompt(
        self,
        chapter: Chapter,
        patterns: Dict[str, Any],
        tone: str,
        context_prompt: str
    ) -> str:
        """构建章节重写提示"""
        base_prompt = self.rewriter._build_rewrite_prompt(
            chapter.content, patterns, tone
        )
        
        chapter_info = f"""
## 章节信息

章节标题：{chapter.title}
章节序号：第 {chapter.index} 章

{context_prompt}
"""
        
        return chapter_info + "\n" + base_prompt
    
    def _format_characters(self) -> str:
        """格式化人物设定"""
        lines = []
        for name, info in self.global_context["characters"].items():
            lines.append(f"- {name}: {info}")
        return "\n".join(lines)
    
    def _update_context(
        self,
        chapter: Chapter,
        key_info: Dict[str, Any]
    ) -> None:
        """更新全局上下文"""
        # 更新人物设定（简化版，实际应用中可使用更复杂的逻辑）
        for char in key_info.get("characters", []):
            if char not in self.global_context["characters"]:
                self.global_context["characters"][char] = f"第{chapter.index}章出场"
    
    def process_all(
        self,
        tone: str = "xuanhuan",
        preserve_context: bool = True,
        output_dir: str = None
    ) -> List[str]:
        """
        批量处理所有章节
        
        Args:
            tone: 目标语调
            preserve_context: 是否保持上下文一致性
            output_dir: 输出目录（可选）
            
        Returns:
            重写后的章节列表
        """
        results = []
        
        for chapter in self.chapters:
            rewritten = self.process_chapter(chapter, tone, preserve_context)
            results.append(rewritten)
            
            # 保存到文件
            if output_dir:
                output_path = Path(output_dir) / f"chapter_{chapter.index:04d}.txt"
                output_path.write_text(
                    f"{chapter.title}\n\n{rewritten}",
                    encoding="utf-8"
                )
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取处理统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "total_chapters": len(self.chapters),
            "total_characters": len(self.global_context["characters"]),
            "total_plot_threads": len(self.global_context["plot_threads"]),
            "chapters_info": [
                {
                    "index": ch.index,
                    "title": ch.title,
                    "length": len(ch.content),
                    "key_info": ch.key_info,
                }
                for ch in self.chapters
            ],
        }
