"""杂鱼♡～本喵为你创建的序列化基础模块喵～这里是核心的序列化逻辑～"""

import datetime
import uuid
from decimal import Decimal
from enum import Enum
from typing import Any

from ..compat import is_pydantic_instance, pydantic_to_dict
from ..type_checker import (
    cached_get_origin,
    cached_get_args,
    fast_is_dataclass,
    get_special_type,
)
from ..validator import get_cached_type_hints, validate_type


def convert_dataclass_to_dict(
    obj: Any, parent_key: str = "", parent_type: Any = None
) -> Any:
    """杂鱼♡～本喵帮你把dataclass实例转换为字典喵～支持各种复杂类型～
    
    Args:
        obj: 要转换的对象
        parent_key: 父级键名，用于错误信息
        parent_type: 父级类型，用于类型验证
        
    Returns:
        转换后的字典或值
        
    Raises:
        TypeError: 当类型验证失败时
    """
    if obj is None:
        return None

    # 杂鱼♡～快速检查基本类型，直接返回喵～
    obj_type = type(obj)
    if obj_type in (int, float, str, bool):
        return obj

    # 杂鱼♡～本喵用快速类型检查来减少 isinstance 调用喵～
    special_type = get_special_type(obj)
    
    if special_type == "datetime":
        return obj.isoformat()
    elif special_type == "date":
        return obj.isoformat()
    elif special_type == "time":
        return obj.isoformat()
    elif special_type == "timedelta":
        return obj.total_seconds()
    elif special_type == "uuid":
        return str(obj)
    elif special_type == "decimal":
        return str(obj)
    elif special_type == "tuple":
        # 杂鱼♡～对于元组，转换为列表返回喵～
        return [
            convert_dataclass_to_dict(
                item,
                f"{parent_key}[]",
                (
                    cached_get_args(parent_type)[0]
                    if parent_type and cached_get_args(parent_type)
                    else None
                ),
            )
            for item in obj
        ]
    elif special_type == "enum":
        return obj.name
    elif special_type == "set":
        # 杂鱼♡～需要检查集合中元素的类型喵～
        element_type = None
        if parent_type and cached_get_origin(parent_type) is set and cached_get_args(parent_type):
            element_type = cached_get_args(parent_type)[0]

        result = []
        for i, item in enumerate(obj):
            # 杂鱼♡～为了测试能通过，本喵还是要验证元素类型喵～
            if element_type:
                item_key = f"{parent_key or 'set'}[{i}]"
                try:
                    validate_type(item_key, item, element_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时集合元素类型验证失败喵：{item_key} {str(e)}～"
                    )

            result.append(
                convert_dataclass_to_dict(item, f"{parent_key}[{i}]", element_type)
            )

        return result
    elif special_type == "list":
        # 杂鱼♡～需要检查列表中元素的类型喵～
        element_type = None
        if parent_type and cached_get_origin(parent_type) is list and cached_get_args(parent_type):
            element_type = cached_get_args(parent_type)[0]

        result = []
        for i, item in enumerate(obj):
            # 杂鱼♡～为了测试能通过，本喵还是要验证元素类型喵～
            if element_type:
                item_key = f"{parent_key or 'list'}[{i}]"
                try:
                    validate_type(item_key, item, element_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时列表元素类型验证失败喵：{item_key} {str(e)}～"
                    )

            result.append(
                convert_dataclass_to_dict(item, f"{parent_key}[{i}]", element_type)
            )

        return result
    elif special_type == "dict":
        # 杂鱼♡～需要检查字典中键和值的类型喵～
        key_type, val_type = None, None
        if (
            parent_type
            and cached_get_origin(parent_type) is dict
            and len(cached_get_args(parent_type)) == 2
        ):
            key_type, val_type = cached_get_args(parent_type)

        result = {}
        for k, v in obj.items():
            # 杂鱼♡～为了测试能通过，本喵还是要验证键值类型喵～
            if key_type:
                key_name = f"{parent_key or 'dict'}.key"
                try:
                    validate_type(key_name, k, key_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时字典键类型验证失败喵：{key_name} {str(e)}～"
                    )

            if val_type:
                val_key = f"{parent_key or 'dict'}[{k}]"
                try:
                    validate_type(val_key, v, val_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时字典值类型验证失败喵：{val_key} {str(e)}～"
                    )

            # 杂鱼♡～将键转换为字符串以支持JSON序列化喵～
            # JSON只支持字符串键，所以本喵需要将其他类型的键转换为字符串～
            json_key = str(k)
            result[json_key] = convert_dataclass_to_dict(
                v, f"{parent_key}[{k}]", val_type
            )

        return result

    # 杂鱼♡～检查 pydantic 和 dataclass，但用缓存版本喵～
    if is_pydantic_instance(obj):
        # 杂鱼♡～使用兼容层来转换 Pydantic 实例喵～
        return pydantic_to_dict(obj)
    elif fast_is_dataclass(obj):
        result = {}
        t_hints = get_cached_type_hints(type(obj))
        for key, value in vars(obj).items():
            e_type = t_hints.get(key)

            # 杂鱼♡～为了测试能通过，本喵还是要验证字段类型喵～
            if e_type is not None:
                field_key = f"{parent_key}.{key}" if parent_key else key
                try:
                    validate_type(field_key, value, e_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时类型验证失败喵：字段 '{field_key}' {str(e)}～"
                    )

            # 杂鱼♡～转换值为字典喵～递归时传递字段类型～
            result[key] = convert_dataclass_to_dict(
                value, f"{parent_key}.{key}" if parent_key else key, e_type
            )
        return result
    return obj 