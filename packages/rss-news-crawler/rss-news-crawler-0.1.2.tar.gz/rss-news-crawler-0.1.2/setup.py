from setuptools import setup, find_packages
import os

# 读取README.md内容（显式使用UTF-8编码）
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='rss-news-crawler',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'feedparser>=6.0.8',
        'pytz>=2023.3',
    ],
    entry_points={
        'console_scripts': [
            'rss-crawler = rss_news_crawler.crawler:main'
        ]
    },
    # 显式添加元数据
    author='John_MC_Python',
    author_email='b297209694@outlook.com',
    description='RSS新闻爬虫工具，自动抓取并存储RSS源的最新新闻',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/John-is-playing/rss-news-crawler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)