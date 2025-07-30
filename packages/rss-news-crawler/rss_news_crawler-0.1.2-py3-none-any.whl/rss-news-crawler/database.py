import sqlite3
import zlib
from datetime import datetime
import pytz

class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def init_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publish_time DATETIME NOT NULL,
            crawl_time DATETIME NOT NULL,
            title TEXT NOT NULL,
            content BLOB NOT NULL,
            url TEXT NOT NULL UNIQUE
        )
        ''')
        self.cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_publish_time ON news(publish_time)
        ''')
        self.conn.commit()
    
    def insert_news(self, publish_time, crawl_time, title, content, url):
        self.cursor.execute(
            "INSERT OR IGNORE INTO news (publish_time, crawl_time, title, content, url) VALUES (?, ?, ?, ?, ?)",
            (publish_time, crawl_time, title, content, url)
        )
        self.conn.commit()
    
    def get_all_news(self):
        self.cursor.execute("SELECT publish_time, title, content, url FROM news")
        rows = self.cursor.fetchall()
        
        news_list = []
        for row in rows:
            news_dict = {
                'publish_time': row[0],
                'title': row[1],
                'content': row[2],  # 压缩后的内容
                'url': row[3]
            }
            news_list.append(news_dict)
        
        return news_list
    
    def close(self):
        if self.conn:
            self.conn.close()