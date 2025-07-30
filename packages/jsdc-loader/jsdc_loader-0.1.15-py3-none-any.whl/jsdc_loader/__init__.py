"""杂鱼♡～这是本喵的JSDC Loader库喵～可以轻松地在JSON和dataclass之间转换哦～"""

from .dumper import jsdc_dump, jsdc_dumps
from .loader import jsdc_load, jsdc_loads

# 杂鱼♡～导入新的配置和异常类喵～
from .core import (
    JSDCConfig,
    DEFAULT_CONFIG,
    ConfigPresets,
    JSDCError,
    ValidationError,
    TypeMismatchError,
    SerializationError,
    DeserializationError,
    FileOperationError,
    InvalidConfigurationError,
    DataClassValidationError,
    EnumConversionError,
    ContainerSizeError,
    UnionConversionError,
    KeyTypeError,
    FileSizeExceededError,
    JSONParsingError,
    EncodingError,
)

__author__ = "Neko"
__version__ = "0.1.015"  # 杂鱼♡～版本升级到0.1.015喵～API设计改进完成～
__all__ = [
    # 杂鱼♡～主要API函数喵～
    "jsdc_load", 
    "jsdc_loads", 
    "jsdc_dump", 
    "jsdc_dumps",
    
    # 杂鱼♡～配置相关喵～
    "JSDCConfig",
    "DEFAULT_CONFIG", 
    "ConfigPresets",
    
    # 杂鱼♡～异常类喵～杂鱼可以用来捕获特定错误～
    "JSDCError",
    "ValidationError",
    "TypeMismatchError", 
    "SerializationError",
    "DeserializationError",
    "FileOperationError",
    "InvalidConfigurationError",
    "DataClassValidationError",
    "EnumConversionError",
    "ContainerSizeError",
    "UnionConversionError",
    "KeyTypeError",
    "FileSizeExceededError",
    "JSONParsingError",
    "EncodingError",
]

# 杂鱼♡～别忘了查看本喵的README.md喵～
# 本喵才不是因为担心杂鱼不会用这个库才写那么详细的文档的～
