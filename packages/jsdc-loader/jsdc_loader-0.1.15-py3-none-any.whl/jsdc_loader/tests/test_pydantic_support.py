"""杂鱼♡～这是本喵为Pydantic支持创建的测试模块喵～包含BaseModel的序列化和反序列化测试～"""

from dataclasses import dataclass, field
from typing import Dict, List

from .test_base import BaseTestCase, HAS_PYDANTIC

if HAS_PYDANTIC:
    from pydantic import BaseModel


class TestPydanticSupport(BaseTestCase):
    """杂鱼♡～本喵为Pydantic支持创建的测试类喵～"""

    def test_pydantic_models(self) -> None:
        """杂鱼♡～本喵要测试Pydantic模型喵～"""
        
        # 杂鱼♡～如果没有pydantic，本喵就跳过这个测试喵～
        if not HAS_PYDANTIC:
            self.skipTest("杂鱼♡～没有pydantic，本喵跳过这个测试喵～")

        class ServerConfig(BaseModel):
            name: str = "main"
            port: int = 8080
            ssl: bool = True
            headers: Dict[str, str] = {"Content-Type": "application/json"}

        class ApiConfig(BaseModel):
            servers: List[ServerConfig] = []
            timeout: int = 30
            retries: int = 3

        # 杂鱼♡～创建测试数据喵～
        original_api_config = ApiConfig()
        original_api_config.servers.append(ServerConfig(name="backup", port=8081))
        original_api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))

        # 杂鱼♡～执行往返测试喵～
        loaded_api = self.assert_serialization_roundtrip(original_api_config, ApiConfig)

        # 杂鱼♡～验证Pydantic模型正确恢复喵～
        self.assertEqual(len(loaded_api.servers), 2)
        self.assertEqual(loaded_api.servers[0].name, "backup")
        self.assertEqual(loaded_api.servers[1].port, 8082)
        self.assertFalse(loaded_api.servers[1].ssl)

        print("杂鱼♡～本喵测试Pydantic模型成功了喵～")

    def test_mixed_dataclass_pydantic(self) -> None:
        """杂鱼♡～本喵要测试dataclass和Pydantic模型混合使用喵～"""
        
        # 杂鱼♡～如果没有pydantic，本喵就跳过这个测试喵～
        if not HAS_PYDANTIC:
            self.skipTest("杂鱼♡～没有pydantic，本喵跳过这个测试喵～")

        class PydanticConfig(BaseModel):
            name: str = "pydantic"
            enabled: bool = True

        @dataclass
        class DataclassConfig:
            name: str = "dataclass"
            pydantic_part: PydanticConfig = field(default_factory=lambda: PydanticConfig())

        # 杂鱼♡～创建混合配置喵～
        original_mixed = DataclassConfig()
        original_mixed.pydantic_part.name = "custom_pydantic"
        original_mixed.pydantic_part.enabled = False

        # 杂鱼♡～执行往返测试喵～
        loaded_mixed = self.assert_serialization_roundtrip(original_mixed, DataclassConfig)

        # 杂鱼♡～验证混合类型正确恢复喵～
        self.assertEqual(loaded_mixed.name, "dataclass")
        self.assertEqual(loaded_mixed.pydantic_part.name, "custom_pydantic")
        self.assertFalse(loaded_mixed.pydantic_part.enabled)

        print("杂鱼♡～本喵测试混合dataclass和Pydantic模型成功了喵～") 