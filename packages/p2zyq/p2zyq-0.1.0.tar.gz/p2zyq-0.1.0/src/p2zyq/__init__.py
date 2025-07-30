"""Top-level package for p2zyq."""

import os
import logging

__author__ = """Zhou Yuanqi"""
__email__ = "zyq1034378361@gmail.com"

# 版本管理
from ._version import get_version

# 如果环境变量设置了调试模式，添加提交哈希到版本号
# 这行代码设置包的版本号。它调用get_version()函数获取版本，
# 并根据环境变量DEBUG的值决定是否包含Git提交哈希。
# 当DEBUG环境变量设置为'1'或'true'时，版本号会包含提交哈希，
# 这有助于在调试模式下更精确地识别代码版本。
__version__ = get_version(
    with_commit=os.environ.get("DEBUG", "").lower() in ("1", "true")
)


# 配置基本日志
# 在包的__init__.py中配置日志是为了确保当包被导入时就立即设置好日志系统
# 这样包的所有模块都可以使用相同的日志配置，保持一致的日志格式和级别
# 根据DEBUG环境变量自动调整日志级别，便于开发调试和生产环境的切换
logging.basicConfig(
    level=logging.INFO
    if os.environ.get("DEBUG", "").lower() not in ("1", "true")
    else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# 导入工具函数
from . import utils
