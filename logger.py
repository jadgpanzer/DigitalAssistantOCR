import logging
from pathlib import Path

class Logger:
    def __init__(self, log_file='app.log', log_level='INFO'):
        self.logger = logging.getLogger(__name__)
        self.setup_logger(log_file, log_level)

    def setup_logger(self, log_file, log_level):
        """配置日志系统"""
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 配置根日志
        self.logger.setLevel(log_level.upper())
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, level, message):
        """统一日志记录方法"""
        getattr(self.logger, level.lower())(message)
