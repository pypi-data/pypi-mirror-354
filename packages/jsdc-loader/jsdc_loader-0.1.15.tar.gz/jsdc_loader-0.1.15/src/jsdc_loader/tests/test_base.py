"""杂鱼♡～这是本喵为所有测试类创建的基础模块喵～这里有共用的设置和工具～"""

import os
import tempfile
import unittest
from typing import Type, TypeVar

# 杂鱼♡～本喵要让pydantic导入变成可选的喵～
try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    # 杂鱼♡～没有pydantic时，本喵创建一个虚拟的BaseModel喵～
    HAS_PYDANTIC = False
    class BaseModel:
        """杂鱼♡～虚拟的BaseModel，只是为了测试能运行喵～"""
        pass

from ..dumper import jsdc_dump, jsdc_dumps
from ..loader import jsdc_load, jsdc_loads

T = TypeVar('T')


class BaseTestCase(unittest.TestCase):
    """杂鱼♡～这是本喵为所有测试类创建的基础类喵～提供共用的设置和工具方法～"""

    def setUp(self) -> None:
        """杂鱼♡～本喵要设置测试环境喵～"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()

    def tearDown(self) -> None:
        """杂鱼♡～本喵要清理测试环境喵～"""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def assert_serialization_roundtrip(self, original: T, cls: Type[T]) -> T:
        """杂鱼♡～本喵的通用序列化往返测试方法喵～
        
        Args:
            original: 原始对象
            cls: 对象类型
            
        Returns:
            反序列化后的对象
            
        Raises:
            AssertionError: 当往返测试失败时
        """
        # 杂鱼♡～序列化到文件喵～
        jsdc_dump(original, self.temp_path)
        
        # 杂鱼♡～从文件反序列化喵～
        loaded = jsdc_load(self.temp_path, cls)
        
        return loaded

    def assert_string_serialization_roundtrip(self, original: T, cls: Type[T]) -> T:
        """杂鱼♡～本喵的字符串序列化往返测试方法喵～
        
        Args:
            original: 原始对象
            cls: 对象类型
            
        Returns:
            反序列化后的对象
            
        Raises:
            AssertionError: 当往返测试失败时
        """
        # 杂鱼♡～序列化到字符串喵～
        json_str = jsdc_dumps(original)
        self.assertIsInstance(json_str, str)
        
        # 杂鱼♡～从字符串反序列化喵～
        loaded = jsdc_loads(json_str, cls)
        
        return loaded

    def assert_both_serialization_methods(self, original: T, cls: Type[T]) -> T:
        """杂鱼♡～本喵的双重序列化测试方法喵～同时测试文件和字符串序列化～
        
        Args:
            original: 原始对象
            cls: 对象类型
            
        Returns:
            反序列化后的对象
        """
        # 杂鱼♡～测试文件序列化喵～
        file_loaded = self.assert_serialization_roundtrip(original, cls)
        
        # 杂鱼♡～测试字符串序列化喵～
        string_loaded = self.assert_string_serialization_roundtrip(original, cls)
        
        # 杂鱼♡～两种方法的结果应该一致喵～
        self.assertEqual(file_loaded, string_loaded)
        
        return file_loaded
        
    def create_temp_file(self, suffix: str = ".json") -> str:
        """杂鱼♡～本喵创建临时文件的工具方法喵～
        
        Args:
            suffix: 文件后缀
            
        Returns:
            临时文件路径
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_path = temp_file.name
        temp_file.close()
        return temp_path

    def cleanup_temp_file(self, temp_path: str) -> None:
        """杂鱼♡～本喵清理临时文件的工具方法喵～
        
        Args:
            temp_path: 要清理的文件路径
        """
        if os.path.exists(temp_path):
            os.remove(temp_path) 