"""杂鱼♡～这是本喵为性能测试创建的模块喵～包含大数据量和性能基准测试～"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .test_base import BaseTestCase


class TestPerformance(BaseTestCase):
    """杂鱼♡～本喵为性能测试创建的测试类喵～"""

    def test_large_json_payload(self) -> None:
        """杂鱼♡～本喵要测试大型JSON负载喵～"""

        @dataclass
        class LargeDataConfig:
            items: List[Dict[str, Any]] = field(default_factory=list)

        # 杂鱼♡～创建大型数据结构喵～
        original_large_config = LargeDataConfig()
        for i in range(1000):  # 创建1000个项目
            item = {
                "id": i,
                "name": f"Item {i}",
                "tags": [f"tag{j}" for j in range(10)],  # 每个项目10个标签
                "properties": {
                    f"prop{k}": f"value{k}" for k in range(5)
                },  # 每个项目5个属性
            }
            original_large_config.items.append(item)

        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_large_config, LargeDataConfig)

        # 杂鱼♡～验证项目数量喵～
        self.assertEqual(len(loaded_config.items), 1000)
        # 验证第一个和最后一个项目
        self.assertEqual(loaded_config.items[0]["id"], 0)
        self.assertEqual(loaded_config.items[999]["id"], 999)
        # 验证结构完整性
        self.assertEqual(len(loaded_config.items[500]["tags"]), 10)
        self.assertEqual(len(loaded_config.items[500]["properties"]), 5)

        print("杂鱼♡～本喵测试大型JSON负载成功了喵～")

    def test_performance_benchmark(self) -> None:
        """杂鱼♡～本喵要测试性能基准喵～"""

        @dataclass
        class SimpleItem:
            id: int = 0
            name: str = ""
            value: float = 0.0

        @dataclass
        class PerformanceConfig:
            items: List[SimpleItem] = field(default_factory=list)
            metadata: Dict[str, Any] = field(default_factory=dict)

        # 杂鱼♡～创建一个包含许多项的大型配置喵～
        original_large_config = PerformanceConfig()
        for i in range(1000):
            original_large_config.items.append(
                SimpleItem(id=i, name=f"Item {i}", value=float(i) * 1.5)
            )

        original_large_config.metadata = {
            "created_at": "2023-01-01T00:00:00",
            "version": "1.0.0",
            "tags": ["performance", "test", "jsdc"],
            "nested": {"level1": {"level2": {"level3": [i for i in range(100)]}}},
        }

        # 杂鱼♡～测量序列化性能喵～
        from ..dumper import jsdc_dump, jsdc_dumps
        from ..loader import jsdc_load, jsdc_loads
        
        start_time = time.time()
        jsdc_dump(original_large_config, self.temp_path)
        serialize_time = time.time() - start_time

        # 杂鱼♡～测量反序列化性能喵～
        start_time = time.time()
        loaded_config = jsdc_load(self.temp_path, PerformanceConfig)
        deserialize_time = time.time() - start_time

        # 杂鱼♡～记录性能指标喵～
        print(f"\n杂鱼♡～性能测试结果喵～")
        print(f"序列化时间: {serialize_time:.6f} 秒喵～")
        print(f"反序列化时间: {deserialize_time:.6f} 秒喵～")
        print(f"项目数量: {len(loaded_config.items)} 个喵～")

        # 杂鱼♡～确认数据完整性喵～
        self.assertEqual(len(loaded_config.items), 1000)
        self.assertEqual(loaded_config.items[0].id, 0)
        self.assertEqual(loaded_config.items[999].id, 999)
        self.assertEqual(loaded_config.items[500].name, "Item 500")
        self.assertEqual(loaded_config.items[500].value, 750.0)  # 500 * 1.5 = 750.0

        # 测试字符串序列化的性能
        start_time = time.time()
        json_str = jsdc_dumps(original_large_config)
        string_serialize_time = time.time() - start_time

        # 测试字符串反序列化的性能
        start_time = time.time()
        loaded_from_str = jsdc_loads(json_str, PerformanceConfig)
        string_deserialize_time = time.time() - start_time

        # 记录额外的性能指标
        print(f"字符串序列化时间: {string_serialize_time:.6f} 秒喵～")
        print(f"字符串反序列化时间: {string_deserialize_time:.6f} 秒喵～")
        print(f"JSON字符串长度: {len(json_str)} 字符喵～")

        # 确认从字符串加载的数据完整性
        self.assertEqual(len(loaded_from_str.items), 1000)
        self.assertEqual(loaded_from_str.items[0].id, 0)

        print("杂鱼♡～本喵测试性能基准成功了喵～") 