"""杂鱼♡～这是本喵为验证功能创建的测试模块喵～包含类型验证和错误处理测试～"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Union

from .test_base import BaseTestCase


class TestValidation(BaseTestCase):
    """杂鱼♡～本喵为验证功能创建的测试类喵～"""

    def test_type_validation_on_load(self) -> None:
        """杂鱼♡～本喵要测试加载时的类型验证喵～"""

        @dataclass
        class TypedConfig:
            integer: int = 0
            string: str = ""
            boolean: bool = False
            float_val: float = 0.0
            list_of_ints: List[int] = field(default_factory=list)

        # 杂鱼♡～创建一个有效的JSON测试喵～
        from ..loader import jsdc_loads
        valid_json = '{"integer": 42, "string": "text", "boolean": true, "float_val": 3.14, "list_of_ints": [1, 2, 3]}'

        # 杂鱼♡～验证正确的类型可以被加载喵～
        config = jsdc_loads(valid_json, TypedConfig)
        self.assertEqual(config.integer, 42)
        self.assertEqual(config.string, "text")
        self.assertTrue(config.boolean)
        self.assertEqual(config.float_val, 3.14)
        self.assertEqual(config.list_of_ints, [1, 2, 3])

        # 杂鱼♡～测试部分字段的JSON喵～
        partial_json = '{"integer": 99}'

        # 杂鱼♡～部分字段应该可以正确加载，其他字段使用默认值喵～
        partial_config = jsdc_loads(partial_json, TypedConfig)
        self.assertEqual(partial_config.integer, 99)
        self.assertEqual(partial_config.string, "")
        self.assertFalse(partial_config.boolean)

        print("杂鱼♡～本喵测试加载时类型验证成功了喵～")

    def test_type_validation_on_dump(self) -> None:
        """杂鱼♡～本喵要测试序列化时的类型验证喵～"""

        # 杂鱼♡～测试List[int]类型验证喵～
        @dataclass
        class IntListConfig:
            integers: List[int] = field(default_factory=list)

        # 杂鱼♡～初始化正确类型的数据喵～
        valid_config = IntListConfig(integers=[1, 2, 3, 4, 5])

        # 杂鱼♡～正常情况应该可以序列化喵～
        from ..dumper import jsdc_dump
        jsdc_dump(valid_config, self.temp_path)

        # 杂鱼♡～添加错误类型的数据喵～
        invalid_config = IntListConfig(integers=[1, 2, "3", 4, 5])  # type: ignore

        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_config, self.temp_path)

        print("杂鱼♡～本喵测试序列化时类型验证成功了喵～")

    def test_nested_type_validation(self) -> None:
        """杂鱼♡～本喵要测试嵌套容器的类型验证喵～"""

        @dataclass
        class NestedConfig:
            nested_list: List[List[int]] = field(
                default_factory=lambda: [[1, 2], [3, 4]]
            )
            nested_dict: Dict[str, List[int]] = field(
                default_factory=lambda: {"a": [1, 2], "b": [3, 4]}
            )

        # 杂鱼♡～初始化正确类型的数据喵～
        valid_nested = NestedConfig()

        # 杂鱼♡～正常情况应该可以序列化喵～
        from ..dumper import jsdc_dump
        jsdc_dump(valid_nested, self.temp_path)

        # 杂鱼♡～嵌套列表中添加错误类型喵～
        invalid_nested1 = NestedConfig()
        invalid_nested1.nested_list[0].append("not an int")  # type: ignore

        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_nested1, self.temp_path)

        print("杂鱼♡～本喵测试嵌套类型验证成功了喵～")

    def test_union_type_validation(self) -> None:
        """杂鱼♡～本喵要测试Union类型验证喵～"""

        @dataclass
        class OptionalConfig:
            maybe_int: Optional[int] = None
            int_or_str: Union[int, str] = 42

        # 杂鱼♡～初始化正确类型的数据喵～
        valid_optional1 = OptionalConfig(maybe_int=None)
        valid_optional2 = OptionalConfig(maybe_int=10)
        valid_optional3 = OptionalConfig(int_or_str=99)
        valid_optional4 = OptionalConfig(int_or_str="string")

        # 杂鱼♡～正常情况应该可以序列化喵～
        from ..dumper import jsdc_dump
        jsdc_dump(valid_optional1, self.temp_path)
        jsdc_dump(valid_optional2, self.temp_path)
        jsdc_dump(valid_optional3, self.temp_path)
        jsdc_dump(valid_optional4, self.temp_path)

        # 杂鱼♡～使用不在Union中的类型喵～
        invalid_optional = OptionalConfig()
        invalid_optional.int_or_str = [1, 2, 3]  # type: ignore

        # 序列化应该抛出类型错误
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_optional, self.temp_path)

        print("杂鱼♡～本喵测试Union类型验证成功了喵～")

    def test_collection_type_validation(self) -> None:
        """杂鱼♡～本喵要测试集合类型验证喵～"""

        # 杂鱼♡～测试集合类型喵～
        @dataclass
        class SetConfig:
            int_set: Set[int] = field(default_factory=set)

        # 杂鱼♡～初始化正确类型的数据喵～
        valid_set = SetConfig(int_set={1, 2, 3, 4, 5})

        # 杂鱼♡～正常情况应该可以序列化喵～
        from ..dumper import jsdc_dump
        jsdc_dump(valid_set, self.temp_path)

        # 杂鱼♡～添加错误类型的数据喵～
        invalid_set = SetConfig()
        invalid_set.int_set = {1, "string", 3}  # type: ignore

        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_set, self.temp_path)

        # 杂鱼♡～测试元组类型喵～
        @dataclass
        class TupleConfig:
            fixed_tuple: Tuple[int, str, bool] = field(
                default_factory=lambda: (1, "a", True)
            )
            var_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))

        # 杂鱼♡～初始化正确类型的数据喵～
        valid_tuple = TupleConfig()

        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_tuple, self.temp_path)

        # 杂鱼♡～使用错误类型喵～
        invalid_tuple1 = TupleConfig(
            fixed_tuple=(1, 2, True)  # type: ignore
        )

        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_tuple1, self.temp_path)

        print("杂鱼♡～本喵测试集合类型验证成功了喵～") 