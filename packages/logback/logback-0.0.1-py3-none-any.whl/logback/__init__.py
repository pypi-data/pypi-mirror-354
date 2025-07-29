import logging
import os
from logback.colorama import Fore, Back, Style, init
from logback.logging.handlers import TimedRotatingFileHandler
import gzip
import shutil
from datetime import datetime
import glob

# 初始化 colorama
init(autoreset=True)


class EnhancedColorfulLogger:
    """
        :param name: 日志名称
        :param level: 日志级别
        :param log_file: 日志文件名(不含路径)
        :param backup_count: 保留的日志文件天数
        :param log_dir: 日志目录(相对于项目根目录)
    """
    COLOR_MAP = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Back.RED + Fore.WHITE + Style.BRIGHT,
    }

    def __init__(self, name='MyLogger', level=logging.DEBUG,
                 log_file=None, backup_count=7, log_dir='logs'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        self.backup_count = backup_count
        self.log_dir = log_dir

        # 确保日志目录存在
        os.makedirs(self.log_dir, exist_ok=True)

        if not self.logger.handlers:
            # 控制台 handler（带颜色）
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.ColorFormatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            self.logger.addHandler(console_handler)

            # 文件 handler（按天分割）
            if log_file:
                full_path = os.path.join(self.log_dir, log_file)
                file_handler = TimedRotatingFileHandler(
                    filename=full_path,
                    when='midnight',  # 每天午夜分割
                    interval=1,
                    backupCount=backup_count,
                    encoding='utf-8'
                )
                file_handler.suffix = "%Y-%m-%d.log"
                file_handler.setFormatter(logging.Formatter(
                    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                ))
                file_handler.namer = self._namer  # 设置自定义文件名处理器
                file_handler.rotator = self._rotator  # 设置自定义旋转处理器
                self.logger.addHandler(file_handler)

                # 启动时清理旧日志
                self._clean_old_logs()

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            color = EnhancedColorfulLogger.COLOR_MAP.get(record.levelname, '')
            message = super().format(record)
            return f"{color}{message}"

    def _namer(self, name):
        """自定义日志文件名格式"""
        return name.replace(".log", "") + ".log"

    def _rotator(self, source, dest):
        """自定义旋转处理器，用于压缩旧日志"""
        # 先让父类完成文件重命名
        os.rename(source, dest)

        # 压缩文件
        with open(dest, 'rb') as f_in:
            with gzip.open(dest + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # 删除未压缩的文件
        os.remove(dest)

    def _clean_old_logs(self):
        """清理过期的日志文件"""
        now = datetime.now()

        # 查找所有日志文件
        for log_file in glob.glob(os.path.join(self.log_dir, '*.log*')):
            # 从文件名中提取日期
            try:
                if log_file.endswith('.gz'):
                    # 压缩日志文件格式: app.log.2023-01-01.log.gz
                    date_str = os.path.basename(log_file).split('.')[2]
                else:
                    # 普通日志文件格式: app.log.2023-01-01.log
                    date_str = os.path.basename(log_file).split('.')[2]

                file_date = datetime.strptime(date_str, '%Y-%m-%d')

                # 如果文件日期早于保留期限，则删除
                if (now - file_date).days > self.backup_count:
                    os.remove(log_file)
            except (IndexError, ValueError):
                # 文件名格式不匹配，跳过
                continue

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)