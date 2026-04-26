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
@click.option("--format", type=click.Choice(["json", "text"]), default="text", help="输出格式")
def detect(file: str, format: str):
    """检测文件中的 AI 写作模式"""
    import json
    
    humanizer = Humanizer()
    
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    results = humanizer.detect(text)
    
    if format == "json":
        # JSON 格式输出（适合 OpenClaw 和其他 Agent）
        output = {
            "success": True,
            "total_patterns": results["total_patterns"],
            "total_matches": results["total_matches"],
            "categories": results["categories"],
            "details": [
                {
                    "pattern_id": d.pattern_id,
                    "pattern_name": d.pattern_name,
                    "category": d.category,
                    "matches": d.matches,
                    "suggestion": d.suggestion
                }
                for d in results["details"]
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出（适合人类阅读）
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
@click.option("--format", type=click.Choice(["json", "text"]), default="text", help="输出格式")
def score(file: str, format: str):
    """评估文本人性化程度"""
    import json
    
    humanizer = Humanizer()
    
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    
    results = humanizer.score(text)
    
    if format == "json":
        # JSON 格式输出（适合 OpenClaw 和其他 Agent）
        output = {
            "success": True,
            "total_score": results["total_score"],
            "max_score": results["max_score"],
            "grade": results["grade"],
            "comment": results["comment"],
            "dimensions": results["dimensions"]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出（适合人类阅读）
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
@click.option("--format", type=click.Choice(["txt", "md", "all"]), default="txt", help="文件格式")
@click.option("--rewrite", is_flag=True, help="是否重写")
@click.option("--score", is_flag=True, help="是否评分")
@click.option("--output", type=click.Path(), help="输出目录")
@click.option("--report", type=click.Path(), help="报告文件路径")
@click.option("--parallel", is_flag=True, help="是否并行处理")
@click.option("--workers", type=int, default=4, help="并行工作进程数")
@click.option("--threshold", type=int, default=3, help="AI 模式阈值")
@click.option("--json", "json_output", is_flag=True, help="JSON 格式输出")
def batch(directory: str, format: str, rewrite: bool, score: bool, output: str, 
          report: str, parallel: bool, workers: int, threshold: int, json_output: bool):
    """批量处理目录中的文件"""
    import os
    import json
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    
    humanizer = Humanizer()
    dir_path = Path(directory)
    
    # 确定文件模式
    if format == "txt":
        patterns = ["**/*.txt"]
    elif format == "md":
        patterns = ["**/*.md"]
    else:
        patterns = ["**/*.txt", "**/*.md"]
    
    # 收集所有文件
    files = []
    for pattern in patterns:
        files.extend(dir_path.glob(pattern))
    
    if not files:
        console.print("[red]未找到匹配的文件[/red]")
        return
    
    console.print(f"[yellow]正在处理目录: {directory}[/yellow]")
    console.print(f"[yellow]找到 {len(files)} 个文件[/yellow]")
    
    # 创建输出目录
    if output:
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # 处理单个文件的函数
    def process_file(file_path: Path) -> dict:
        """处理单个文件"""
        result = {
            "path": str(file_path),
            "success": False,
            "detection": None,
            "rewrite": None,
            "score": None
        }
        
        try:
            # 读取文件
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # 检测 AI 模式
            detection = humanizer.detect(text)
            result["detection"] = {
                "total_patterns": detection["total_patterns"],
                "total_matches": detection["total_matches"],
                "categories": detection["categories"]
            }
            
            # 决定是否重写
            should_rewrite = rewrite and detection["total_patterns"] >= threshold
            
            if should_rewrite:
                # 重写文本
                humanized = humanizer.rewrite(text)
                
                # 评分
                if score:
                    score_result = humanizer.score(humanized)
                    result["score"] = score_result
                
                # 保存到输出目录
                if output:
                    output_file = output_path / file_path.name
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(humanized)
                    
                    result["rewrite"] = {
                        "rewritten": True,
                        "output_path": str(output_file),
                        "score": result["score"]["total_score"] if result["score"] else None
                    }
                else:
                    result["rewrite"] = {
                        "rewritten": True,
                        "humanized": humanized[:200] + "..." if len(humanized) > 200 else humanized,
                        "score": result["score"]["total_score"] if result["score"] else None
                    }
            else:
                # 仅评分（如果不重写但需要评分）
                if score:
                    score_result = humanizer.score(text)
                    result["score"] = score_result
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    # 处理所有文件
    results = []
    
    if parallel:
        # 并行处理
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("处理中...", total=len(files))
            
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(process_file, f): f for f in files}
                
                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)
                    progress.update(task, advance=1)
    else:
        # 串行处理
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("处理中...", total=len(files))
            
            for file_path in files:
                result = process_file(file_path)
                results.append(result)
                progress.update(task, advance=1)
    
    # 生成统计
    successful = [r for r in results if r["success"]]
    rewritten = [r for r in successful if r.get("rewrite") and r["rewrite"].get("rewritten")]
    
    avg_patterns = sum(r["detection"]["total_patterns"] for r in successful) / len(successful) if successful else 0
    avg_score = sum(r["score"]["total_score"] for r in successful if r.get("score")) / len([r for r in successful if r.get("score")]) if any(r.get("score") for r in successful) else 0
    
    summary = {
        "total_files": len(files),
        "processed_files": len(successful),
        "rewritten_files": len(rewritten),
        "average_patterns": round(avg_patterns, 2),
        "average_score": round(avg_score, 2) if avg_score > 0 else None
    }
    
    # 输出结果
    if json_output:
        output_data = {
            "summary": summary,
            "files": results
        }
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        # 显示统计
        console.print("\n[green]✅ 处理完成！[/green]")
        console.print(f"  总文件数: {summary['total_files']}")
        console.print(f"  处理成功: {summary['processed_files']}")
        if summary['rewritten_files'] > 0:
            console.print(f"  重写文件: {summary['rewritten_files']}")
        console.print(f"  平均 AI 模式: {summary['average_patterns']}")
        if summary['average_score']:
            console.print(f"  平均评分: {summary['average_score']}/50")
    
    # 保存报告
    if report:
        report_data = {
            "summary": summary,
            "files": results
        }
        with open(report, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        console.print(f"\n[green]报告已保存: {report}[/green]")


if __name__ == "__main__":
    main()
