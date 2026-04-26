# 📦 批量处理命令详解

## 当前实现

### 命令格式
```bash
python -m ai_humanizer.cli batch ./documents/
```

### 执行流程

```
1. 扫描目录
   ↓
2. 查找所有 .txt 文件
   ↓
3. 逐个文件处理：
   - 读取文件内容
   - 检测 AI 模式
   - 输出结果
   ↓
4. 完成
```

### 具体代码

```python
@main.command()
@click.argument("directory", type=click.Path(exists=True))
def batch(directory: str):
    """批量处理目录中的文件"""
    import os
    from pathlib import Path

    humanizer = Humanizer()
    dir_path = Path(directory)

    console.print(f"[yellow]正在处理目录: {directory}[/yellow]")

    # 遍历所有 .txt 文件
    for file_path in dir_path.glob("**/*.txt"):
        console.print(f"\n[blue]处理文件: {file_path}[/blue]")

        # 读取文件
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 检测 AI 模式
        results = humanizer.detect(text)
        console.print(f"  检测到 {results['total_patterns']} 种 AI 写作模式")
```

### 当前功能

✅ **支持的功能：**
- 扫描目录及子目录
- 查找所有 `.txt` 文件
- 检测 AI 写作模式
- 输出检测结果

❌ **缺失的功能：**
- 不支持其他文件格式（.md, .docx 等）
- 不支持重写功能
- 不支持评分功能
- 不支持输出到文件
- 不支持 JSON 格式输出
- 不支持并行处理

---

## 🚀 增强版批量处理

### 新增功能

- ✅ 支持多种文件格式
- ✅ 支持重写功能
- ✅ 支持评分功能
- ✅ 支持输出到文件
- ✅ 支持 JSON 格式输出
- ✅ 支持并行处理
- ✅ 支持进度显示
- ✅ 支持生成报告

### 使用示例

```bash
# 基础批量检测
python -m ai_humanizer.cli batch ./documents/

# 批量重写（输出到新目录）
python -m ai_humanizer.cli batch ./documents/ --rewrite --output ./humanized/

# 批量评分
python -m ai_humanizer.cli batch ./documents/ --score

# 完整处理（检测 + 重写 + 评分）
python -m ai_humanizer.cli batch ./documents/ --full --output ./results/

# 生成 JSON 报告
python -m ai_humanizer.cli batch ./documents/ --report report.json

# 并行处理（加速）
python -m ai_humanizer.cli batch ./documents/ --parallel --workers 4
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `directory` | 要处理的目录 | 必需 |
| `--format` | 文件格式（txt/md/all） | txt |
| `--rewrite` | 是否重写 | False |
| `--score` | 是否评分 | False |
| `--output` | 输出目录 | None |
| `--report` | 报告文件路径 | None |
| `--parallel` | 是否并行处理 | False |
| `--workers` | 并行工作进程数 | 4 |
| `--threshold` | AI 模式阈值（超过则重写） | 3 |

---

## 📊 执行示例

### 示例 1：基础批量检测

```bash
python -m ai_humanizer.cli batch ./novels/
```

**输出：**
```
正在处理目录: ./novels/

处理文件: ./novels/chapter1.txt
  检测到 5 种 AI 写作模式

处理文件: ./novels/chapter2.txt
  检测到 3 种 AI 写作模式

处理文件: ./novels/chapter3.txt
  检测到 7 种 AI 写作模式

✅ 处理完成！
   总文件数: 3
   平均 AI 模式: 5.0
```

### 示例 2：批量重写

```bash
python -m ai_humanizer.cli batch ./novels/ --rewrite --output ./humanized/
```

**输出：**
```
正在处理目录: ./novels/

处理文件: ./novels/chapter1.txt
  检测到 5 种 AI 写作模式
  正在重写...
  重写完成，评分: 42/50
  保存到: ./humanized/chapter1.txt

处理文件: ./novels/chapter2.txt
  检测到 3 种 AI 写作模式
  AI 模式较少，跳过重写

处理文件: ./novels/chapter3.txt
  检测到 7 种 AI 写作模式
  正在重写...
  重写完成，评分: 45/50
  保存到: ./humanized/chapter3.txt

✅ 处理完成！
   总文件数: 3
   重写文件: 2
   平均评分: 43.5/50
```

### 示例 3：生成报告

```bash
python -m ai_humanizer.cli batch ./novels/ --full --report report.json
```

**生成的 report.json：**
```json
{
  "summary": {
    "total_files": 3,
    "processed_files": 3,
    "rewritten_files": 2,
    "average_score": 43.5,
    "average_patterns": 5.0
  },
  "files": [
    {
      "path": "./novels/chapter1.txt",
      "detection": {
        "total_patterns": 5,
        "patterns": ["AI 词汇", "三段式法则", ...]
      },
      "rewrite": {
        "rewritten": true,
        "output_path": "./humanized/chapter1.txt",
        "score": 42
      }
    },
    ...
  ]
}
```

---

## 🔧 实现细节

### 文件扫描

```python
# 支持多种文件格式
if format == "txt":
    pattern = "**/*.txt"
elif format == "md":
    pattern = "**/*.md"
elif format == "all":
    pattern = "**/*.*"

files = list(dir_path.glob(pattern))
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor

def process_file(file_path):
    # 处理单个文件
    ...

with ThreadPoolExecutor(max_workers=workers) as executor:
    results = list(executor.map(process_file, files))
```

### 进度显示

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("处理中...", total=len(files))

    for file_path in files:
        # 处理文件
        process_file(file_path)
        progress.update(task, advance=1)
```

---

## 📈 性能优化

### 1. 并行处理

```bash
# 串行处理（慢）
python -m ai_humanizer.cli batch ./documents/

# 并行处理（快 4 倍）
python -m ai_humanizer.cli batch ./documents/ --parallel --workers 4
```

### 2. 批量 API 调用

```python
# 批量调用 LLM API（减少网络开销）
texts = [read_file(f) for f in files]
results = humanizer.batch_detect(texts)
```

### 3. 缓存

```python
# 缓存已处理的文件
import hashlib

def get_cache_key(file_path):
    content = read_file(file_path)
    return hashlib.md5(content.encode()).hexdigest()

if cache_key in cache:
    return cache[cache_key]
```

---

## ✅ 总结

### 当前批量处理功能

- ✅ 扫描目录
- ✅ 查找 .txt 文件
- ✅ 检测 AI 模式
- ✅ 输出结果

### 建议增强

- ✅ 支持多种文件格式
- ✅ 支持重写功能
- ✅ 支持评分功能
- ✅ 支持输出到文件
- ✅ 支持 JSON 格式
- ✅ 支持并行处理
- ✅ 支持生成报告

---

**需要我实现增强版的批量处理命令吗？**
