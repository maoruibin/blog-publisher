# blog-publisher

> 一键将本地 Markdown 文件发布到 GitHub Pages 博客（Jekyll）

一个为 Claude Code 设计的技能，让你可以用自然语言把文章发布到 GitHub 博客。

---

## ✨ 特性

- 📝 **智能解析** - 自动从文件名提取标题和日期
- 🔄 **格式转换** - 自动转换 Frontmatter 为 Jekyll 格式
- 🖼️ **图片处理** - 自动上传本地图片到 GitHub 仓库
- 🚀 **一键发布** - 通过 GitHub API 直接推送，无需 Git 操作

---

## 📦 安装

### 1. 克隆技能到本地

```bash
git clone https://github.com/maoruibin/blog-publisher.git
cp -r blog-publisher ~/.claude/skills/
```

### 2. 配置环境变量

在 `~/.zshrc` 或 `~/.bash_profile` 中添加：

```bash
# ===== 必需配置 =====
export GITHUB_BLOG_TOKEN="your_github_personal_access_token"
export GITHUB_BLOG_USER="your_username"
export GITHUB_BLOG_REPO="your_username.github.io"
export GITHUB_BLOG_AUTHOR="你的名字"

# ===== 可选配置 =====
export GITHUB_BLOG_BRANCH="master"             # 默认: master
export GITHUB_BLOG_POSTS_DIR="_posts"          # 默认: _posts
export GITHUB_BLOG_IMAGES_DIR="images"         # 默认: images
export GITHUB_BLOG_LAYOUT="post"               # 默认: post
export GITHUB_BLOG_DEFAULT_CATEGORY="blog"     # 默认: blog
export GITHUB_BLOG_DEFAULT_TAGS="daily"        # 默认: daily
```

### 3. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 复制生成的 Token

---

## 🎯 使用方式

在 Claude Code 中：

```
我: 帮我把这篇文章发布到我的 GitHub 博客：drafts/2026-01-11-我的文章/article.md

Claude: [自动调用技能，完成发布]
```

---

## 📁 文件名规范

推荐使用日期前缀命名：

```
2026-01-11-文章标题.md
drafts/2026-01-11-文章标题/article.md  ← 也支持
```

- 日期会自动提取作为文章日期
- 标题会从文件名/目录名解析

---

## 🔄 Frontmatter 转换

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
layout: mypost
author: 咕咚
tags: daily
categories: blog
title: "文章标题"
---
```

---

## 🖼️ 图片处理

本地图片会自动上传到 GitHub 仓库的 `images/` 目录：

**转换前：**
```markdown
![](./images/screenshot.png)
```

**转换后：**
```markdown
![](/images/screenshot.png)
```

已上传的图片（如 S3 URL）不会被处理。

---

## 📂 项目结构

```
blog-publisher/
├── SKILL.md              # Claude Code 技能定义
├── scripts/
│   └── publish.py        # 发布脚本
├── references/
│   └── config.md         # 配置参考
├── README.md             # 本文件
└── LICENSE               # MIT 许可证
```

---

## 🛠️ 直接使用脚本

如果你不想通过 Claude Code，也可以直接运行脚本：

```bash
python3 scripts/publish.py /path/to/article.md
```

---

## 📄 许可证

[MIT](LICENSE) - 欢迎自由使用和修改

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📝 作者

**咕咚** - [GitHub](https://github.com/maoruibin)

- inBox 笔记作者
- 独立开发者
- AI 编程实践者

---

## 📮 反馈

有问题或建议？欢迎：

- [提交 Issue](https://github.com/maoruibin/blog-publisher/issues)
- [关注我的公众号](https://mp.weixin.qq.com/s/l-EZl5MsXh-Y4uTbPAy80Q)

---

<p align="center">
  <b>如果这个项目对你有帮助，请给个 ⭐️</b>
</p>
