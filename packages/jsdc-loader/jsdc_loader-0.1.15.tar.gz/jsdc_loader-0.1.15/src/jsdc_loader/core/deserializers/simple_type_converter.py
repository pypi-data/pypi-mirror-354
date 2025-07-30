"""杂鱼♡～本喵为你创建的简单类型转换器喵～处理基本类型和特殊类型的反序列化～"""

import datetime
import uuid
from decimal import Decimal
from enum import Enum
from typing import Any

from ..type_checker import cached_get_origin


def convert_simple_type(key: str, value: Any, e_type: Any) -> Any:
    """杂鱼♡～本喵帮你转换简单类型喵～包括基本类型和特殊类型～
    
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
    # 杂鱼♡～处理特殊类型喵～
    if e_type is Any:
        return value
    elif isinstance(e_type, type) and issubclass(e_type, Enum):
        return e_type[value]
    elif e_type == dict or cached_get_origin(e_type) == dict:
        # Handle dict type properly
        return value
    elif e_type == list or cached_get_origin(e_type) == list:
        # Handle list type properly
        return value
    # 杂鱼♡～处理复杂类型喵～如日期、时间等
    elif e_type == datetime.datetime and isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif e_type == datetime.date and isinstance(value, str):
        return datetime.date.fromisoformat(value)
    elif e_type == datetime.time and isinstance(value, str):
        return datetime.time.fromisoformat(value)
    elif e_type == datetime.timedelta and isinstance(value, (int, float)):
        return datetime.timedelta(seconds=value)
    elif e_type == datetime.timedelta and isinstance(value, dict):
        return datetime.timedelta(**value)
    elif e_type == uuid.UUID and isinstance(value, str):
        return uuid.UUID(value)
    elif e_type == Decimal and isinstance(value, (str, int, float)):
        return Decimal(str(value))
    else:
        # 杂鱼♡～对于基本类型，本喵需要先验证类型匹配喵～
        if e_type in (int, float, str, bool):
            if not isinstance(value, e_type):
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～"
                )
            return value
        
        try:
            return e_type(value)
        except TypeError:
            # If it's a typing.Dict or typing.List, just return the value
            if str(e_type).startswith("typing."):
                return value
            raise 