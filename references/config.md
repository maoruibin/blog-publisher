# 配置参考

## 环境变量

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

## 快速配置（咕咚专用）

```bash
# 添加到 ~/.zshrc
cat >> ~/.zshrc << 'EOF'

# GitHub Blog Publisher
export GITHUB_BLOG_TOKEN="d6b501c3101dc476b74ee86837889099342ce0"
export GITHUB_BLOG_USER="maoruibin"
export GITHUB_BLOG_REPO="maoruibin.github.com"
export GITHUB_BLOG_AUTHOR="咕咚"
export GITHUB_BLOG_LAYOUT="mypost"
EOF

# 重新加载配置
source ~/.zshrc
```

## 获取 GitHub Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选权限：
   - ✅ repo (Full control of private repositories)
4. 点击 "Generate token"
5. 复制 token（只显示一次！）
