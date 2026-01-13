# blog-publisher

> 一键将本地 Markdown 文件发布到 GitHub Pages 博客（Jekyll）

---

## 使用方式

在 Claude Code 中，只需一句话：

```
发布博客 /path/to/article.md
```

**示例：**

```
发布博客 /Users/gudong/write/drafts/2026-01-11-我的文章/article.md
```

就这么简单，文章会自动发布到你的 GitHub 博客。

---

## 安装

### 1. 安装技能

```bash
git clone https://github.com/maoruibin/blog-publisher.git
cp -r blog-publisher ~/.claude/skills/
```

### 2. 配置

**复制配置模板：**

```bash
cd ~/.claude/skills/blog-publisher
cp .env.example .env
```

**编辑 .env 文件，填写你的信息：**

```bash
# ===== 必需配置 =====
GITHUB_BLOG_TOKEN=your_github_personal_access_token
GITHUB_BLOG_USER=your_username
GITHUB_BLOG_REPO=your_username.github.io
GITHUB_BLOG_AUTHOR=你的名字
```

> **说明**：`.env` 文件包含敏感信息，已加入 `.gitignore` 不会提交到 GitHub。配置一次，永久有效。

### 3. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 复制生成的 Token，填入 `.env` 文件

---

## 文件名规范

推荐使用日期前缀命名：

```
2026-01-11-文章标题.md
drafts/2026-01-11-文章标题/article.md  ← 也支持
```

- 日期会自动提取作为文章日期
- 标题会从文件名/目录名解析

---

## 功能特性

- 📝 **智能解析** - 自动从文件名提取标题和日期
- 🔄 **格式转换** - 自动转换 Frontmatter 为 Jekyll 格式
- 🖼️ **图片处理** - 自动上传本地图片到 GitHub 仓库
- 🚀 **一键发布** - 通过 GitHub API 直接推送，无需 Git 操作

---

## Frontmatter 转换

**你的写作格式：**
```yaml
---
theme: default
category: AI
---
```

**自动转换为 Jekyll 格式：**
```yaml
---
layout: post
author: 你的名字
tags: daily
categories: blog
title: "文章标题"
date: 2026-01-11
---
```

---

## 图片处理

本地图片会自动上传到 GitHub 仓库：

**转换前：** `![](./images/screenshot.png)`

**转换后：** `![](/images/screenshot.png)`

已上传的图片（如 S3 URL）不会被处理。

---

## 可选配置

`.env` 文件中的可选配置（有默认值，可不填）：

```bash
GITHUB_BLOG_BRANCH=master             # 默认: master
GITHUB_BLOG_POSTS_DIR=_posts          # 默认: _posts
GITHUB_BLOG_IMAGES_DIR=images         # 默认: images
GITHUB_BLOG_LAYOUT=post               # 默认: post
GITHUB_BLOG_DEFAULT_CATEGORY=blog     # 默认: blog
GITHUB_BLOG_DEFAULT_TAGS=daily        # 默认: daily
GITHUB_BLOG_DOMAIN=blog.gudong.site   # 自定义域名（重要！）
```

**自定义域名说明**：

如果你使用自定义域名（如 `blog.gudong.site`），必须设置 `GITHUB_BLOG_DOMAIN`，否则生成的文章链接不正确。

设置后文章链接格式：
```
https://blog.gudong.site/2026/01/11/your-title.html
```

---

## 直接使用脚本

不通过 Claude Code，直接运行：

```bash
python3 scripts/publish.py /path/to/article.md
```

---

## 项目结构

```
blog-publisher/
├── .env.example          # 配置模板（提交到 GitHub）
├── .gitignore            # 忽略 .env 文件
├── SKILL.md              # Claude Code 技能定义
├── scripts/
│   └── publish.py        # 发布脚本
├── references/
│   └── config.md         # 配置参考
├── README.md             # 本文件
└── LICENSE               # MIT 许可证
```

---

## 作者

**咕咚** - [GitHub](https://github.com/maoruibin)

- inBox 笔记作者
- 独立开发者
- AI 编程实践者

---

## 许可证

[MIT](LICENSE)

---

<p align="center">
  <b>如果这个项目对你有帮助，请给个 ⭐️</b>
</p>
