"""版本管理模块。"""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple


__version__ = "0.1.0"


def get_version_from_git() -> Optional[str]:
    """从git标签获取版本。

    返回:
        Optional[str]: 版本号，如果无法获取则返回None
    """
    try:
        # 运行git命令获取最近的标签
        cmd = ["git", "describe", "--tags", "--abbrev=0"]
        git_tag = subprocess.check_output(cmd, universal_newlines=True).strip()

        # 如果标签以'v'开头，移除'v'
        if git_tag.startswith("v"):
            git_tag = git_tag[1:]

        # 验证版本号格式
        if re.match(r"^\d+\.\d+\.\d+", git_tag):
            return git_tag
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return None


def get_git_commit() -> Optional[str]:
    """获取当前git提交哈希。

    返回:
        Optional[str]: 提交哈希短版本，如果无法获取则返回None
    """
    try:
        cmd = ["git", "rev-parse", "--short", "HEAD"]
        return subprocess.check_output(cmd, universal_newlines=True).strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return None


def get_version_from_pkg_info() -> Optional[str]:
    """从已安装的包信息中获取版本。

    返回:
        Optional[str]: 版本号，如果无法获取则返回None
    """
    try:
        from importlib.metadata import version, PackageNotFoundError

        try:
            return version("p2zyq")
        except PackageNotFoundError:
            pass
    except ImportError:
        pass

    return None


def get_version_from_env() -> Optional[str]:
    """从环境变量获取版本号。

    在CI/CD环境中非常有用。

    返回:
        Optional[str]: 环境变量中的版本号，如果未设置则返回None
    """
    # 检查常见的环境变量
    for env_var in ["VERSION", "P2ZYQ_VERSION"]:
        if env_var in os.environ:
            return os.environ[env_var]

    return None


def get_version(with_commit: bool = False) -> str:
    """获取版本号，按以下优先级：
    1. 从环境变量
    2. 从git标签
    3. 从包信息
    4. 从__version__变量

    参数:
        with_commit: 是否附加git提交哈希

    返回:
        str: 版本号，可选带git提交哈希（格式：1.0.0+abcdef）
    """
    # 首先尝试从环境变量获取
    env_version = get_version_from_env()
    if env_version:
        version_str = env_version
    else:
        # 尝试从git获取
        git_version = get_version_from_git()
        if git_version:
            version_str = git_version
        else:
            # 尝试从包信息获取
            pkg_version = get_version_from_pkg_info()
            if pkg_version:
                version_str = pkg_version
            else:
                # 使用默认版本
                version_str = __version__

    # 添加git提交哈希
    if with_commit:
        commit = get_git_commit()
        if commit:
            return f"{version_str}+{commit}"

    return version_str
