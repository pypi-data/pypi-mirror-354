"""杂鱼♡～这是本喵为边缘情况创建的测试模块喵～包含各种特殊情况和边缘测试～"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .test_base import BaseTestCase


class TestEdgeCases(BaseTestCase):
    """杂鱼♡～本喵为边缘情况创建的测试类喵～"""

    def test_edge_cases_fixes(self) -> None:
        """杂鱼♡～本喵要测试一些边缘情况喵～"""

        # 杂鱼♡～测试空字符串字段喵～
        @dataclass
        class EmptyStringConfig:
            empty_str: str = ""
            normal_str: str = "normal"

        original_empty_config = EmptyStringConfig()
        loaded_empty = self.assert_serialization_roundtrip(original_empty_config, EmptyStringConfig)

        self.assertEqual(loaded_empty.empty_str, "")
        self.assertEqual(loaded_empty.normal_str, "normal")

        # 杂鱼♡～测试零值数字字段喵～
        @dataclass
        class ZeroValueConfig:
            zero_int: int = 0
            zero_float: float = 0.0
            false_bool: bool = False

        original_zero_config = ZeroValueConfig()
        loaded_zero = self.assert_serialization_roundtrip(original_zero_config, ZeroValueConfig)

        self.assertEqual(loaded_zero.zero_int, 0)
        self.assertEqual(loaded_zero.zero_float, 0.0)
        self.assertEqual(loaded_zero.false_bool, False)

        # 杂鱼♡～测试字符串中的特殊JSON字符喵～
        @dataclass
        class JsonSpecialCharsConfig:
            json_like: str = '{"key": "value", "array": [1,2,3]}'
            escaped: str = "Line 1\nLine 2\tTabbed"
            quotes: str = 'He said "Hello" to her'

        original_special_config = JsonSpecialCharsConfig()
        loaded_special = self.assert_serialization_roundtrip(original_special_config, JsonSpecialCharsConfig)

        self.assertEqual(loaded_special.json_like, '{"key": "value", "array": [1,2,3]}')
        self.assertEqual(loaded_special.escaped, "Line 1\nLine 2\tTabbed")
        self.assertEqual(loaded_special.quotes, 'He said "Hello" to her')

        print("杂鱼♡～本喵测试边缘情况成功了喵～")

    def test_formatting_options(self) -> None:
        """杂鱼♡～本喵要测试不同的格式化选项喵～"""

        @dataclass
        class SimpleConfig:
            name: str = "test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])
            nested: Dict[str, Any] = field(
                default_factory=lambda: {"a": 1, "b": [2, 3], "c": {"d": 4}}
            )

        original_config = SimpleConfig()

        # 杂鱼♡～测试indent=0的情况喵～
        from ..dumper import jsdc_dump
        from ..loader import jsdc_load
        
        jsdc_dump(original_config, self.temp_path, indent=0)

        # 杂鱼♡～加载并验证内容喵～
        loaded_zero_indent = jsdc_load(self.temp_path, SimpleConfig)
        self.assertEqual(loaded_zero_indent.name, "test")

        # 杂鱼♡～测试其他缩进选项喵～
        for indent in [2, 4, 8]:
            # 杂鱼♡～使用不同的缩进序列化喵～
            jsdc_dump(original_config, self.temp_path, indent=indent)

            # 杂鱼♡～读取序列化后的内容喵～
            with open(self.temp_path, "r") as f:
                content = f.read()

            # 杂鱼♡～反序列化确认内容正确喵～
            loaded = jsdc_load(self.temp_path, SimpleConfig)
            self.assertEqual(loaded.name, "test")
            self.assertEqual(loaded.values, [1, 2, 3])
            self.assertEqual(loaded.nested, {"a": 1, "b": [2, 3], "c": {"d": 4}})

            # 杂鱼♡～如果有缩进，确认内容中包含换行符喵～
            self.assertIn("\n", content)

        print("杂鱼♡～本喵测试格式化选项成功了喵～")

    def test_dump_load_with_invalid_types(self) -> None:
        """杂鱼♡～本喵要测试当杂鱼提供错误类型时的异常处理喵～"""
        import tempfile
        from typing import List, Dict
        
        # 杂鱼♡～首先定义一个简单的测试数据类喵～
        @dataclass
        class SimpleTestData:
            name: str
            count: int
            enabled: bool
            scores: List[float] = field(default_factory=list)
            metadata: Dict[str, str] = field(default_factory=dict)
        
        # 杂鱼♡～创建正确的测试实例喵～
        valid_data = SimpleTestData(
            name="test_data",
            count=42,
            enabled=True,
            scores=[98.5, 87.3, 91.0],
            metadata={"created_by": "neko", "purpose": "test"}
        )
        
        # 杂鱼♡～先正常保存一次数据喵～
        valid_temp_path = self.temp_path
        from ..dumper import jsdc_dump
        jsdc_dump(valid_data, valid_temp_path)
        
        # 杂鱼♡～验证初始文件内容是正确的喵～
        try:
            from ..loader import jsdc_load
            loaded_valid_data = jsdc_load(valid_temp_path, SimpleTestData)
            self.assertEqual(loaded_valid_data.name, valid_data.name)
            self.assertEqual(loaded_valid_data.count, valid_data.count)
            self.assertEqual(loaded_valid_data.enabled, valid_data.enabled)
            self.assertEqual(loaded_valid_data.scores, valid_data.scores)
            self.assertEqual(loaded_valid_data.metadata, valid_data.metadata)
        except Exception as e:
            self.fail(f"杂鱼♡～加载有效数据失败了喵～：{str(e)}")
        
        # 杂鱼♡～准备一些无效类型的数据喵～
        invalid_data_samples = [
            SimpleTestData(name=123, count=42, enabled=True),  # type: ignore
            SimpleTestData(name="test", count="fortytwo", enabled=True),  # type: ignore
            SimpleTestData(name="test", count=42, enabled="yes"),  # type: ignore
        ]
        
        # 杂鱼♡～测试jsdc_dump异常处理喵～
        for i, invalid_data in enumerate(invalid_data_samples):
            # 使用新临时文件避免污染原始文件
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                invalid_temp_path = temp_file.name
            
            # 杂鱼♡～期待类型错误被捕获喵～
            with self.assertRaises((TypeError, ValueError)) as context:
                jsdc_dump(invalid_data, invalid_temp_path)
            
            # 杂鱼♡～确保异常被正确抛出喵～
            self.assertIsNotNone(context.exception)

        print("杂鱼♡～本喵的类型错误测试全部通过了喵～你的代码异常处理做得还不错呢～") 