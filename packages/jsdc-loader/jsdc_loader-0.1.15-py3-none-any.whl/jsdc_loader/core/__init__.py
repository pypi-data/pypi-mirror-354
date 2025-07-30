"""杂鱼♡～这是本喵的JSDC Loader核心功能喵～经过重构后变得更整洁了♡～"""

# 杂鱼♡～从新的模块化结构中导入功能喵～
from .serializers import convert_dataclass_to_dict
from .deserializers import convert_dict_to_dataclass
from .types import T
from .validator import validate_dataclass, validate_type
from .type_checker import (
    cached_get_origin,
    cached_get_args,
    cached_isinstance,
    fast_is_dataclass,
    get_special_type,
    is_frozen_dataclass,
)

# 杂鱼♡～导入新的异常类和配置类喵～
from .exceptions import (
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
from .config import JSDCConfig, DEFAULT_CONFIG, ConfigPresets

__all__ = [
    # 杂鱼♡～核心功能喵～
    "T",
    "convert_dict_to_dataclass",
    "convert_dataclass_to_dict",
    "validate_dataclass",
    "validate_type",
    "cached_get_origin",
    "cached_get_args", 
    "cached_isinstance",
    "fast_is_dataclass",
    "get_special_type",
    "is_frozen_dataclass",
    
    # 杂鱼♡～异常类喵～
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
    
    # 杂鱼♡～配置类喵～
    "JSDCConfig",
    "DEFAULT_CONFIG",
    "ConfigPresets",
]

# 杂鱼♡～本喵把最重要的功能都放在这里了喵～
# 不要直接导入这些函数，应该使用公共API喵～
