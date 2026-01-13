# 配置参考

## 配置方式（推荐）：使用 .env 文件

在技能目录创建 `.env` 文件：

```bash
cd ~/.claude/skills/blog-publisher
cp .env.example .env
```

## 配置项说明

### 必需配置（必须设置）

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `GITHUB_BLOG_TOKEN` | GitHub Personal Access Token | `ghp_xxxxxxxx` |
| `GITHUB_BLOG_USER` | GitHub 用户名 | `maoruibin` |
| `GITHUB_BLOG_REPO` | 博客仓库名 | `maoruibin.github.io` |
| `GITHUB_BLOG_AUTHOR` | 文章作者名 | `咕咚` |

### 可选配置（有默认值）

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `GITHUB_BLOG_BRANCH` | `master` | 目标分支（也可能是 `main`） |
| `GITHUB_BLOG_POSTS_DIR` | `_posts` | 文章存放目录 |
| `GITHUB_BLOG_IMAGES_DIR` | `images` | 图片存放目录 |
| `GITHUB_BLOG_LAYOUT` | `post` | Jekyll 布局模板 |
| `GITHUB_BLOG_DEFAULT_CATEGORY` | `blog` | 文章分类 |
| `GITHUB_BLOG_DEFAULT_TAGS` | `daily` | 文章标签 |
| `GITHUB_BLOG_DOMAIN` | 无 | 自定义域名，如 `blog.gudong.site` |

## 自定义域名说明

如果你使用了自定义域名（如 blog.gudong.site），需要设置 `GITHUB_BLOG_DOMAIN`：

```bash
GITHUB_BLOG_DOMAIN=blog.gudong.site
```

这样生成的文章链接就是：
```
https://blog.gudong.site/2026/01/11/your-title.html
```

如果不设置，则使用仓库名生成链接：
```
https://username.github.io/2026/01/11/your-title.html
```

## 获取 GitHub Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选权限：
   - ✅ repo (Full control of private repositories)
4. 点击 "Generate token"
5. 复制 token（只显示一次！）

## 备选方式：环境变量

如果不想用 `.env` 文件，也可以在 `~/.zshrc` 中设置环境变量：

```bash
cat >> ~/.zshrc << 'EOF'

# GitHub Blog Publisher
export GITHUB_BLOG_TOKEN="your_token"
export GITHUB_BLOG_USER="your_username"
export GITHUB_BLOG_REPO="your_repo"
export GITHUB_BLOG_AUTHOR="你的名字"
EOF

source ~/.zshrc
```

变量名与 `.env` 文件完全相同。
