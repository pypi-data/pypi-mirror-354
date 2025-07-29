from setuptools import setup, find_packages

setup(
    name='rss_news_crawler',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'feedparser',
        'pytz',
    ],
    entry_points={
        'console_scripts': [
            'rss-news-crawler = rss_news_crawler.crawler:main',
        ],
    },
)