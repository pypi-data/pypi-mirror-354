"""杂鱼♡～本喵为你创建的联合类型转换器喵～专门处理Union和Optional类型的反序列化～"""

from typing import Any, Union

from ..type_checker import cached_get_args, _is_exact_type_match


def convert_union_type(key: str, value: Any, union_type: Any) -> Any:
    """杂鱼♡～本喵帮你转换联合类型喵～支持Union和Optional～
    
    Args:
        key: 字段名称，用于错误信息
        value: 要转换的值
        union_type: 联合类型
        
    Returns:
        转换后的值
        
    Raises:
        TypeError: 当所有类型转换都失败时
    """
    # 需要导入convert_value，但要避免循环导入
    from .base import convert_value
    
    args = cached_get_args(union_type)

    # 杂鱼♡～处理None值喵～
    if value is None and type(None) in args:
        return None

    # 杂鱼♡～首先尝试精确类型匹配，这样可以避免不必要的类型转换喵～
    for arg_type in args:
        if arg_type is type(None):
            continue

        # 杂鱼♡～检查是否是精确的类型匹配喵～
        if _is_exact_type_match(value, arg_type):
            try:
                return convert_value(key, value, arg_type)
            except (ValueError, TypeError):
                continue

    # 杂鱼♡～如果没有精确匹配，再尝试类型转换喵～
    for arg_type in args:
        if arg_type is type(None):
            continue

        # 杂鱼♡～跳过已经尝试过的精确匹配喵～
        if _is_exact_type_match(value, arg_type):
            continue

        try:
            return convert_value(key, value, arg_type)
        except (ValueError, TypeError):
            continue

    # 如果所有转换都失败，则抛出错误喵～
    raise TypeError(f"杂鱼♡～无法将键{key}的值{value}转换为{union_type}喵！～") 