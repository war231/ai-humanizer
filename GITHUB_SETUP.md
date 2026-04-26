# GitHub 仓库创建指南

## 方法 1：使用 GitHub CLI（推荐）

如果您已安装 GitHub CLI (`gh`)，可以直接运行：

```bash
cd e:\xiangmu\ai-humanizer

# 创建 GitHub 仓库
gh repo create ai-humanizer --public --source=. --remote=origin --push

# 或者创建私有仓库
gh repo create ai-humanizer --private --source=. --remote=origin --push
```

## 方法 2：手动创建并推送

### 步骤 1：在 GitHub 网站创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `ai-humanizer`
   - Description: `AI 文本检测与人性化 Skill - 检测并修复 AI 生成文本的痕迹`
   - 选择 Public 或 Private
   - **不要**勾选 "Add a README file"（我们已经有了）
   - **不要**勾选 "Add .gitignore"（我们已经有了）
   - **不要**选择 License（我们已经有了）

3. 点击 "Create repository"

### 步骤 2：添加远程仓库并推送

创建仓库后，GitHub 会显示推送命令。根据您的用户名，运行：

```bash
cd e:\xiangmu\ai-humanizer

# 添加远程仓库（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-humanizer.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 方法 3：使用 SSH（如果已配置 SSH 密钥）

```bash
cd e:\xiangmu\ai-humanizer

# 添加远程仓库（SSH 方式）
git remote add origin git@github.com:YOUR_USERNAME/ai-humanizer.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 验证推送成功

推送完成后，访问您的仓库页面：
```
https://github.com/YOUR_USERNAME/ai-humanizer
```

应该能看到所有文件，包括：
- `.codebuddy/skills/ai-humanizer.md` - Skill 定义文件
- `README.md` - 项目说明
- `QUICKSTART.md` - 快速使用指南
- 其他文档和代码文件

## 后续操作

### 添加仓库描述和主题

在 GitHub 仓库页面：
1. 点击 ⚙️ Settings
2. 在 "General" 页面添加：
   - Description: `AI 文本检测与人性化 Skill - 检测并修复 AI 生成文本的痕迹`
   - Website: 可以留空或添加文档链接
   - Topics: 添加标签，如 `ai`, `skill`, `claude-code`, `humanizer`, `text-processing`

### 创建 Release

```bash
# 创建标签
git tag -a v1.0.0 -m "Release v1.0.0: Initial release"

# 推送标签
git push origin v1.0.0
```

然后在 GitHub 仓库的 "Releases" 页面创建正式发布。

### 添加徽章到 README

可以在 README.md 顶部添加徽章：

```markdown
[![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/ai-humanizer)](https://github.com/YOUR_USERNAME/ai-humanizer/releases)
[![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/ai-humanizer)](https://github.com/YOUR_USERNAME/ai-humanizer/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/ai-humanizer)](https://github.com/YOUR_USERNAME/ai-humanizer/stargazers)
```

## 需要帮助？

如果您提供 GitHub 用户名，我可以帮您生成完整的推送命令。
