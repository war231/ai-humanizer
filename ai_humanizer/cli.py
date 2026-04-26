"""
命令行接口

提供命令行工具进行 AI 文本检测和人性化重写。
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ai_humanizer import Humanizer


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """AI Humanizer - AI 文本检测与人性化工具"""
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True))
def detect(file: str):
    """检测文件中的 AI 写作模式"""
    humanizer = Humanizer()
    
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    results = humanizer.detect(text)
    
    # 显示结果
    console.print(Panel(
        f"检测到 {results['total_patterns']} 种 AI 写作模式\n"
        f"总计 {results['total_matches']} 处匹配",
        title="检测结果",
        style="bold blue"
    ))
    
    # 显示详细表格
    if results["details"]:
        table = Table(title="检测到的模式")
        table.add_column("类别", style="cyan")
        table.add_column("模式", style="yellow")
        table.add_column("匹配数", justify="right")
        table.add_column("建议", style="green")
        
        for detail in results["details"]:
            table.add_row(
                detail.category,
                detail.pattern_name,
                str(len(detail.matches)),
                detail.suggestion[:30] + "..."
            )
        
        console.print(table)


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="输出文件路径")
@click.option("-t", "--tone", type=click.Choice(["neutral", "formal", "casual", "technical"]), default="neutral", help="目标语调")
def rewrite(file: str, output: str, tone: str):
    """人性化重写文件"""
    humanizer = Humanizer()
    
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    console.print("[yellow]正在重写...[/yellow]")
    humanized = humanizer.rewrite(text, tone=tone)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(humanized)
        console.print(f"[green]重写完成，已保存到 {output}[/green]")
    else:
        console.print(Panel(humanized, title="重写结果", style="green"))


@main.command()
@click.argument("file", type=click.Path(exists=True))
def score(file: str):
    """评估文本人性化程度"""
    humanizer = Humanizer()
    
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    results = humanizer.score(text)
    
    # 显示总分
    console.print(Panel(
        f"总分: {results['total_score']}/{results['max_score']}\n"
        f"评级: {results['grade']}\n"
        f"评价: {results['comment']}",
        title="质量评分",
        style="bold magenta"
    ))
    
    # 显示各维度得分
    table = Table(title="各维度评分")
    table.add_column("维度", style="cyan")
    table.add_column("得分", justify="right")
    table.add_column("反馈", style="green")
    
    for dim in results["dimensions"]:
        table.add_row(
            dim["name"],
            f"{dim['score']}/{dim['max_score']}",
            dim["feedback"]
        )
    
    console.print(table)


@main.command()
@click.argument("directory", type=click.Path(exists=True))
def batch(directory: str):
    """批量处理目录中的文件"""
    import os
    from pathlib import Path
    
    humanizer = Humanizer()
    dir_path = Path(directory)
    
    console.print(f"[yellow]正在处理目录: {directory}[/yellow]")
    
    for file_path in dir_path.glob("**/*.txt"):
        console.print(f"\n[blue]处理文件: {file_path}[/blue]")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        results = humanizer.detect(text)
        console.print(f"  检测到 {results['total_patterns']} 种 AI 写作模式")


if __name__ == "__main__":
    main()
