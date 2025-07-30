"""杂鱼♡～这是本喵为联合类型创建的测试模块喵～包含Union和Optional类型的测试～"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from .test_base import BaseTestCase


class TestUnionTypes(BaseTestCase):
    """杂鱼♡～本喵为联合类型创建的测试类喵～"""

    def test_simple_union_types(self) -> None:
        """杂鱼♡～本喵要测试简单的联合类型喵～"""

        @dataclass
        class ConfigWithUnions:
            int_or_str: Union[int, str] = 42
            dict_or_list: Union[Dict[str, int], List[int]] = field(
                default_factory=lambda: {"a": 1}
            )

        # 杂鱼♡～测试不同的联合类型值喵～
        original_config1 = ConfigWithUnions(int_or_str=42, dict_or_list={"a": 1, "b": 2})
        original_config2 = ConfigWithUnions(int_or_str="string_value", dict_or_list=[1, 2, 3])

        # 杂鱼♡～测试第一个配置喵～
        loaded_config1 = self.assert_serialization_roundtrip(original_config1, ConfigWithUnions)
        self.assertEqual(loaded_config1.int_or_str, 42)
        self.assertEqual(loaded_config1.dict_or_list, {"a": 1, "b": 2})

        # 杂鱼♡～测试第二个配置喵～
        loaded_config2 = self.assert_serialization_roundtrip(original_config2, ConfigWithUnions)
        self.assertEqual(loaded_config2.int_or_str, "string_value")
        self.assertEqual(loaded_config2.dict_or_list, [1, 2, 3])

        print("杂鱼♡～本喵测试简单联合类型成功了喵～")

    def test_optional_types(self) -> None:
        """杂鱼♡～本喵要测试Optional类型喵～"""

        @dataclass
        class ConfigWithOptionals:
            maybe_str: Optional[str] = None
            maybe_int: Optional[int] = None
            maybe_list: Optional[List[str]] = None

        # 杂鱼♡～测试None值喵～
        original_config1 = ConfigWithOptionals()
        loaded_config1 = self.assert_serialization_roundtrip(original_config1, ConfigWithOptionals)
        
        self.assertIsNone(loaded_config1.maybe_str)
        self.assertIsNone(loaded_config1.maybe_int)
        self.assertIsNone(loaded_config1.maybe_list)

        # 杂鱼♡～测试有值的情况喵～
        original_config2 = ConfigWithOptionals(
            maybe_str="test",
            maybe_int=42,
            maybe_list=["item1", "item2"]
        )
        loaded_config2 = self.assert_serialization_roundtrip(original_config2, ConfigWithOptionals)
        
        self.assertEqual(loaded_config2.maybe_str, "test")
        self.assertEqual(loaded_config2.maybe_int, 42)
        self.assertEqual(loaded_config2.maybe_list, ["item1", "item2"])

        print("杂鱼♡～本喵测试Optional类型成功了喵～")

    def test_complex_union_types(self) -> None:
        """杂鱼♡～本喵要测试更复杂的联合类型喵～"""

        @dataclass
        class ConfigA:
            type: str = "A"
            value_a: int = 1

        @dataclass
        class ConfigB:
            type: str = "B"
            value_b: str = "b"

        @dataclass
        class NestedConfig:
            name: str = "nested"
            value: Union[int, str] = 42

        # 杂鱼♡～测试简单联合类型喵～
        original_config1 = NestedConfig(value=42)
        original_config2 = NestedConfig(value="string")

        # 杂鱼♡～测试第一个配置喵～
        loaded_config1 = self.assert_serialization_roundtrip(original_config1, NestedConfig)
        self.assertEqual(loaded_config1.value, 42)

        # 杂鱼♡～测试第二个配置喵～
        loaded_config2 = self.assert_serialization_roundtrip(original_config2, NestedConfig)
        self.assertEqual(loaded_config2.value, "string")

        # 杂鱼♡～测试对象联合类型喵～
        @dataclass
        class ComplexConfig:
            value: Union[ConfigA, ConfigB] = field(default_factory=lambda: ConfigA())

        original_complex1 = ComplexConfig(value=ConfigA(value_a=99))
        original_complex2 = ComplexConfig(value=ConfigB(value_b="test"))

        # 杂鱼♡～测试第一个复杂配置喵～
        loaded_complex1 = self.assert_serialization_roundtrip(original_complex1, ComplexConfig)
        self.assertEqual(loaded_complex1.value.type, "A")
        self.assertEqual(loaded_complex1.value.value_a, 99)

        # 杂鱼♡～测试第二个复杂配置喵～
        loaded_complex2 = self.assert_serialization_roundtrip(original_complex2, ComplexConfig)
        self.assertEqual(loaded_complex2.value.type, "B")
        self.assertEqual(loaded_complex2.value.value_b, "test")

        print("杂鱼♡～本喵测试复杂联合类型成功了喵～")

    def test_mixed_types_serialization(self) -> None:
        """杂鱼♡～本喵要测试混合类型序列化喵～"""

        @dataclass
        class MixedConfig:
            any_field: Any = None
            union_field: Union[int, str, List[int]] = 42
            optional_field: Optional[str] = None

        # 杂鱼♡～测试各种混合类型的组合喵～
        test_cases = [
            # (any_field, union_field, optional_field)
            ("string_value", 100, "optional_string"),
            ([1, 2, 3], "union_string", None),
            ({"nested": "dict"}, "union_list_test", "another_string"),
            (None, 999, None),
        ]

        for i, (any_val, union_val, opt_val) in enumerate(test_cases):
            with self.subTest(case=i):
                original_config = MixedConfig(
                    any_field=any_val, union_field=union_val, optional_field=opt_val
                )

                # 杂鱼♡～执行往返测试喵～
                loaded = self.assert_serialization_roundtrip(original_config, MixedConfig)

                # 杂鱼♡～验证每个字段喵～
                self.assertEqual(loaded.any_field, any_val)
                self.assertEqual(loaded.union_field, union_val)
                self.assertEqual(loaded.optional_field, opt_val)

        # 杂鱼♡～单独测试Union中的列表类型喵～
        @dataclass
        class ListUnionConfig:
            list_field: Union[str, List[int]] = field(default_factory=lambda: [1, 2, 3])

        original_list_config = ListUnionConfig(list_field=[10, 20, 30])
        loaded_list = self.assert_serialization_roundtrip(original_list_config, ListUnionConfig)

        # 杂鱼♡～验证列表在Union中正确处理喵～
        self.assertEqual(loaded_list.list_field, [10, 20, 30])
        self.assertIsInstance(loaded_list.list_field, list)

        print("杂鱼♡～本喵测试混合类型序列化成功了喵～")

    def test_default_values(self) -> None:
        """杂鱼♡～本喵要测试Union类型的默认值处理喵～"""

        @dataclass
        class ConfigWithDefaults:
            required_int: int = 0
            required_str: str = ""
            optional_int: int = 42
            optional_str: str = "default"
            optional_list: List[str] = field(default_factory=lambda: ["default_item"])
            optional_dict: Dict[str, int] = field(default_factory=lambda: {"default_key": 1})

        # 杂鱼♡～使用部分JSON反序列化，其他字段应该使用默认值喵～
        from ..loader import jsdc_loads
        partial_json = '{"required_int": 456, "optional_int": 99, "optional_list": ["custom_item"]}'
        partial_config = jsdc_loads(partial_json, ConfigWithDefaults)

        # 杂鱼♡～验证自定义值和默认值混合喵～
        self.assertEqual(partial_config.required_int, 456)  # 自定义值
        self.assertEqual(partial_config.required_str, "")  # 默认值
        self.assertEqual(partial_config.optional_int, 99)  # 自定义值
        self.assertEqual(partial_config.optional_str, "default")  # 默认值
        self.assertEqual(partial_config.optional_list, ["custom_item"])  # 自定义值
        self.assertEqual(partial_config.optional_dict, {"default_key": 1})  # 默认值

        print("杂鱼♡～本喵测试Union类型默认值处理成功了喵～") 