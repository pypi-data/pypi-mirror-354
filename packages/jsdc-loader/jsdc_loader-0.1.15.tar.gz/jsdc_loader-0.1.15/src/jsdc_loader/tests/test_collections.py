"""杂鱼♡～这是本喵为集合类型创建的测试模块喵～包含List、Set、Dict、Tuple等集合类型的测试～"""

import collections
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple

from .test_base import BaseTestCase


class TestCollections(BaseTestCase):
    """杂鱼♡～本喵为集合类型创建的测试类喵～"""

    def test_empty_collections(self) -> None:
        """杂鱼♡～本喵要测试空集合的情况喵～"""

        @dataclass
        class EmptyCollections:
            empty_list: List[str] = field(default_factory=list)
            empty_dict: Dict[str, int] = field(default_factory=dict)
            empty_set: Set[int] = field(default_factory=set)
            empty_nested_list: List[List[int]] = field(default_factory=lambda: [])

        # 杂鱼♡～创建空集合对象喵～
        original_empty = EmptyCollections()

        # 杂鱼♡～执行往返测试喵～
        loaded_empty = self.assert_serialization_roundtrip(original_empty, EmptyCollections)

        # 杂鱼♡～验证空集合正确恢复喵～
        self.assertEqual(loaded_empty.empty_list, [])
        self.assertEqual(loaded_empty.empty_dict, {})
        self.assertEqual(loaded_empty.empty_set, set())
        self.assertEqual(loaded_empty.empty_nested_list, [])

        print("杂鱼♡～本喵测试空集合成功了喵～")

    def test_tuple_types(self) -> None:
        """杂鱼♡～本喵要测试元组类型喵～"""

        @dataclass
        class ConfigWithTuples:
            simple_tuple: Tuple[int, str, bool] = field(
                default_factory=lambda: (1, "test", True)
            )
            int_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
            empty_tuple: Tuple = field(default_factory=tuple)
            nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]] = field(
                default_factory=lambda: ((1, 2), ("a", "b"))
            )

        # 杂鱼♡～创建测试对象喵～
        original_config = ConfigWithTuples()

        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_config, ConfigWithTuples)

        # 杂鱼♡～验证元组类型正确恢复喵～
        self.assertEqual(loaded_config.simple_tuple, (1, "test", True))
        self.assertEqual(loaded_config.int_tuple, (1, 2, 3))
        self.assertEqual(loaded_config.empty_tuple, ())
        self.assertEqual(loaded_config.nested_tuple, ((1, 2), ("a", "b")))

        print("杂鱼♡～本喵测试元组类型成功了喵～")

    def test_hashable_model_set(self) -> None:
        """杂鱼♡～本喵要测试可哈希模型的集合喵～"""

        @dataclass(frozen=True)  # 让这个数据类不可变，以便可以哈希
        class Model:
            base_url: str = ""
            api_key: str = ""
            model: str = ""

            def __hash__(self) -> int:
                return hash((self.base_url, self.api_key, self.model))

            def __eq__(self, other: object) -> bool:
                if not isinstance(other, Model):
                    return NotImplemented
                return (self.base_url, self.api_key, self.model) == (
                    other.base_url,
                    other.api_key,
                    other.model,
                )

        @dataclass
        class ModelList:
            models: Set[Model] = field(default_factory=lambda: set())

        # 杂鱼♡～创建测试数据喵～
        model1 = Model(
            base_url="https://api1.example.com", api_key="key1", model="gpt-4"
        )
        model2 = Model(
            base_url="https://api2.example.com", api_key="key2", model="gpt-3.5"
        )
        model3 = Model(
            base_url="https://api3.example.com", api_key="key3", model="llama-3"
        )

        original_model_list = ModelList()
        original_model_list.models.add(model1)
        original_model_list.models.add(model2)
        original_model_list.models.add(model3)

        # 杂鱼♡～测试相同模型的哈希值和相等性喵～
        duplicate_model = Model(
            base_url="https://api1.example.com", api_key="key1", model="gpt-4"
        )
        original_model_list.models.add(duplicate_model)  # 这个不应该增加集合的大小

        self.assertEqual(len(original_model_list.models), 3)  # 验证重复模型没有被添加

        # 杂鱼♡～执行往返测试喵～
        loaded_model_list = self.assert_serialization_roundtrip(original_model_list, ModelList)

        # 杂鱼♡～验证集合大小喵～
        self.assertEqual(len(loaded_model_list.models), 3)

        # 杂鱼♡～验证所有模型都被正确反序列化喵～
        loaded_models = sorted(loaded_model_list.models, key=lambda m: m.base_url)
        original_models = sorted(original_model_list.models, key=lambda m: m.base_url)

        for i in range(len(original_models)):
            self.assertEqual(loaded_models[i].base_url, original_models[i].base_url)
            self.assertEqual(loaded_models[i].api_key, original_models[i].api_key)
            self.assertEqual(loaded_models[i].model, original_models[i].model)

        print("杂鱼♡～本喵测试可哈希模型集合成功了喵～")

    def test_custom_containers(self) -> None:
        """杂鱼♡～本喵要测试自定义容器类型喵～"""

        @dataclass
        class CustomContainersConfig:
            # 杂鱼♡～将类型声明为普通dict，但初始化时使用特殊容器喵～
            ordered_dict: Dict[str, int] = field(
                default_factory=lambda: collections.OrderedDict(
                    [("a", 1), ("b", 2), ("c", 3)]
                )
            )
            default_dict: Dict[str, int] = field(
                default_factory=lambda: collections.defaultdict(int, {"x": 10, "y": 20})
            )
            counter: Dict[str, int] = field(
                default_factory=lambda: collections.Counter(["a", "b", "a", "c", "a"])
            )

        # 杂鱼♡～创建配置并添加一些值喵～
        original_config = CustomContainersConfig()
        original_config.ordered_dict["d"] = 4  # type: ignore
        original_config.default_dict["z"] = 30  # type: ignore
        original_config.counter.update(["d", "e", "d"])  # type: ignore

        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_config, CustomContainersConfig)

        # 杂鱼♡～验证序列化和反序列化后的值（使用dict比较）喵～
        self.assertEqual(dict(original_config.ordered_dict), dict(loaded_config.ordered_dict))  # type: ignore
        self.assertEqual(dict(original_config.default_dict), dict(loaded_config.default_dict))  # type: ignore
        self.assertEqual(dict(original_config.counter), dict(loaded_config.counter))  # type: ignore

        # 杂鱼♡～验证字典内容喵～
        self.assertEqual(
            dict(loaded_config.ordered_dict), {"a": 1, "b": 2, "c": 3, "d": 4}
        )
        self.assertEqual(dict(loaded_config.default_dict), {"x": 10, "y": 20, "z": 30})
        self.assertEqual(
            dict(loaded_config.counter), {"a": 3, "b": 1, "c": 1, "d": 2, "e": 1}
        )

        print("杂鱼♡～本喵测试自定义容器类型成功了喵～")

    def test_dict_key_types_support(self) -> None:
        """杂鱼♡～本喵要专门测试各种字典键类型的支持喵～"""

        # 杂鱼♡～测试整数键字典喵～
        @dataclass
        class IntKeyConfig:
            int_to_str: Dict[int, str] = field(default_factory=dict)
            int_to_int: Dict[int, int] = field(default_factory=dict)

        original_int_config = IntKeyConfig()
        original_int_config.int_to_str = {1: "one", 2: "two", 42: "answer"}
        original_int_config.int_to_int = {10: 100, 20: 200}

        loaded_int = self.assert_serialization_roundtrip(original_int_config, IntKeyConfig)

        self.assertEqual(loaded_int.int_to_str, {1: "one", 2: "two", 42: "answer"})
        self.assertEqual(loaded_int.int_to_int, {10: 100, 20: 200})

        # 杂鱼♡～测试浮点数键字典喵～
        @dataclass
        class FloatKeyConfig:
            float_to_str: Dict[float, str] = field(default_factory=dict)

        original_float_config = FloatKeyConfig()
        original_float_config.float_to_str = {1.5: "one and half", 3.14: "pi", 2.718: "e"}

        loaded_float = self.assert_serialization_roundtrip(original_float_config, FloatKeyConfig)

        self.assertEqual(
            loaded_float.float_to_str, {1.5: "one and half", 3.14: "pi", 2.718: "e"}
        )

        # 杂鱼♡～测试布尔键字典喵～
        @dataclass
        class BoolKeyConfig:
            bool_to_str: Dict[bool, str] = field(default_factory=dict)

        original_bool_config = BoolKeyConfig()
        original_bool_config.bool_to_str = {True: "yes", False: "no"}

        loaded_bool = self.assert_serialization_roundtrip(original_bool_config, BoolKeyConfig)

        self.assertEqual(loaded_bool.bool_to_str, {True: "yes", False: "no"})

        print("杂鱼♡～本喵测试各种字典键类型支持成功了喵～")

    def test_collection_type_consistency(self) -> None:
        """杂鱼♡～本喵要测试集合类型一致性喵～"""

        @dataclass
        class CollectionConfig:
            int_list: List[int] = field(default_factory=list)
            str_set: Set[str] = field(default_factory=set)
            str_int_dict: Dict[str, int] = field(default_factory=dict)
            nested_list: List[List[str]] = field(default_factory=list)

        # 杂鱼♡～创建具有各种集合的配置喵～
        original_config = CollectionConfig()
        original_config.int_list = [1, 2, 3, 2, 1]  # 杂鱼♡～有重复元素喵～
        original_config.str_set = {"apple", "banana", "apple"}  # 杂鱼♡～集合会自动去重喵～
        original_config.str_int_dict = {"one": 1, "two": 2, "three": 3}
        original_config.nested_list = [["a", "b"], ["c", "d"], []]  # 杂鱼♡～包含空列表喵～

        # 杂鱼♡～执行往返测试喵～
        loaded = self.assert_serialization_roundtrip(original_config, CollectionConfig)

        # 杂鱼♡～验证列表（保持顺序和重复）喵～
        self.assertEqual(loaded.int_list, [1, 2, 3, 2, 1])

        # 杂鱼♡～验证集合（去重但可能顺序不同）喵～
        self.assertEqual(loaded.str_set, {"apple", "banana"})

        # 杂鱼♡～验证字典喵～
        self.assertEqual(loaded.str_int_dict, {"one": 1, "two": 2, "three": 3})

        # 杂鱼♡～验证嵌套列表喵～
        self.assertEqual(loaded.nested_list, [["a", "b"], ["c", "d"], []])

        print("杂鱼♡～本喵测试集合类型一致性成功了喵～") 