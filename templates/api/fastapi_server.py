"""
AI Humanizer - FastAPI 服务器模板

提供 REST API 接口，供任何 Agent 调用
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from ai_humanizer import Humanizer

app = FastAPI(
    title="AI Humanizer API",
    description="AI 文本检测与人性化 API",
    version="1.0.0"
)

# 初始化 Humanizer
humanizer = Humanizer()


class DetectRequest(BaseModel):
    """检测请求"""
    text: str


class RewriteRequest(BaseModel):
    """重写请求"""
    text: str
    tone: Optional[str] = "neutral"


class ScoreRequest(BaseModel):
    """评分请求"""
    text: str


@app.post("/detect")
async def detect(request: DetectRequest):
    """
    检测文本中的 AI 写作模式

    Args:
        request: 检测请求

    Returns:
        检测结果
    """
    try:
        result = humanizer.detect(request.text)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rewrite")
async def rewrite(request: RewriteRequest):
    """
    人性化重写文本

    Args:
        request: 重写请求

    Returns:
        重写后的文本
    """
    try:
        humanized = humanizer.rewrite(request.text, tone=request.tone)
        score = humanizer.score(humanized)
        return {
            "success": True,
            "original": request.text,
            "humanized": humanized,
            "score": score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/score")
async def score(request: ScoreRequest):
    """
    评估文本人性化程度

    Args:
        request: 评分请求

    Returns:
        评分结果
    """
    try:
        result = humanizer.score(request.text)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


# 使用示例
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 客户端调用示例
"""
import requests

# 检测
response = requests.post(
    "http://localhost:8000/detect",
    json={"text": "此外，这个项目至关重要。"}
)
print(response.json())

# 重写
response = requests.post(
    "http://localhost:8000/rewrite",
    json={"text": "此外，这个项目至关重要。", "tone": "neutral"}
)
print(response.json())

# 评分
response = requests.post(
    "http://localhost:8000/score",
    json={"text": "软件更新添加了批处理功能。"}
)
print(response.json())
"""
