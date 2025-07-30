#!/usr/bin/env python
"""
AsyncFrame 包安装脚本
"""
import sys
from pathlib import Path
from setuptools import setup, find_packages

# 读取 README
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "现代异步Python Web框架，支持FBV和CBV两种编程风格，以及完整的异步ORM系统"

# 读取版本信息
version = "0.1.0"

# 基础依赖
install_requires = [
    "uvicorn>=0.18.0",
    "python-multipart>=0.0.5", 
    "jinja2>=3.1.0",
    "aiofiles>=0.8.0",
    "asyncpg>=0.28.0",
    "aiomysql>=0.1.1",
    "aiosqlite>=0.19.0",
    "databases>=0.7.0",
    "python-dotenv>=0.19.0",
]

# 可选依赖
extras_require = {
    "dev": [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "black>=22.0.0",
        "flake8>=4.0.0",
        "mypy>=0.991",
    ],
    "mysql": [
        "aiomysql>=0.1.1",
    ],
    "postgresql": [
        "asyncpg>=0.28.0",
    ],
    "all": [
        "aiomysql>=0.1.1",
        "asyncpg>=0.28.0",
    ],
}

setup(
    name="asyncframe",
    version=version,
    description="现代异步Python Web框架，支持FBV和CBV两种编程风格，以及完整的异步ORM系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0716gzs",
    author_email="team@asyncframe.org",
    url="https://github.com/0716gzs/asyncframe",
    project_urls={
        "Bug Tracker": "https://github.com/0716gzs/asyncframe/issues",
        "Documentation": "https://github.com/0716gzs/asyncframe/blob/main/README.md",
        "Source Code": "https://github.com/0716gzs/asyncframe",
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "asyncframe=asyncframe.management:main",
            "acf=asyncframe.management:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    keywords="web framework async asyncio orm database",
    license="MIT",
    zip_safe=False,
) 

"""
# 提交所有更改
git add .
git commit -m "Prepare version 0.1.0 release"

# 创建Git标签
git tag -a v0.1.0 -m "Version 0.1.0"
git push origin v0.1.0


# 安装最新构建工具
pip install --upgrade build twine

# 构建分发包
python -m build


# 测试上传到TestPyPI
python -m twine upload --repository testpypi dist/*

# 正式上传到PyPI
python -m twine upload dist/*

pip install asyncframe






使用 GitHub Actions 自动化发布流程，创建 .github/workflows/publish.yml：
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
"""
