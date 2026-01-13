---
name: blog-publisher
description: Publish local markdown files to GitHub Pages blog (Jekyll). Use this skill when the user wants to publish a local markdown article to their GitHub blog, automatically converting frontmatter to Jekyll format, uploading local images, and pushing to the repository via GitHub API.
license: MIT
---

# GitHub Blog Publisher

一键将本地 Markdown 文件发布到 GitHub Pages 博客（Jekyll 格式）。

## 功能

- 自动解析文件名获取日期和标题
- 转换 Frontmatter 为 Jekyll 格式
- 上传本地图片到 GitHub 仓库
- 通过 GitHub API 推送文章到 `_posts` 目录

## 使用前配置

### 配置方式（推荐）：使用 .env 文件

在技能目录创建 `.env` 文件：

```bash
cd ~/.claude/skills/blog-publisher
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# ===== 必需配置 =====
GITHUB_BLOG_TOKEN=your_github_personal_access_token
GITHUB_BLOG_USER=your_username
GITHUB_BLOG_REPO=your_username.github.io
GITHUB_BLOG_AUTHOR=你的名字

# ===== 可选配置 =====
GITHUB_BLOG_DOMAIN=blog.yourdomain.com  # 自定义域名（可选）
GITHUB_BLOG_LAYOUT=post                 # Jekyll layout
```

> **说明**：`.env` 文件包含敏感信息，已加入 `.gitignore` 不会提交到 GitHub。配置一次，永久有效。

### 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 生成新 Token，勾选 `repo` 权限

### 备选方式：环境变量

如果不想用 `.env` 文件，也可以在 `~/.zshrc` 中设置环境变量（变量名相同）。

## 使用方式

```
我: 帮我把这篇文章发布到我的 GitHub 博客：/path/to/article.md
Claude: [调用技能]
```

## 文件名规范

推荐使用日期前缀命名格式：

```
2026-01-11-AI-编程实践心得.md
drafts/2026-01-11-AI-编程实践心得/article.md
```

- 日期会自动提取作为文章日期
- 标题会从文件名/目录名解析（连字符转为空格）

## Frontmatter 转换

技能会自动将你的文章转换为 Jekyll 格式：

**输入（你的写作格式）：**
```yaml
---
theme: default
category: AI
---
```

**输出（Jekyll 格式）：**
```yaml
---
layout: post
author: 你的名字
tags: daily
categories: blog
title: "AI 编程实践心得"
date: 2026-01-11
---
```

## 图片处理

本地图片会自动上传到 GitHub 仓库的 `images/` 目录：

**转换前：**
```markdown
![](./images/screenshot.png)
```

**转换后：**
```markdown
![](/images/screenshot.png)
```

## 输出结果

发布成功后会返回：

```json
{
  "title": "AI 编程实践心得",
  "date": "2026-01-11",
  "filename": "2026-01-11-ai-bian-cheng-shi-jian-xin-de.md",
  "post_url": "https://blog.gudong.site/2026/01/11/ai-bian-cheng-shi-jian-xin-de.html",
  "github_url": "https://github.com/user/repo/blob/master/_posts/2026-01-11-ai-bian-cheng-shi-jian-xin-de.md"
}
```

**文章 URL 格式**：Jekyll 默认格式 `/:year/:month/:day/:title.html`

## 资源

- **Scripts**: `scripts/publish.py` - 发布脚本
- **References**: `references/config.md` - 配置参考
