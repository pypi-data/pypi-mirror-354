"""杂鱼♡～这是本喵为基础功能创建的测试模块喵～包含最基本的序列化和反序列化测试～"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional

from .test_base import BaseTestCase


class TestBasicFunctionality(BaseTestCase):
    """杂鱼♡～本喵为基础功能创建的测试类喵～"""

    def test_basic_dataclass_serialization(self) -> None:
        """杂鱼♡～本喵要测试最基础的dataclass序列化/反序列化喵～"""

        @dataclass
        class DatabaseConfig:
            host: str = "localhost"
            port: int = 3306
            user: str = "root"
            password: str = "password"
            ips: List[str] = field(default_factory=lambda: ["127.0.0.1"])
            primary_user: Optional[str] = field(default_factory=lambda: None)

        # 杂鱼♡～创建测试数据喵～
        original_config = DatabaseConfig()
        
        # 杂鱼♡～执行往返测试喵～
        loaded_config = self.assert_serialization_roundtrip(original_config, DatabaseConfig)

        # 杂鱼♡～验证所有字段都正确恢复喵～
        self.assertEqual(original_config.host, loaded_config.host)
        self.assertEqual(original_config.port, loaded_config.port)
        self.assertEqual(original_config.user, loaded_config.user)
        self.assertEqual(original_config.password, loaded_config.password)
        self.assertEqual(original_config.ips, loaded_config.ips)
        self.assertEqual(original_config.primary_user, loaded_config.primary_user)

        print("杂鱼♡～本喵测试基础dataclass序列化成功了喵～")

    def test_enum_serialization(self) -> None:
        """杂鱼♡～本喵要测试枚举的序列化/反序列化喵～"""

        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass
        class UserConfig:
            name: str = "John Doe"
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ["read"])

        # 杂鱼♡～创建测试数据喵～
        original_user = UserConfig()
        
        # 杂鱼♡～执行往返测试喵～
        loaded_user = self.assert_serialization_roundtrip(original_user, UserConfig)

        # 杂鱼♡～验证枚举值正确恢复喵～
        self.assertEqual(original_user.name, loaded_user.name)
        self.assertEqual(original_user.age, loaded_user.age)
        self.assertEqual(original_user.married, loaded_user.married)
        self.assertEqual(original_user.user_type, loaded_user.user_type)
        self.assertEqual(original_user.roles, loaded_user.roles)
        
        # 杂鱼♡～确保枚举类型正确喵～
        self.assertIsInstance(loaded_user.user_type, UserType)

        print("杂鱼♡～本喵测试枚举序列化成功了喵～")

    def test_nested_dataclasses(self) -> None:
        """杂鱼♡～本喵要测试嵌套的数据类序列化喵～"""

        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass
        class UserConfig:
            name: str = "John Doe"
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ["read"])

        @dataclass
        class DatabaseConfig:
            host: str = "localhost"
            port: int = 3306
            user: str = "root"
            password: str = "password"
            ips: List[str] = field(default_factory=lambda: ["127.0.0.1"])
            primary_user: Optional[str] = field(default_factory=lambda: None)

        @dataclass
        class AppConfig:
            user: UserConfig = field(default_factory=lambda: UserConfig())
            database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
            version: str = "1.0.0"
            debug: bool = False
            settings: Dict[str, str] = field(default_factory=lambda: {"theme": "dark"})

        # 杂鱼♡～创建并修改测试数据喵～
        original_app = AppConfig()
        original_app.user.roles.append("write")
        original_app.database.ips.extend(["192.168.1.1", "10.0.0.1"])
        original_app.settings["language"] = "en"

        # 杂鱼♡～执行往返测试喵～
        loaded_app = self.assert_serialization_roundtrip(original_app, AppConfig)

        # 杂鱼♡～验证嵌套结构正确恢复喵～
        self.assertEqual(loaded_app.user.roles, ["read", "write"])
        self.assertEqual(
            loaded_app.database.ips, ["127.0.0.1", "192.168.1.1", "10.0.0.1"]
        )
        self.assertEqual(loaded_app.settings, {"theme": "dark", "language": "en"})
        self.assertEqual(loaded_app.version, "1.0.0")
        self.assertEqual(loaded_app.debug, False)

        print("杂鱼♡～本喵测试嵌套数据类序列化成功了喵～")

    def test_string_serialization(self) -> None:
        """杂鱼♡～本喵要测试字符串序列化喵～"""

        @dataclass
        class Config:
            name: str = "test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])

        # 杂鱼♡～创建测试对象喵～
        original_config = Config(name="string_test", values=[5, 6, 7, 8])

        # 杂鱼♡～执行字符串往返测试喵～
        loaded_config = self.assert_string_serialization_roundtrip(original_config, Config)

        # 杂鱼♡～验证值正确恢复喵～
        self.assertEqual(original_config.name, loaded_config.name)
        self.assertEqual(original_config.values, loaded_config.values)

        print("杂鱼♡～本喵测试字符串序列化成功了喵～")

    def test_error_handling(self) -> None:
        """杂鱼♡～本喵要测试错误处理喵～"""

        @dataclass
        class DatabaseConfig:
            host: str = "localhost"
            port: int = 3306

        # 杂鱼♡～测试不存在的文件喵～
        with self.assertRaises(FileNotFoundError):
            from ..loader import jsdc_load
            jsdc_load("nonexistent.json", DatabaseConfig)

        # 杂鱼♡～测试空输入喵～
        with self.assertRaises(ValueError):
            from ..loader import jsdc_loads
            jsdc_loads("", DatabaseConfig)

        # 杂鱼♡～测试无效JSON喵～
        with self.assertRaises(ValueError):
            from ..loader import jsdc_loads
            jsdc_loads("{invalid json}", DatabaseConfig)

        # 杂鱼♡～测试无效缩进喵～
        with self.assertRaises(ValueError):
            from ..dumper import jsdc_dump
            jsdc_dump(DatabaseConfig(), self.temp_path, indent=-1)

        print("杂鱼♡～本喵测试错误处理成功了喵～")

    def test_inheritance(self) -> None:
        """杂鱼♡～本喵要测试继承关系的序列化喵～"""

        @dataclass
        class BaseConfig:
            name: str = "base"
            version: str = "1.0.0"

        @dataclass
        class DerivedConfig(BaseConfig):
            name: str = "derived"  # 覆盖基类字段
            extra_field: str = "extra"

        @dataclass
        class Container:
            base: BaseConfig = field(default_factory=lambda: BaseConfig())
            derived: DerivedConfig = field(default_factory=lambda: DerivedConfig())

        # 杂鱼♡～创建并修改测试数据喵～
        original_container = Container()
        original_container.base.version = "2.0.0"
        original_container.derived.extra_field = "custom_value"

        # 杂鱼♡～执行往返测试喵～
        loaded_container = self.assert_serialization_roundtrip(original_container, Container)

        # 杂鱼♡～验证基类和派生类的字段喵～
        self.assertEqual(loaded_container.base.name, "base")
        self.assertEqual(loaded_container.base.version, "2.0.0")
        self.assertEqual(loaded_container.derived.name, "derived")
        self.assertEqual(loaded_container.derived.version, "1.0.0")
        self.assertEqual(loaded_container.derived.extra_field, "custom_value")

        print("杂鱼♡～本喵测试继承关系序列化成功了喵～") 