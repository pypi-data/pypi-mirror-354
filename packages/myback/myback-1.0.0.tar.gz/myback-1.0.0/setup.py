#!/usr/bin/env python3
"""
myback - 交互式反馈收集工具
一个基于MCP协议的图形化反馈收集工具，支持文字和图片反馈
"""

from setuptools import setup, find_packages
import os

# 读取版本信息
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'myback', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return "1.0.0"

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "myback - 交互式反馈收集工具"

# 读取requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'mcp>=1.0.0',
        'pillow>=9.0.0',
        'pywin32>=300;platform_system=="Windows"',
    ]

setup(
    name="myback",
    version=get_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="交互式反馈收集工具 - 支持文字和图片反馈的MCP工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myback",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'myback=myback.main:main',
            'myback-server=myback.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'myback': ['*.md', '*.txt'],
    },
    keywords="feedback, mcp, gui, tkinter, image, text, interactive",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/myback/issues",
        "Source": "https://github.com/yourusername/myback",
        "Documentation": "https://github.com/yourusername/myback#readme",
    },
)
