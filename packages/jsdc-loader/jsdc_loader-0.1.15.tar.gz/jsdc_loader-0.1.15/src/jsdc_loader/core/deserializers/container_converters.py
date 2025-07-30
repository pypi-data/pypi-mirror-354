"""杂鱼♡～本喵为你创建的容器类型转换器喵～专门处理字典、元组等容器类型的反序列化～"""

from dataclasses import is_dataclass
from typing import Any, Union

from ..type_checker import cached_get_origin, cached_get_args


def convert_dict_type(key: str, value: dict, e_type: Any) -> dict:
    """杂鱼♡～本喵帮你转换字典类型喵～支持各种键类型～
    
    Args:
        key: 字段名称，用于错误信息
        value: 要转换的字典值
        e_type: 目标字典类型
        
    Returns:
        转换后的字典
        
    Raises:
        ValueError: 当键类型不支持或转换失败时
    """
    # 需要导入convert_value，但要避免循环导入
    from .base import convert_value
    
    if cached_get_origin(e_type) is dict:
        key_type, val_type = cached_get_args(e_type)

        # 杂鱼♡～本喵扩展支持更多键类型了喵～
        # 支持字符串、整数、浮点数等基本类型作为键
        supported_key_types = (str, int, float, bool)
        if key_type not in supported_key_types:
            raise ValueError(
                f"杂鱼♡～字典键类型 {key_type} 暂不支持喵！支持的键类型: {supported_key_types}～"
            )

        # 杂鱼♡～如果键类型不是字符串，需要转换JSON中的字符串键为目标类型喵～
        converted_dict = {}
        for k, v in value.items():
            # 杂鱼♡～JSON中的键总是字符串，需要转换为目标键类型喵～
            if key_type == str:
                converted_key = k
            elif key_type == int:
                try:
                    converted_key = int(k)
                except ValueError:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为整数喵！～")
            elif key_type == float:
                try:
                    converted_key = float(k)
                except ValueError:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为浮点数喵！～")
            elif key_type == bool:
                if k.lower() in ("true", "1"):
                    converted_key = True
                elif k.lower() in ("false", "0"):
                    converted_key = False
                else:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为布尔值喵！～")
            else:
                converted_key = k  # 杂鱼♡～其他情况保持原样喵～

            # 杂鱼♡～转换值喵～
            if is_dataclass(val_type) or cached_get_origin(val_type) is Union:
                converted_dict[converted_key] = convert_value(f"{key}.{k}", v, val_type)
            else:
                converted_dict[converted_key] = v

        return converted_dict

    # Default case, just return the dict
    return value


def convert_tuple_type(key: str, value: list, e_type: Any) -> tuple:
    """杂鱼♡～本喵帮你把列表转换成元组喵～支持固定长度和可变长度元组～
    
    Args:
        key: 字段名称，用于错误信息
        value: 要转换的列表值
        e_type: 目标元组类型
        
    Returns:
        转换后的元组
        
    Raises:
        ValueError: 当元组长度不匹配时
    """
    # 需要导入convert_value，但要避免循环导入
    from .base import convert_value
    
    if cached_get_origin(e_type) is tuple:
        args = cached_get_args(e_type)
        if len(args) == 2 and args[1] is Ellipsis:  # Tuple[X, ...]
            element_type = args[0]
            return tuple(
                convert_value(f"{key}[{i}]", item, element_type)
                for i, item in enumerate(value)
            )
        elif args:  # Tuple[X, Y, Z]
            if len(value) != len(args):
                raise ValueError(
                    f"杂鱼♡～元组{key}的长度不匹配喵！期望{len(args)}，得到{len(value)}～"
                )
            return tuple(
                convert_value(f"{key}[{i}]", item, arg_type)
                for i, (item, arg_type) in enumerate(zip(value, args))
            )

    # 如果没有参数类型或者其他情况，直接转换为元组喵～
    return tuple(value) 