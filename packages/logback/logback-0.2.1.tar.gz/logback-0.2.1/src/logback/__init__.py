import logging
import os
import sys
import re
from logging.handlers import TimedRotatingFileHandler
import zipfile
from datetime import datetime, timedelta
import glob
from typing import Optional, Dict

# 跨平台颜色初始化
if sys.platform == 'win32':
    from colorama import Fore, Back, Style, init

    init(autoreset=True)
    COLOR_MAP = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Back.RED + Fore.WHITE + Style.BRIGHT,
    }
    COLOR_RESET = ''
else:
    # Linux/macOS ANSI颜色代码
    COLOR_MAP = {
        'DEBUG': '\033[36m',  # CYAN
        'INFO': '\033[32m',  # GREEN
        'WARNING': '\033[33m',  # YELLOW
        'ERROR': '\033[31m',  # RED
        'CRITICAL': '\033[41;37;1m',  # 红底白字加粗
    }
    COLOR_RESET = '\033[0m'


class EnhancedColorfulLogger:
    """
    增强型彩色日志记录器（修复日期格式问题）

    :param name: 日志名称（显示用）
    :param level: 日志级别
    :param log_file: 基础日志文件名（如"app.log"）
    :param backup_count: 保留的日志文件天数
    :param log_dir: 日志目录
    :param force_no_color: 强制禁用颜色
    :param zip_compression: ZIP压缩方式
    :param zip_level: ZIP压缩等级（1-9）
    """

    def __init__(self, name: str = 'FlaskApp', level: int = logging.DEBUG,
                 log_file: Optional[str] = None, backup_count: int = 7,
                 log_dir: str = 'logs', force_no_color: bool = False,
                 zip_compression=zipfile.ZIP_DEFLATED, zip_level: int = 9):
        self.name = name
        self.level = level
        self.log_file = log_file
        self.backup_count = backup_count
        self.log_dir = log_dir
        self.force_no_color = force_no_color
        self.zip_compression = zip_compression
        self.zip_level = zip_level
        self._loggers: Dict[str, logging.Logger] = {}

        os.makedirs(self.log_dir, exist_ok=True)

    def get_logger(self, module: Optional[str] = None) -> logging.Logger:
        """获取日志记录器（修复日期格式问题的核心修改）"""
        logger_name = f"{self.name}.{module}" if module else self.name

        if logger_name not in self._loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(self.level)
            logger.propagate = False

            if not logger.handlers:
                # 控制台handler（带颜色）
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(self.ColorFormatter(
                    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    force_no_color=self.force_no_color
                ))
                logger.addHandler(console_handler)

                if self.log_file:
                    # 生成带日期的初始文件名（app-YYYY-MM-DD.log）
                    base_name = os.path.splitext(self.log_file)[0]
                    dated_filename = f"{base_name}-{datetime.now().strftime('%Y-%m-%d')}.log"
                    full_path = os.path.join(self.log_dir, dated_filename)

                    # 配置TimedRotatingFileHandler
                    file_handler = TimedRotatingFileHandler(
                        filename=full_path,
                        when='midnight',
                        interval=1,
                        backupCount=self.backup_count,
                        encoding='utf-8'
                    )
                    # 禁用自动后缀并自定义匹配模式
                    file_handler.suffix = ""
                    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.log)?(\.zip)?$")

                    file_handler.setFormatter(logging.Formatter(
                        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    ))
                    file_handler.rotator = self._rotator
                    logger.addHandler(file_handler)

                    self._clean_old_logs()

            self._loggers[logger_name] = logger

        return self._loggers[logger_name]

    class ColorFormatter(logging.Formatter):
        def __init__(self, fmt=None, datefmt=None, force_no_color=False):
            super().__init__(fmt, datefmt)
            self.force_no_color = force_no_color

        def format(self, record):
            color = "" if self.force_no_color else COLOR_MAP.get(record.levelname, "")
            reset = "" if self.force_no_color else COLOR_RESET
            message = super().format(record)
            return f"{color}{message}{reset}"

    def _rotator(self, source: str, dest: str) -> None:
        """处理形如 app-YYYY-MM-DD.log 的日志压缩"""
        try:
            # 创建ZIP文件（app-YYYY-MM-DD.log.zip）
            with zipfile.ZipFile(
                    f"{dest}.zip",
                    mode='w',
                    compression=self.zip_compression,
                    compresslevel=self.zip_level
            ) as zf:
                zf.write(source, arcname=os.path.basename(dest))
            os.remove(source)
        except Exception as e:
            logging.error(f"日志压缩失败: {str(e)}")
            if os.path.exists(f"{dest}.zip"):
                os.remove(f"{dest}.zip")

    def _clean_old_logs(self) -> None:
        """清理过期的日志文件（匹配 app-YYYY-MM-DD.log 和 .zip 文件）"""
        cutoff_date = datetime.now() - timedelta(days=self.backup_count)

        for f in glob.glob(os.path.join(self.log_dir, '*-*-*.log*')):
            try:
                # 从文件名提取日期（app-YYYY-MM-DD.log 或 app-YYYY-MM-DD.log.zip）
                base_name = os.path.basename(f)
                date_str = "-".join(base_name.split('-')[1:4])[:10]  # 提取YYYY-MM-DD
                file_date = datetime.strptime(date_str, '%Y-%m-%d')

                if file_date < cutoff_date:
                    os.remove(f)
            except (ValueError, IndexError):
                continue

    # 快捷方法
    def debug(self, msg: str, module: Optional[str] = None, *args, **kwargs):
        self.get_logger(module).debug(msg, *args, **kwargs)

    def info(self, msg: str, module: Optional[str] = None, *args, **kwargs):
        self.get_logger(module).info(msg, *args, **kwargs)

    def warning(self, msg: str, module: Optional[str] = None, *args, **kwargs):
        self.get_logger(module).warning(msg, *args, **kwargs)

    def error(self, msg: str, module: Optional[str] = None, *args, **kwargs):
        self.get_logger(module).error(msg, *args, **kwargs)

    def critical(self, msg: str, module: Optional[str] = None, *args, **kwargs):
        self.get_logger(module).critical(msg, *args, **kwargs)