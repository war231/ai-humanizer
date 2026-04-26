"""
AI Humanizer - LangChain Tool 模板

将 AI Humanizer 集成为 LangChain Tool
"""

from langchain.tools import Tool
from ai_humanizer import Humanizer
from typing import Optional


def create_humanizer_tools(model: str = "gpt-4"):
    """
    创建 AI Humanizer LangChain Tools

    Args:
        model: 使用的 LLM 模型

    Returns:
        LangChain Tool 列表
    """
    humanizer = Humanizer(model=model)

    tools = [
        Tool(
            name="ai_humanizer_detect",
            func=lambda text: str(humanizer.detect(text)),
            description="检测文本中的 AI 写作模式。输入文本，返回检测结果（JSON 格式）。"
        ),
        Tool(
            name="ai_humanizer_rewrite",
            func=lambda text: humanizer.rewrite(text),
            description="人性化重写文本。输入文本，返回重写后的文本。"
        ),
        Tool(
            name="ai_humanizer_score",
            func=lambda text: str(humanizer.score(text)),
            description="评估文本人性化程度。输入文本，返回评分结果（JSON 格式）。"
        )
    ]

    return tools


# 使用示例
if __name__ == "__main__":
    from langchain.agents import initialize_agent
    from langchain.llms import OpenAI

    # 创建 Tools
    tools = create_humanizer_tools()

    # 初始化 Agent
    llm = OpenAI(temperature=0)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

    # 使用 Agent
    result = agent.run("请检测这段文本中的 AI 痕迹：此外，这个项目至关重要。")
    print(result)
