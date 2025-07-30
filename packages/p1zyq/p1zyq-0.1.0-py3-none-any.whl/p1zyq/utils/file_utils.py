"""文件处理相关工具函数。"""

import json
import os
import pickle
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def ensure_dir(directory: Union[str, Path]) -> Path:
    """确保目录存在，不存在则创建。

    Args:
        directory: 目录路径

    Returns:
        Path: 目录路径对象
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """从JSON文件加载数据。

    Args:
        file_path: JSON文件路径

    Returns:
        Dict: 加载的数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(
    data: Dict[str, Any], file_path: Union[str, Path], indent: int = 2
) -> None:
    """保存数据到JSON文件。

    Args:
        data: 要保存的数据
        file_path: 保存路径
        indent: 缩进空格数
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def load_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """从YAML文件加载数据。

    Args:
        file_path: YAML文件路径

    Returns:
        Dict: 加载的数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """保存数据到YAML文件。

    Args:
        data: 要保存的数据
        file_path: 保存路径
    """
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)


def load_pickle(file_path: Union[str, Path]) -> Any:
    """从Pickle文件加载数据。

    Args:
        file_path: Pickle文件路径

    Returns:
        Any: 加载的数据
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)


def save_pickle(data: Any, file_path: Union[str, Path]) -> None:
    """保存数据到Pickle文件。

    Args:
        data: 要保存的数据
        file_path: 保存路径
    """
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def list_files(
    directory: Union[str, Path], pattern: str = "*", recursive: bool = False
) -> List[Path]:
    """列出目录中符合模式的所有文件。

    Args:
        directory: 目录路径
        pattern: 匹配模式 (glob格式)
        recursive: 是否递归搜索子目录

    Returns:
        List[Path]: 文件路径列表
    """
    path = Path(directory)
    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))


def get_file_size(file_path: Union[str, Path], unit: str = "bytes") -> float:
    """获取文件大小。

    Args:
        file_path: 文件路径
        unit: 单位('bytes', 'KB', 'MB', 'GB')

    Returns:
        float: 文件大小
    """
    size_bytes = os.path.getsize(file_path)

    if unit == "bytes":
        return size_bytes
    elif unit == "KB":
        return size_bytes / 1024
    elif unit == "MB":
        return size_bytes / (1024 * 1024)
    elif unit == "GB":
        return size_bytes / (1024 * 1024 * 1024)
    else:
        raise ValueError(f"不支持的单位: {unit}")
