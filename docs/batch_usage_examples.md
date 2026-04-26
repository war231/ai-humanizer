# 📦 批量处理命令使用示例

## 基础用法

### 1. 批量检测（默认）

```bash
python -m ai_humanizer.cli batch ./documents/
```

**输出：**
```
正在处理目录: ./documents/
找到 10 个文件

✅ 处理完成！
  总文件数: 10
  处理成功: 10
  平均 AI 模式: 4.5
```

---

### 2. 批量重写

```bash
python -m ai_humanizer.cli batch ./documents/ --rewrite --output ./humanized/
```

**输出：**
```
正在处理目录: ./documents/
找到 10 个文件

✅ 处理完成！
  总文件数: 10
  处理成功: 10
  重写文件: 7
  平均 AI 模式: 4.5
  平均评分: 42.3/50
```

**生成的文件：**
```
./humanized/
├── file1.txt
├── file2.txt
└── ...
```

---

### 3. 批量评分

```bash
python -m ai_humanizer.cli batch ./documents/ --score
```

**输出：**
```
正在处理目录: ./documents/
找到 10 个文件

✅ 处理完成！
  总文件数: 10
  处理成功: 10
  平均 AI 模式: 4.5
  平均评分: 38.2/50
```

---

### 4. 完整处理（检测 + 重写 + 评分）

```bash
python -m ai_humanizer.cli batch ./documents/ --rewrite --score --output ./results/
```

**输出：**
```
正在处理目录: ./documents/
找到 10 个文件

✅ 处理完成！
  总文件数: 10
  处理成功: 10
  重写文件: 7
  平均 AI 模式: 4.5
  平均评分: 42.3/50
```

---

## 高级用法

### 5. 生成 JSON 报告

```bash
python -m ai_humanizer.cli batch ./documents/ --full --report report.json
```

**生成的 report.json：**
```json
{
  "summary": {
    "total_files": 10,
    "processed_files": 10,
    "rewritten_files": 7,
    "average_patterns": 4.5,
    "average_score": 42.3
  },
  "files": [
    {
      "path": "./documents/file1.txt",
      "success": true,
      "detection": {
        "total_patterns": 5,
        "total_matches": 12,
        "categories": {
          "content": {"count": 2, "patterns": ["AI 词汇", "三段式法则"]},
          "language": {"count": 3, "patterns": ["过度使用"]}
        }
      },
      "rewrite": {
        "rewritten": true,
        "output_path": "./results/file1.txt",
        "score": 45
      },
      "score": {
        "total_score": 45,
        "grade": "优秀",
        "dimensions": [...]
      }
    },
    ...
  ]
}
```

---

### 6. 并行处理（加速）

```bash
# 串行处理（慢）
python -m ai_humanizer.cli batch ./documents/

# 并行处理（快 4 倍）
python -m ai_humanizer.cli batch ./documents/ --parallel --workers 4
```

**性能对比：**
```
串行处理: 100 个文件，耗时 120 秒
并行处理: 100 个文件，耗时 35 秒（提速 3.4 倍）
```

---

### 7. 支持多种文件格式

```bash
# 仅处理 .txt 文件
python -m ai_humanizer.cli batch ./documents/ --format txt

# 仅处理 .md 文件
python -m ai_humanizer.cli batch ./documents/ --format md

# 处理所有文件
python -m ai_humanizer.cli batch ./documents/ --format all
```

---

### 8. 自定义 AI 模式阈值

```bash
# 默认阈值：3（检测到 3 种以上 AI 模式才重写）
python -m ai_humanizer.cli batch ./documents/ --rewrite

# 自定义阈值：5（检测到 5 种以上 AI 模式才重写）
python -m ai_humanizer.cli batch ./documents/ --rewrite --threshold 5

# 阈值：0（所有文件都重写）
python -m ai_humanizer.cli batch ./documents/ --rewrite --threshold 0
```

---

### 9. JSON 格式输出

```bash
python -m ai_humanizer.cli batch ./documents/ --json
```

**输出：**
```json
{
  "summary": {
    "total_files": 10,
    "processed_files": 10,
    "rewritten_files": 0,
    "average_patterns": 4.5,
    "average_score": null
  },
  "files": [...]
}
```

---

## 完整示例

### 示例 1：处理小说章节

```bash
# 批量处理小说章节
python -m ai_humanizer.cli batch ./novels/ \
  --format txt \
  --rewrite \
  --score \
  --output ./humanized/ \
  --report ./reports/novels_report.json \
  --parallel \
  --workers 8
```

**效果：**
- 检测所有章节的 AI 痕迹
- 重写 AI 痕迹较多的章节
- 评估人性化程度
- 保存重写后的章节
- 生成详细报告

---

### 示例 2：处理博客文章

```bash
# 批量处理博客文章
python -m ai_humanizer.cli batch ./blog/ \
  --format md \
  --rewrite \
  --threshold 4 \
  --output ./humanized_blog/ \
  --report ./reports/blog_report.json
```

---

### 示例 3：快速检测

```bash
# 快速检测（不重写）
python -m ai_humanizer.cli batch ./documents/ \
  --parallel \
  --workers 8 \
  --json > detection_results.json
```

---

## 参数详解

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
| `--threshold` | AI 模式阈值 | 3 |
| `--json` | JSON 格式输出 | False |

---

## 性能优化建议

### 1. 使用并行处理

```bash
# 推荐：使用 4-8 个工作进程
python -m ai_humanizer.cli batch ./documents/ --parallel --workers 8
```

### 2. 批量处理大量文件

```bash
# 分批处理（每批 100 个文件）
for i in {1..10}; do
  python -m ai_humanizer.cli batch ./batch_$i/ --parallel --workers 4
done
```

### 3. 使用缓存

```python
# 在代码中使用缓存
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_detect(text_hash):
    return humanizer.detect(text)
```

---

## 常见问题

### Q1: 如何只重写 AI 痕迹较多的文件？

**A:** 使用 `--threshold` 参数：
```bash
python -m ai_humanizer.cli batch ./documents/ --rewrite --threshold 5
```

### Q2: 如何处理子目录中的文件？

**A:** 默认会递归处理所有子目录：
```bash
python -m ai_humanizer.cli batch ./documents/
# 会处理 ./documents/ 及其所有子目录中的文件
```

### Q3: 如何查看详细错误信息？

**A:** 使用 `--json` 输出，错误信息会包含在报告中：
```bash
python -m ai_humanizer.cli batch ./documents/ --json > results.json
# 查看 results.json 中的 "error" 字段
```

### Q4: 如何处理非 UTF-8 编码的文件？

**A:** 目前仅支持 UTF-8，建议先转换编码：
```bash
# 转换编码
iconv -f GBK -t UTF-8 input.txt > output.txt
```

---

## 总结

**增强版批量处理命令功能：**

✅ 支持多种文件格式（txt/md/all）
✅ 支持重写功能
✅ 支持评分功能
✅ 支持输出到文件
✅ 支持 JSON 格式
✅ 支持并行处理
✅ 支持生成报告
✅ 支持自定义阈值
✅ 支持进度显示

**性能提升：**
- 并行处理提速 3-4 倍
- 支持批量处理数千文件
- 内存占用优化

**易用性：**
- 丰富的参数选项
- 清晰的输出格式
- 详细的错误报告
