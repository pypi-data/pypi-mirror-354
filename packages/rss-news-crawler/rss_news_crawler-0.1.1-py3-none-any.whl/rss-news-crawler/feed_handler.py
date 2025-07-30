import feedparser
from datetime import datetime
import pytz
import zlib
import re
from .utils import clean_text, similarity

class FeedHandler:
    def __init__(self, rss_feeds_file):
        self.rss_feeds_file = rss_feeds_file
    
    def get_rss_feeds(self):
        rss_feeds = []
        try:
            with open(self.rss_feeds_file, "r", encoding="utf-8") as f:
                for url in f.readlines():
                    url = url.strip()
                    if url:
                        rss_feeds.append(url)
                if not rss_feeds:
                    raise FileNotFoundError("No valid RSS feeds found")
        except FileNotFoundError as e:
            print(f"RSS feed file not found or empty, using default RSS feed. Error: {e}")
            rss_feeds = ["https://www.chinanews.com.cn/rss/scroll-news.xml"]
        except Exception as e:
            print(f"Unknown error: {e}")
            rss_feeds = ["https://www.chinanews.com.cn/rss/scroll-news.xml"]
        return rss_feeds
    
    def parse_feed(self, feed_url):
        return feedparser.parse(feed_url)
    
    def parse_publish_time(self, entry):
        time_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        for field in time_fields:
            if hasattr(entry, field) and getattr(entry, field):
                return datetime(*getattr(entry, field)[:6]).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        return datetime.now(pytz.timezone("Asia/Shanghai"))
    
    def get_current_east8_time(self):
        return datetime.now(pytz.timezone("Asia/Shanghai"))
    
    def get_today_start_time(self):
        now = self.get_current_east8_time()
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def compress_content(self, content):
        # 确保 content 是字节类型
        if isinstance(content, str):
            return zlib.compress(content.encode('utf-8'))
        return zlib.compress(content)
    
    def decompress_content(self, compressed_content):
        decompressed_bytes = zlib.decompress(compressed_content)
        return decompressed_bytes.decode('utf-8')