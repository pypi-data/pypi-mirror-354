"""数据处理相关工具函数。"""

import hashlib
import random
import re
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union


def generate_random_string(length: int = 8, include_digits: bool = True) -> str:
    """生成随机字符串。

    Args:
        length: 字符串长度
        include_digits: 是否包含数字

    Returns:
        str: 随机字符串
    """
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    return "".join(random.choice(chars) for _ in range(length))


def calculate_md5(data: Union[str, bytes]) -> str:
    """计算MD5哈希值。

    Args:
        data: 输入数据

    Returns:
        str: MD5哈希值
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.md5(data).hexdigest()


def format_datetime(
    dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """格式化日期时间。

    Args:
        dt: 日期时间，默认为当前时间
        fmt: 格式字符串

    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """解析日期时间字符串。

    Args:
        dt_str: 日期时间字符串
        fmt: 格式字符串

    Returns:
        datetime: 解析后的日期时间对象
    """
    return datetime.strptime(dt_str, fmt)


def get_date_range(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    fmt: str = "%Y-%m-%d",
) -> List[str]:
    """获取日期范围内的所有日期。

    Args:
        start_date: 开始日期
        end_date: 结束日期
        fmt: 返回的日期格式

    Returns:
        List[str]: 日期列表
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, fmt)
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, fmt)

    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date.strftime(fmt))
        curr_date += timedelta(days=1)

    return date_list


def clean_text(text: str) -> str:
    """清理文本，移除多余空白和特殊字符。

    Args:
        text: 输入文本

    Returns:
        str: 清理后的文本
    """
    # 替换多个空白为单个空格
    text = re.sub(r"\s+", " ", text)
    # 移除首尾空白
    return text.strip()


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """将列表分割为指定大小的块。

    Args:
        lst: 输入列表
        chunk_size: 每个块的大小

    Returns:
        List[List[Any]]: 分块后的列表
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", separator: str = "."
) -> Dict[str, Any]:
    """将嵌套字典扁平化。

    Args:
        d: 嵌套字典
        parent_key: 父键前缀
        separator: 键分隔符

    Returns:
        Dict[str, Any]: 扁平化后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, separator).items())
        else:
            items.append((new_key, v))
    return dict(items)
