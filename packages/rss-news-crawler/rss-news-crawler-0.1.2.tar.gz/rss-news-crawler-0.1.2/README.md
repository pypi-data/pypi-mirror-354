# RSS新闻爬虫工具

## 概述
这是一个自动抓取RSS新闻源并存储到SQLite数据库的工具，支持：
- 多RSS源并行抓取
- 内容去重和压缩存储
- 当日新闻过滤
- 日志记录

## 安装
```
pip install rss-news-crawler``` 

## 使用方法
```
from rss_news_crawler import NewsCrawler
# 创建爬虫对象
crawler = NewsCrawler(
    db_name='news.db',  # SQLite数据库路径
    log_file='news.log',  # 日志文件路径
    rss_feeds_file='rss_feeds.txt',  # RSS源文件路径，在RSS文件不存在或为空时将使用默认RSS源
)
# 爬取RSS源
crawler.fetch_and_store_news()```

## rss_feeds.txt文件格式
每行一个RSS源的URL，例如：
```
https://www.example.com/rss.xml
https://www.example.com/rss2.xml
```
## 数据库表结构
```CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    publish_time DATETIME NOT NULL,
    crawl_time DATETIME NOT NULL,
    title TEXT NOT NULL,
    content BLOB NOT NULL,
    url TEXT NOT NULL UNIQUE
)
```

Content字段存储的是经过压缩和去重的新闻内容，使用feed_handler.compress_content()进行压缩
## 示例
```
from rss_news_crawler import NewsCrawler

crawler = NewsCrawler(
    db_name='news.db',
    log_file='news.log',
    rss_feeds_file='rss_feeds.txt',
)

crawler.fetch_and_store_news()
```