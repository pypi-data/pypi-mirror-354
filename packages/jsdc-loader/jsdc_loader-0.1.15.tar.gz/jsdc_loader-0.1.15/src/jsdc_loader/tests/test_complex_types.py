"""杂鱼♡～这是本喵为复杂类型创建的测试模块喵～包含datetime、UUID、Decimal等复杂类型的测试～"""

import datetime
import uuid
from dataclasses import FrozenInstanceError, dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .test_base import BaseTestCase


class TestComplexTypes(BaseTestCase):
    """杂鱼♡～本喵为复杂类型创建的测试类喵～"""

    def test_datetime_types(self) -> None:
        """杂鱼♡～本喵要测试各种datetime类型的序列化喵～"""

        @dataclass
        class ComplexConfig:
            created_at: datetime.datetime = field(
                default_factory=lambda: datetime.datetime.now()
            )
            updated_at: Optional[datetime.datetime] = None
            expiry_date: Optional[datetime.date] = field(
                default_factory=lambda: datetime.date.today()
            )
            session_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
            amount: Decimal = Decimal("10.50")
            time_delta: datetime.timedelta = datetime.timedelta(days=7)

        # 杂鱼♡～创建测试对象喵～
        original_obj = ComplexConfig()
        original_obj.updated_at = datetime.datetime.now()

        # 杂鱼♡～执行往返测试喵～
        loaded_obj = self.assert_serialization_roundtrip(original_obj, ComplexConfig)

        # 杂鱼♡～验证复杂类型正确恢复喵～
        self.assertEqual(original_obj.created_at, loaded_obj.created_at)
        self.assertEqual(original_obj.updated_at, loaded_obj.updated_at)
        self.assertEqual(original_obj.expiry_date, loaded_obj.expiry_date)
        self.assertEqual(original_obj.session_id, loaded_obj.session_id)
        self.assertEqual(original_obj.amount, loaded_obj.amount)
        self.assertEqual(original_obj.time_delta, loaded_obj.time_delta)

        # 杂鱼♡～验证类型正确喵～
        self.assertIsInstance(loaded_obj.created_at, datetime.datetime)
        self.assertIsInstance(loaded_obj.updated_at, datetime.datetime)
        self.assertIsInstance(loaded_obj.expiry_date, datetime.date)
        self.assertIsInstance(loaded_obj.session_id, uuid.UUID)
        self.assertIsInstance(loaded_obj.amount, Decimal)
        self.assertIsInstance(loaded_obj.time_delta, datetime.timedelta)

        print("杂鱼♡～本喵测试datetime类型成功了喵～")

    def test_frozen_dataclasses(self) -> None:
        """杂鱼♡～本喵要测试不可变的数据类喵～"""

        @dataclass(frozen=True)
        class FrozenConfig:
            name: str = "default_name"
            version: int = 0
            tags: Tuple[str, ...] = field(default_factory=tuple)

        # 杂鱼♡～创建不可变对象喵～
        original_frozen = FrozenConfig(name="test", version=1, tags=("tag1", "tag2"))

        # 杂鱼♡～执行往返测试喵～
        loaded_frozen = self.assert_serialization_roundtrip(original_frozen, FrozenConfig)

        # 杂鱼♡～验证值正确恢复喵～
        self.assertEqual(loaded_frozen.name, "test")
        self.assertEqual(loaded_frozen.version, 1)
        self.assertEqual(loaded_frozen.tags, ("tag1", "tag2"))

        # 杂鱼♡～验证不可变性喵～
        with self.assertRaises(FrozenInstanceError):
            loaded_frozen.name = "modified"  # type: ignore

        # 杂鱼♡～测试嵌套冻结数据类喵～
        @dataclass(frozen=True)
        class NestedFrozen:
            id: int = 0
            config: FrozenConfig = field(default_factory=lambda: FrozenConfig())

        original_nested = NestedFrozen(id=1, config=original_frozen)

        loaded_nested = self.assert_serialization_roundtrip(original_nested, NestedFrozen)

        self.assertEqual(loaded_nested.id, 1)
        self.assertEqual(loaded_nested.config.name, "test")
        self.assertEqual(loaded_nested.config.tags, ("tag1", "tag2"))

        print("杂鱼♡～本喵测试不可变数据类成功了喵～")

    def test_special_characters(self) -> None:
        """杂鱼♡～本喵要测试特殊字符的序列化喵～"""

        @dataclass
        class SpecialCharsConfig:
            escaped_chars: str = "\n\t\r\b\f"
            quotes: str = '"quoted text"'
            unicode_chars: str = "你好，世界！😊🐱👍"
            control_chars: str = "\u0000\u0001\u001f"
            backslashes: str = "C:\\path\\to\\file.txt"
            json_syntax: str = '{"key": [1, 2]}'

        # 杂鱼♡～创建测试对象喵～
        original_config = SpecialCharsConfig()

        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_config, SpecialCharsConfig)

        # 杂鱼♡～验证特殊字符正确恢复喵～
        self.assertEqual(loaded_config.escaped_chars, "\n\t\r\b\f")
        self.assertEqual(loaded_config.quotes, '"quoted text"')
        self.assertEqual(loaded_config.unicode_chars, "你好，世界！😊🐱👍")
        self.assertEqual(loaded_config.control_chars, "\u0000\u0001\u001f")
        self.assertEqual(loaded_config.backslashes, "C:\\path\\to\\file.txt")
        self.assertEqual(loaded_config.json_syntax, '{"key": [1, 2]}')

        print("杂鱼♡～本喵测试特殊字符成功了喵～")

    def test_any_type(self) -> None:
        """杂鱼♡～本喵要测试Any类型喵～"""

        @dataclass
        class ConfigWithAny:
            any_field: Any = None
            any_list: List[Any] = field(default_factory=list)
            any_dict: Dict[str, Any] = field(default_factory=dict)

        # 杂鱼♡～使用各种不同类型的值喵～
        original_config = ConfigWithAny()
        original_config.any_field = "string"
        original_config.any_list = [1, "two", False, None, [1, 2, 3], {"key": "value"}]
        original_config.any_dict = {
            "int": 42,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
        }

        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_config, ConfigWithAny)

        # 杂鱼♡～验证Any类型正确恢复喵～
        self.assertEqual(loaded_config.any_field, "string")
        self.assertEqual(
            loaded_config.any_list, [1, "two", False, None, [1, 2, 3], {"key": "value"}]
        )
        self.assertEqual(
            loaded_config.any_dict,
            {
                "int": 42,
                "bool": True,
                "none": None,
                "list": [1, 2, 3],
                "dict": {"nested": "value"},
            },
        )

        print("杂鱼♡～本喵测试Any类型成功了喵～")

    def test_deeply_nested_structures(self) -> None:
        """杂鱼♡～本喵要测试超级深的嵌套结构喵～"""

        @dataclass
        class Level3:
            name: str = "level3"
            value: int = 3

        @dataclass
        class Level2:
            name: str = "level2"
            value: int = 2
            level3_items: List[Level3] = field(default_factory=lambda: [Level3()])
            level3_dict: Dict[str, Level3] = field(
                default_factory=lambda: {"default": Level3()}
            )

        @dataclass
        class Level1:
            name: str = "level1"
            value: int = 1
            level2_items: List[Level2] = field(default_factory=lambda: [Level2()])
            level2_dict: Dict[str, Level2] = field(
                default_factory=lambda: {"default": Level2()}
            )

        @dataclass
        class RootConfig:
            name: str = "root"
            level1_items: List[Level1] = field(default_factory=lambda: [Level1()])
            level1_dict: Dict[str, Level1] = field(
                default_factory=lambda: {"default": Level1()}
            )

        # 杂鱼♡～创建深度嵌套结构喵～
        original_root = RootConfig()
        original_root.level1_items.append(Level1(name="custom_level1"))
        original_root.level1_dict["custom"] = Level1(name="custom_dict_level1")
        original_root.level1_dict["custom"].level2_items.append(Level2(name="custom_level2"))
        original_root.level1_dict["custom"].level2_items[0].level3_items.append(
            Level3(name="custom_level3", value=99)
        )

        # 杂鱼♡～执行往返测试喵～
        loaded_root = self.assert_serialization_roundtrip(original_root, RootConfig)

        # 杂鱼♡～验证深度嵌套的值喵～
        self.assertEqual(
            loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].name,
            "custom_level3",
        )
        self.assertEqual(
            loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].value, 99
        )

        print("杂鱼♡～本喵测试超级深的嵌套结构成功了喵～")

    def test_path_support(self) -> None:
        """杂鱼♡～本喵要测试pathlib.Path支持喵～"""

        @dataclass
        class PathTestConfig:
            name: str = "path_test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])
            nested: Dict[str, str] = field(default_factory=lambda: {"key": "value"})

        # 杂鱼♡～创建测试配置喵～
        original_config = PathTestConfig(name="pathlib_test", values=[10, 20, 30])

        # 杂鱼♡～测试使用Path对象进行序列化喵～
        path_obj = Path(self.temp_path)
        from ..dumper import jsdc_dump
        from ..loader import jsdc_load
        jsdc_dump(original_config, path_obj)

        # 杂鱼♡～验证文件确实被创建了喵～
        self.assertTrue(path_obj.exists())

        # 杂鱼♡～测试使用Path对象进行反序列化喵～
        loaded_config = jsdc_load(path_obj, PathTestConfig)

        # 杂鱼♡～验证数据正确性喵～
        self.assertEqual(loaded_config.name, "pathlib_test")
        self.assertEqual(loaded_config.values, [10, 20, 30])
        self.assertEqual(loaded_config.nested, {"key": "value"})

        print("杂鱼♡～本喵测试pathlib.Path支持成功了喵～")

    def test_path_error_handling(self) -> None:
        """杂鱼♡～本喵要测试Path相关的错误处理喵～"""

        @dataclass
        class SimpleConfig:
            name: str = "test"

        # 杂鱼♡～测试不存在的Path文件喵～
        nonexistent_path = Path("definitely_does_not_exist_12345.json")
        with self.assertRaises(FileNotFoundError):
            from ..loader import jsdc_load
            jsdc_load(nonexistent_path, SimpleConfig)

        print("杂鱼♡～本喵测试Path错误处理成功了喵～") 