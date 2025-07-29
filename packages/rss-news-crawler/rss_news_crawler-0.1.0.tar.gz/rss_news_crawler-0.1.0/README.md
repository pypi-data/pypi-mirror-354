# RSS News Crawler

A news crawler tool to fetch and store news from RSS feeds.

## Features

- Fetch news from multiple RSS feeds
- Store news in a SQLite database
- Log activities to a file
- Filter and store only today's news
- Check for duplicate news

## Installation
```pip install rss-news-crawler```

## Usage
```
from rss_news_crawler import NewsCrawler

news = NewsCrawler()
```

## Params
NewsCrawler:
- db_name: Sqlite3 database path (for news data)      default:news.db
- log_file: Some logs for News crawler                default:news.log
- rss_feeds_file: RSS File path                       default:rss_feeds.txt
If the rss_feeds_file is not exist or is empty, it will use default rss url

## RSS File
Like this:
```
https://rss.example1.com/example
https://rss.example2.com/example
https://rss.example3.com/example
https://rss.example4.com/example
```