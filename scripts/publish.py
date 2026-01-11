#!/usr/bin/env python3
"""
GitHub Blog Publisher

将本地 Markdown 文件发布到 GitHub Pages 博客 (Jekyll)

使用方式:
    python publish.py /path/to/article.md
"""

import os
import re
import sys
import base64
import json
import ssl
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib import request
from urllib.error import HTTPError, URLError

# ==================== 配置（从环境变量读取）====================

def get_config():
    """从环境变量读取配置，关键配置必须设置"""
    config = {
        # 必需配置（因人而异）
        'token': os.getenv('GITHUB_BLOG_TOKEN'),
        'user': os.getenv('GITHUB_BLOG_USER'),
        'repo': os.getenv('GITHUB_BLOG_REPO'),
        'author': os.getenv('GITHUB_BLOG_AUTHOR'),
        # 可选配置（有通用默认值）
        'branch': os.getenv('GITHUB_BLOG_BRANCH', 'master'),
        'posts_dir': os.getenv('GITHUB_BLOG_POSTS_DIR', '_posts'),
        'images_dir': os.getenv('GITHUB_BLOG_IMAGES_DIR', 'images'),
        'layout': os.getenv('GITHUB_BLOG_LAYOUT', 'post'),
        'default_category': os.getenv('GITHUB_BLOG_DEFAULT_CATEGORY', 'blog'),
        'default_tags': os.getenv('GITHUB_BLOG_DEFAULT_TAGS', 'daily'),
    }

    # 验证必需配置
    required = {
        'token': 'GITHUB_BLOG_TOKEN',
        'user': 'GITHUB_BLOG_USER',
        'repo': 'GITHUB_BLOG_REPO',
        'author': 'GITHUB_BLOG_AUTHOR',
    }

    for key, env_var in required.items():
        if not config[key]:
            raise ValueError(f'请设置环境变量 {env_var}')

    return config

# ==================== GitHub API ====================

class GitHubAPI:
    """GitHub API 封装（使用 urllib）"""

    def __init__(self, config):
        self.config = config
        self.base_url = f"https://api.github.com/repos/{config['user']}/{config['repo']}"
        self.token = config['token']

    def _make_request(self, path, method='GET', data=None):
        """发送 GitHub API 请求"""
        # URL 编码路径中的中文等特殊字符
        encoded_path = '/'.join(quote(p, safe='') for p in path.split('/'))
        url = f"{self.base_url}/{encoded_path}"

        headers = {
            'Authorization': f"token {self.token}",
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Blog-Publisher',
        }

        body = None
        if data:
            body = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'

        req = request.Request(url, data=body, headers=headers, method=method)

        # 创建 SSL 上下文（跳过证书验证，仅用于测试）
        ssl_context = ssl._create_unverified_context()

        try:
            with request.urlopen(req, context=ssl_context) as resp:
                if resp.status == 200 or resp.status == 201:
                    return json.loads(resp.read().decode('utf-8'))
                elif resp.status == 404:
                    return None
                else:
                    raise Exception(f"API 请求失败: {resp.status} {resp.read().decode()}")
        except HTTPError as e:
            if e.code == 404:
                return None
            raise Exception(f"API 请求失败: {e.code} {e.read().decode()}")

    def get_file(self, path):
        """获取文件内容（检查是否存在）"""
        return self._make_request(f"contents/{path}?ref={self.config['branch']}")

    def create_or_update_file(self, path, content, message):
        """创建或更新文件"""
        # 先检查文件是否存在
        existing = self.get_file(path)

        data = {
            'message': message,
            'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            'branch': self.config['branch'],
        }

        if existing:
            data['sha'] = existing['sha']

        return self._make_request(f"contents/{path}", method='PUT', data=data)

    def upload_image(self, image_path: Path, image_content: bytes):
        """上传图片到仓库"""
        filename = image_path.name
        target_path = f"{self.config['images_dir']}/{filename}"

        result = self.create_or_update_file(
            target_path,
            image_content,
            f"Upload image: {filename}"
        )

        # 返回图片的相对路径（用于 Jekyll）
        return f"/{self.config['images_dir']}/{filename}"

# ==================== Markdown 处理 ====================

def extract_title_and_date_from_path(filepath):
    """从文件路径提取标题和日期

    支持两种格式:
    1. 目录名包含日期和标题: drafts/2026-01-10-付费是一种自律/article.md
    2. 文件名包含日期和标题: drafts/2026-01-10-付费是一种自律.md
    """
    # 先尝试从文件名提取
    filename = filepath.stem
    date_pattern = r'^(\d{4}-\d{2}-\d{2})-(.+)$'
    match = re.match(date_pattern, filename)

    if match:
        date_str = match.group(1)
        title = match.group(2).replace('-', ' ')
        return title, date_str

    # 如果文件名不匹配，尝试从父目录名提取
    parent_dir = filepath.parent.name
    match = re.match(date_pattern, parent_dir)

    if match:
        date_str = match.group(1)
        title = match.group(2).replace('-', ' ')
        return title, date_str

    return None, None

def extract_title_from_content(content):
    """从 Markdown 内容提取标题（第一个 # 标题）"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def extract_date_from_filename(filepath):
    """从文件名提取日期（已弃用，使用 extract_title_and_date_from_path）

    支持格式:
    - 2026-01-11-Title.md → 2026-01-11
    """
    filename = filepath.stem
    date_pattern = r'^(\d{4}-\d{2}-\d{2})'
    match = re.match(date_pattern, filename)

    if match:
        return match.group(1)

    # 如果文件名没有日期，使用今天
    return datetime.now().strftime('%Y-%m-%d')

def parse_existing_frontmatter(content):
    """解析现有的 YAML frontmatter"""
    if not content.startswith('---'):
        return {}, content

    # 找到第二个 ---
    end = content.find('---', 3)
    if end == -1:
        return {}, content

    frontmatter_text = content[3:end].strip()
    body = content[end + 3:].lstrip()

    # 简单解析（假设 key: value 格式）
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, body

def build_jekyll_frontmatter(title, config):
    """构建 Jekyll frontmatter（固定格式）"""
    tags = config['default_tags']
    # 如果 tags 包含逗号，解析为列表
    if ',' in tags:
        tags_list = [t.strip() for t in tags.split(',')]
    else:
        tags_list = [tags]

    frontmatter = f"""---
layout: {config['layout']}
author: {config['author']}
tags: {tags}
categories: {config['default_category']}
title: "{title}"
---"""
    return frontmatter

def find_and_replace_images(content, api, article_dir):
    """查找并替换本地图片链接

    支持的格式:
    - ![](./images/xxx.png)
    - ![](images/xxx.png)
    - ![](./xxx.png)

    不匹配:
    - http:// 或 https:// 开头的 URL
    """
    # 只匹配本地路径（不以 http:// 或 https:// 开头）
    image_pattern = r'!\[([^\]]*)\]\(((?!https?://)(\./)?(images\/)?([^)]+\.(png|jpg|jpeg|gif|webp|svg)))\)'

    def replace_image(match):
        alt_text = match.group(1)
        url_path = match.group(2)  # 完整的 URL 路径
        images_prefix = match.group(3) or ''
        images_dir = match.group(4) or ''
        filename = match.group(5)

        # 构建本地图片路径
        if images_dir:
            relative_path = images_dir + filename
        else:
            relative_path = filename

        local_path = article_dir / relative_path

        # 如果本地文件存在，上传
        if local_path.exists():
            print(f"  上传图片: {filename}")
            try:
                with open(local_path, 'rb') as f:
                    image_content = f.read()
                new_path = api.upload_image(local_path, image_content)
                print(f"  → {new_path}")
                return f'![{alt_text}]({new_path})'
            except Exception as e:
                print(f"  上传失败: {e}")
                # 保留原链接
                return match.group(0)
        else:
            print(f"  本地图片不存在，跳过: {local_path}")
            return match.group(0)

    return re.sub(image_pattern, replace_image, content)

# ==================== 主逻辑 ====================

def publish_article(filepath):
    """发布文章到 GitHub 博客"""

    filepath = Path(filepath).resolve()

    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    print(f"读取文件: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    config = get_config()
    api = GitHubAPI(config)

    # 1. 从路径提取标题和日期
    print("提取文章标题和日期...")
    title, date = extract_title_and_date_from_path(filepath)

    if not title:
        title = extract_title_from_content(content)
    if not title:
        title = filepath.stem

    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    print(f"  标题: {title}")
    print(f"  日期: {date}")

    # 3. 解析现有 frontmatter，获取正文
    print("解析文章内容...")
    existing_fm, body = parse_existing_frontmatter(content)

    # 4. 处理图片
    print("处理本地图片...")
    article_dir = filepath.parent
    body = find_and_replace_images(body, api, article_dir)

    # 5. 构建 Jekyll frontmatter
    print("构建 Jekyll frontmatter...")
    jekyll_fm = build_jekyll_frontmatter(title, config)

    # 6. 组合最终内容
    final_content = f"{jekyll_fm}\n\n{body}"

    # 7. 确定目标文件名
    target_filename = f"{date}-{title}.md"
    # 清理文件名中的特殊字符
    target_filename = re.sub(r'[<>:"|?*]', '', target_filename)
    target_filename = re.sub(r'\s+', '-', target_filename)

    target_path = f"{config['posts_dir']}/{target_filename}"

    # 8. 推送到 GitHub
    print(f"发布到 GitHub: {target_path}")
    result = api.create_or_update_file(
        target_path,
        final_content,
        f"Publish: {title}"
    )

    # 9. 返回结果
    post_url = f"https://{config['repo']}/{date}-{title.replace(' ', '-').lower()}.html"

    print()
    print("=" * 50)
    print("发布成功！")
    print(f"博客文章: {post_url}")
    print(f"GitHub: {result['content']['html_url']}")
    print("=" * 50)

    return {
        'title': title,
        'date': date,
        'filename': target_filename,
        'post_url': post_url,
        'github_url': result['content']['html_url'],
    }

# ==================== 命令行入口 ====================

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方式: python publish.py <markdown-file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        result = publish_article(filepath)
        # 输出 JSON 格式（方便 Claude 解析）
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
