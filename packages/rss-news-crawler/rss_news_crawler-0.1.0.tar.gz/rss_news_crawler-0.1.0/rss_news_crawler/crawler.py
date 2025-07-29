import logging
from .database import DatabaseHandler
from .feed_handler import FeedHandler
from .log_handler import LogHandler
from .utils import clean_text, similarity

class NewsCrawler:
    def __init__(self, db_name='news.db', log_file='news.log', rss_feeds_file='rss_feeds.txt'):
        self.db_handler = DatabaseHandler(db_name)
        self.feed_handler = FeedHandler(rss_feeds_file)
        self.log_handler = LogHandler(log_file)
        self.logger = self.log_handler.get_logger()
    
    def fetch_and_store_news(self):
        self.logger.info("Starting news crawl...")
        
        # 初始化数据库
        self.db_handler.init_db()
        
        # 获取RSS源列表
        rss_feeds = self.feed_handler.get_rss_feeds()
        
        for feed_url in rss_feeds:
            try:
                feed = self.feed_handler.parse_feed(feed_url)
                self.logger.info(f"Processing feed: {feed_url} ({len(feed.entries)} entries)")
                
                for entry in feed.entries:
                    try:
                        title = entry.title
                        content = entry.description if 'description' in entry else title
                        url = entry.link
                        
                        # 获取新闻发布时间
                        publish_time = self.feed_handler.parse_publish_time(entry)
                        
                        # 获取当天的零点时间
                        today_start = self.feed_handler.get_today_start_time()
                        
                        # 如果新闻发布不是当天的，则跳过
                        if publish_time < today_start:
                            self.logger.info(f"Skipping non-today news: {title[:50]}... (Published at {publish_time.strftime('%Y-%m-%d %H:%M')})")
                            continue
                        
                        # 压缩内容
                        compressed_content = self.feed_handler.compress_content(content)
                        
                        # 获取当前东八区时间
                        current_east8_time = self.feed_handler.get_current_east8_time()
                        
                        # 检查重复
                        if not self.is_duplicate(title, content):
                            self.db_handler.insert_news(publish_time, current_east8_time, title, compressed_content, url)
                            self.logger.info(f"Added: {title[:50]}... (Published at {publish_time.strftime('%Y-%m-%d %H:%M')})")
                        else:
                            self.logger.info(f"Skipping duplicate: {title[:50]}...")
                    
                    except Exception as e:
                        self.logger.error(f"Error processing entry: {str(e)}")
            
            except Exception as e:
                self.logger.error(f"Error processing feed {feed_url}: {str(e)}")
        
        self.logger.info("News crawl completed!")
    
    def is_duplicate(self, title, content):
        clean_title = clean_text(title)
        clean_content = clean_text(content)
        
        existing_news = self.db_handler.get_all_news()
        
        for news in existing_news:
            db_title = clean_text(news['title'])
            db_content = clean_text(self.feed_handler.decompress_content(news['content']))
            
            title_sim = similarity(clean_title, db_title)
            content_sim = similarity(clean_content, db_content)
            
            if title_sim > 0.75 or content_sim > 0.75:
                return True
        
        return False