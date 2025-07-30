"""杂鱼♡～本喵为你创建的枚举转换器喵～专门处理Enum类型的反序列化～"""

from enum import Enum
from typing import Any, Type


def convert_enum(key: str, value: Any, enum_type: Type[Enum]) -> Enum:
    """杂鱼♡～本喵帮你把字符串值转换成枚举成员喵～
    
    Args:
        key: 字段名称，用于错误信息
        value: 要转换的值
        enum_type: 目标枚举类型
        
    Returns:
        转换后的枚举实例
        
    Raises:
        ValueError: 当枚举值无效时
    """
    try:
        return enum_type[value]
    except KeyError:
        raise ValueError(f"杂鱼♡～键{key}的枚举值无效喵：{value}～") 