"""工具函数测试。"""

import json
import pickle
import os
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from p1zyq.utils.file_utils import (
    ensure_dir,
    load_json,
    save_json,
    load_pickle,
    save_pickle,
    list_files,
    get_file_size,
)
from p1zyq.utils.data_utils import (
    generate_random_string,
    calculate_md5,
    clean_text,
    chunk_list,
    flatten_dict,
)
from p1zyq.utils.logging_utils import setup_logger, get_logger, log_function_call


def test_ensure_dir(temp_dir):
    """测试确保目录存在。"""
    # 动态导入，避免模板变量替换问题

    test_dir = temp_dir / "test_dir" / "nested"
    path = ensure_dir(test_dir)

    assert path.exists()
    assert path.is_dir()


def test_json_roundtrip(temp_dir, sample_data):
    """测试JSON数据的保存和加载。"""

    json_file = temp_dir / "test.json"

    # 保存数据
    save_json(sample_data, json_file)
    assert json_file.exists()

    # 加载数据
    loaded_data = load_json(json_file)
    assert loaded_data == sample_data


def test_pickle_roundtrip(temp_dir, sample_data):
    """测试Pickle数据的保存和加载。"""

    pickle_file = temp_dir / "test.pkl"

    # 保存数据
    save_pickle(sample_data, pickle_file)
    assert pickle_file.exists()

    # 加载数据
    loaded_data = load_pickle(pickle_file)
    assert loaded_data == sample_data


def test_list_files(temp_dir):
    """测试列出文件。"""

    # 创建测试文件
    file1 = temp_dir / "file1.txt"
    file2 = temp_dir / "file2.txt"
    file3 = temp_dir / "subdir" / "file3.txt"

    file1.touch()
    file2.touch()
    ensure_dir(file3.parent)
    file3.touch()

    # 非递归测试
    files = list_files(temp_dir, "*.txt")
    assert len(files) == 2
    assert set(f.name for f in files) == {"file1.txt", "file2.txt"}

    # 递归测试
    files = list_files(temp_dir, "*.txt", recursive=True)
    assert len(files) == 3
    assert set(f.name for f in files) == {"file1.txt", "file2.txt", "file3.txt"}


def test_get_file_size(temp_dir):
    """测试获取文件大小。"""

    # 创建固定大小的文件
    test_file = temp_dir / "size_test.dat"
    with open(test_file, "wb") as f:
        f.write(b"0" * 1024)  # 1KB的文件

    assert get_file_size(test_file) == 1024
    assert get_file_size(test_file, "KB") == 1.0
    assert get_file_size(test_file, "MB") == 1.0 / 1024

    # 测试无效单位
    with pytest.raises(ValueError):
        get_file_size(test_file, "invalid_unit")


def test_generate_random_string():
    """测试生成随机字符串。"""

    # 默认设置
    s1 = generate_random_string()
    assert len(s1) == 8
    assert s1.isalnum()  # 包含字母和数字

    # 自定义长度
    s2 = generate_random_string(length=12)
    assert len(s2) == 12

    # 不包含数字
    s3 = generate_random_string(include_digits=False)
    assert s3.isalpha()  # 只包含字母

    # 两次生成的字符串应该不同
    assert s1 != generate_random_string()


def test_calculate_md5():
    """测试MD5哈希计算。"""

    # 字符串输入
    assert calculate_md5("hello") == "5d41402abc4b2a76b9719d911017c592"

    # 字节输入
    assert calculate_md5(b"hello") == "5d41402abc4b2a76b9719d911017c592"


def test_clean_text():
    """测试文本清理。"""

    assert clean_text("  hello  world  ") == "hello world"
    assert clean_text("\t\nhello\n\tworld\n") == "hello world"
    assert clean_text("multiple    spaces    here") == "multiple spaces here"


def test_chunk_list():
    """测试列表分块。"""

    # 空列表
    assert chunk_list([], 3) == []

    # 正常分块
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    # 块大小等于列表长度
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]

    # 块大小大于列表长度
    assert chunk_list([1, 2], 5) == [[1, 2]]


def test_flatten_dict():
    """测试字典扁平化。"""

    nested_dict = {"a": 1, "b": {"c": 2, "d": {"e": 3}}, "f": 4}

    flat_dict = flatten_dict(nested_dict)

    assert flat_dict == {"a": 1, "b.c": 2, "b.d.e": 3, "f": 4}

    # 自定义分隔符
    flat_dict_custom = flatten_dict(nested_dict, separator="_")
    assert flat_dict_custom == {"a": 1, "b_c": 2, "b_d_e": 3, "f": 4}


def test_setup_logger():
    """测试日志设置函数。"""

    # 设置基本控制台日志
    logger = setup_logger("test_logger", level=logging.DEBUG)
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

    # 测试带文件的日志配置
    with patch("p1zyq.utils.logging_utils.logging.FileHandler") as mock_file_handler:
        mock_instance = MagicMock()
        mock_file_handler.return_value = mock_instance

        logger = setup_logger("test_file_logger", log_file="test.log")
        assert logger.name == "test_file_logger"
        assert len(logger.handlers) == 2  # 控制台和文件
        mock_file_handler.assert_called_once_with("test.log", encoding="utf-8")


def test_log_function_call():
    """测试函数调用日志装饰器。"""

    # 创建模拟logger
    mock_logger = MagicMock()

    # 定义测试函数
    @log_function_call(mock_logger, log_args=True)
    def test_func(arg1, arg2, kwarg1=None):
        return arg1 + arg2

    # 调用并验证日志记录
    result = test_func(1, 2, kwarg1="test")
    assert result == 3
    mock_logger.debug.assert_called_once()

    # 测试异常情况
    mock_logger.reset_mock()

    @log_function_call(mock_logger)
    def failing_func():
        raise ValueError("测试错误")

    with pytest.raises(ValueError):
        failing_func()

    mock_logger.debug.assert_called_once()
    mock_logger.exception.assert_called_once()
