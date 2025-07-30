"""日志处理相关工具函数。"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union


def setup_logger(
    name: Optional[str] = None,
    level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_format: Optional[str] = None,
    date_format: str = "%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    """配置并获取日志记录器。

    Args:
        name: 日志记录器名称，默认使用根记录器
        level: 日志级别
        log_file: 日志文件路径，默认只输出到控制台
        log_format: 日志格式字符串
        date_format: 日期格式字符串

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 获取logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建控制台handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 如果指定了日志文件，创建文件handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """获取预先配置的日志记录器，如果不存在则创建。

    Args:
        name: 日志记录器名称

    Returns:
        logging.Logger: 日志记录器
    """
    logger = logging.getLogger(name)

    # 如果没有配置，使用默认配置
    if not logger.hasHandlers():
        return setup_logger(name)

    return logger


def create_rotating_log(
    log_dir: Union[str, Path],
    name: str,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """创建带文件轮转的日志记录器。

    Args:
        log_dir: 日志目录
        name: 日志记录器名称
        level: 日志级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的备份文件数量

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    from logging.handlers import RotatingFileHandler

    # 确保日志目录存在
    if isinstance(log_dir, str):
        log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # 日志文件路径
    log_file = log_dir / f"{name}.log"

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.hasHandlers():
        logger.handlers.clear()

    # 创建文件handler，支持文件轮转
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(level)

    # 设置格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    # 添加handler
    logger.addHandler(file_handler)

    # 添加控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def log_function_call(logger: logging.Logger, log_args: bool = True):
    """装饰器：记录函数调用信息。

    Args:
        logger: 日志记录器
        log_args: 是否记录参数值
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # 记录函数调用
            if log_args:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                logger.debug(f"调用函数 {func_name}({signature})")
            else:
                logger.debug(f"调用函数 {func_name}")

            # 执行函数
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(f"函数 {func_name} 执行出错: {str(e)}")
                raise

        return wrapper

    return decorator
