"""杂鱼♡～本喵为你创建的反序列化基础模块喵～这里是核心的转换逻辑～"""

from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Union

from ..compat import (
    create_pydantic_from_dict,
    is_pydantic_model,
)
from ..types import T
from ..type_checker import cached_get_origin, cached_get_args
from ..validator import get_cached_type_hints
from .enum_converter import convert_enum
from .union_converter import convert_union_type
from .container_converters import convert_dict_type, convert_tuple_type
from .simple_type_converter import convert_simple_type


def convert_value(key: str, value: Any, e_type: Any) -> Any:
    """杂鱼♡～本喵的核心转换函数喵～把JSON值转换为指定类型～
    
    Args:
        key: 字段名称，用于错误信息
        value: 要转换的值
        e_type: 目标类型
        
    Returns:
        转换后的值
        
    Raises:
        TypeError: 当类型转换失败时
        ValueError: 当值无效时
    """
    # 杂鱼♡～处理None值和Any类型喵～早期返回可以提高性能～
    if e_type is Any:
        return value
    
    if value is None:
        origin = cached_get_origin(e_type)
        if origin is Union and type(None) in cached_get_args(e_type):
            return None
        # 如果不是Union类型但值是None，让它继续处理以抛出适当的错误
    
    # 杂鱼♡～先检查常见的简单类型，提早返回喵～
    value_type = type(value)
    if e_type is value_type or (e_type in (int, float, str, bool) and value_type is e_type):
        return value

    # 杂鱼♡～缓存origin和args避免重复计算喵～
    origin = cached_get_origin(e_type)
    args = cached_get_args(e_type) if origin else None

    # 杂鱼♡～处理容器类型喵～优化顺序以处理最常见的类型～
    if origin is list or e_type == list:
        if args and (is_dataclass(args[0]) or is_pydantic_model(args[0])):
            return [
                (
                    convert_dict_to_dataclass(item, args[0])
                    if is_dataclass(args[0])
                    else create_pydantic_from_dict(args[0], item)
                )
                for item in value
            ]
        elif args:
            return [
                convert_value(f"{key}[{i}]", item, args[0])
                for i, item in enumerate(value)
            ]
        return value
    elif origin is dict or e_type == dict:
        return convert_dict_type(key, value, e_type)
    elif origin is set or e_type is set:
        if isinstance(value, list):
            if args:
                element_type = args[0]
                return {convert_value(f"{key}[*]", item, element_type) for item in value}
            else:
                return set(value)
        return value
    elif origin is tuple or e_type is tuple:
        if isinstance(value, list):
            return convert_tuple_type(key, value, e_type)
        return value
    elif origin is Union:
        return convert_union_type(key, value, e_type)
    elif isinstance(e_type, type) and issubclass(e_type, Enum):
        return convert_enum(key, value, e_type)
    elif is_dataclass(e_type):
        return convert_dict_to_dataclass(value, e_type)
    elif is_pydantic_model(e_type):
        # 杂鱼♡～处理 Pydantic 模型喵～
        return create_pydantic_from_dict(e_type, value)
    else:
        return convert_simple_type(key, value, e_type)


def convert_dict_to_dataclass(data: dict, cls: T) -> T:
    """杂鱼♡～本喵帮你把字典转换为dataclass实例喵～
    
    Args:
        data: 源字典数据
        cls: 目标dataclass或Pydantic模型类
        
    Returns:
        转换后的实例
        
    Raises:
        ValueError: 当数据为空或字段未知时
    """
    if not data:
        raise ValueError("杂鱼♡～空的数据字典喵！～")

    if is_pydantic_model(cls):
        # 杂鱼♡～使用兼容层来创建 Pydantic 模型喵～
        return create_pydantic_from_dict(cls, data)

    # 杂鱼♡～无论是否为frozen dataclass，都使用构造函数方式创建实例喵～这样更安全～
    init_kwargs = {}
    t_hints = get_cached_type_hints(cls)

    for key, value in data.items():
        if key in t_hints:
            e_type = t_hints.get(key)
            if e_type is not None:
                init_kwargs[key] = convert_value(key, value, e_type)
        else:
            raise ValueError(f"杂鱼♡～未知的数据键喵：{key}～")

    return cls(**init_kwargs) 