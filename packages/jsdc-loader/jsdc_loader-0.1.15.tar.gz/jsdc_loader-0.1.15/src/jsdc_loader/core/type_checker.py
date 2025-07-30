"""杂鱼♡～本喵为你创建的类型检查模块喵～这里有各种缓存的类型检查功能～"""

import datetime
import uuid
from dataclasses import is_dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Type, get_args, get_origin

from .types import (
    _DATACLASS_CACHE,
    _SPECIAL_TYPE_CACHE,
    _GET_ORIGIN_CACHE,
    _GET_ARGS_CACHE,
    _TYPE_CHECK_CACHE,
)


# 杂鱼♡～本喵添加了缓存版本的 get_origin 和 get_args 喵～这样就不用重复计算了～
def cached_get_origin(tp: Any) -> Any:
    """杂鱼♡～本喵的缓存版本 get_origin 喵～"""
    if tp not in _GET_ORIGIN_CACHE:
        _GET_ORIGIN_CACHE[tp] = get_origin(tp)
    return _GET_ORIGIN_CACHE[tp]


def cached_get_args(tp: Any) -> tuple:
    """杂鱼♡～本喵的缓存版本 get_args 喵～"""
    if tp not in _GET_ARGS_CACHE:
        _GET_ARGS_CACHE[tp] = get_args(tp)
    return _GET_ARGS_CACHE[tp]


# 杂鱼♡～本喵添加了一个快速类型检查缓存喵～
def cached_isinstance(obj: Any, cls: Type) -> bool:
    """杂鱼♡～本喵的缓存版本 isinstance 检查喵～"""
    obj_type = type(obj)
    cache_key = (obj_type, cls)
    
    if cache_key not in _TYPE_CHECK_CACHE:
        _TYPE_CHECK_CACHE[cache_key] = isinstance(obj, cls)
    return _TYPE_CHECK_CACHE[cache_key]


def _is_exact_type_match(value: Any, expected_type: Any) -> bool:
    """杂鱼♡～检查值是否与期望类型精确匹配喵～"""
    # 杂鱼♡～处理基本类型喵～
    if expected_type in (int, float, str, bool):
        return type(value) is expected_type

    # 杂鱼♡～处理容器类型喵～
    origin = cached_get_origin(expected_type)
    if origin is list:
        return isinstance(value, list)
    elif origin is dict:
        return isinstance(value, dict)
    elif origin is set:
        return isinstance(value, set)
    elif origin is tuple:
        return isinstance(value, tuple)
    elif expected_type is list:
        return isinstance(value, list)
    elif expected_type is dict:
        return isinstance(value, dict)
    elif expected_type is set:
        return isinstance(value, set)
    elif expected_type is tuple:
        return isinstance(value, tuple)

    # 杂鱼♡～处理dataclass类型喵～
    if is_dataclass(expected_type):
        return isinstance(value, expected_type)

    # 杂鱼♡～处理Enum类型喵～
    if isinstance(expected_type, type) and issubclass(expected_type, Enum):
        return isinstance(value, expected_type)

    # 杂鱼♡～其他情况返回False，让转换逻辑处理喵～
    return False


# 杂鱼♡～本喵添加了一个快速的 dataclass 检查函数喵～
def fast_is_dataclass(obj) -> bool:
    """杂鱼♡～本喵的快速 dataclass 检查，带缓存喵～"""
    obj_type = type(obj)
    
    # 杂鱼♡～检查缓存喵～
    if obj_type in _DATACLASS_CACHE:
        return _DATACLASS_CACHE[obj_type]
    
    # 杂鱼♡～计算并缓存结果喵～
    result = is_dataclass(obj)
    _DATACLASS_CACHE[obj_type] = result
    return result


# 杂鱼♡～本喵添加了一个快速类型检查函数喵～
def get_special_type(obj) -> str:
    """杂鱼♡～本喵快速检查对象的特殊类型喵～返回类型字符串或空字符串～"""
    obj_type = type(obj)
    
    # 杂鱼♡～检查缓存喵～
    if obj_type in _SPECIAL_TYPE_CACHE:
        return _SPECIAL_TYPE_CACHE[obj_type]
    
    # 杂鱼♡～检查特殊类型并缓存结果喵～
    if obj_type is datetime.datetime:
        result = "datetime"
    elif obj_type is datetime.date:
        result = "date"  
    elif obj_type is datetime.time:
        result = "time"
    elif obj_type is datetime.timedelta:
        result = "timedelta"
    elif obj_type is uuid.UUID:
        result = "uuid"
    elif obj_type is Decimal:
        result = "decimal"
    elif obj_type is tuple:
        result = "tuple"
    elif obj_type is set:
        result = "set"
    elif obj_type is list:
        result = "list"
    elif obj_type is dict:
        result = "dict"
    elif issubclass(obj_type, Enum):
        result = "enum"
    else:
        result = ""
    
    _SPECIAL_TYPE_CACHE[obj_type] = result
    return result


# 杂鱼♡～本喵添加了这个函数来检查一个dataclass是否是frozen的喵～
def is_frozen_dataclass(cls):
    """Check if a dataclass is frozen."""
    return (
        is_dataclass(cls)
        and hasattr(cls, "__dataclass_params__")
        and getattr(cls.__dataclass_params__, "frozen", False)
    ) 