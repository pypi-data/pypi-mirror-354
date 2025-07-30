import logging
from logging.handlers import RotatingFileHandler

class LogHandler:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def get_logger(self):
        return self.logger