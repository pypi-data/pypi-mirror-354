"""杂鱼♡～本喵为你创建的异常类型层次喵～专门处理各种错误情况～"""

from typing import Optional, Any


class JSDCError(Exception):
    """杂鱼♡～本喵的基础异常类喵～所有JSDC相关异常的父类～"""
    
    def __init__(
        self, 
        message: str, 
        chinese_message: Optional[str] = None,
        field_name: Optional[str] = None,
        expected_type: Optional[Any] = None,
        actual_type: Optional[Any] = None,
        value: Optional[Any] = None
    ):
        self.english_message = message
        self.chinese_message = chinese_message or message
        self.field_name = field_name
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.value = value
        super().__init__(self.chinese_message)  # 杂鱼♡～默认显示中文消息喵～
    
    def get_message(self, language: str = "zh") -> str:
        """杂鱼♡～本喵支持中英文切换喵～"""
        if language.lower() in ("en", "english"):
            return self.english_message
        return self.chinese_message


class ValidationError(JSDCError):
    """杂鱼♡～验证错误喵～当数据不符合预期格式时抛出～"""
    pass


class TypeMismatchError(ValidationError):
    """杂鱼♡～类型不匹配错误喵～当类型转换失败时抛出～"""
    
    def __init__(
        self,
        field_name: str,
        expected_type: Any,
        actual_type: Any,
        value: Optional[Any] = None
    ):
        chinese_msg = f"杂鱼♡～键{field_name}的类型无效喵：期望{expected_type}，得到{actual_type}～"
        english_msg = f"Type mismatch for field '{field_name}': expected {expected_type}, got {actual_type}"
        
        super().__init__(
            english_msg,
            chinese_msg,
            field_name=field_name,
            expected_type=expected_type,
            actual_type=actual_type,
            value=value
        )


class SerializationError(JSDCError):
    """杂鱼♡～序列化错误喵～当无法将对象转换为JSON时抛出～"""
    pass


class DeserializationError(JSDCError):
    """杂鱼♡～反序列化错误喵～当无法从JSON创建对象时抛出～"""
    pass


class FileOperationError(JSDCError):
    """杂鱼♡～文件操作错误喵～当文件读写失败时抛出～"""
    pass


class InvalidConfigurationError(JSDCError):
    """杂鱼♡～配置错误喵～当JSDC配置无效时抛出～"""
    pass


class DataClassValidationError(ValidationError):
    """杂鱼♡～数据类验证错误喵～当提供的类不是有效的dataclass或Pydantic模型时抛出～"""
    
    def __init__(self, cls: Any):
        chinese_msg = f"杂鱼♡～{cls}不是有效的dataclass或Pydantic BaseModel喵！～"
        english_msg = f"{cls} is not a valid dataclass or Pydantic BaseModel"
        
        super().__init__(english_msg, chinese_msg, expected_type="dataclass or BaseModel", actual_type=type(cls))


class EnumConversionError(ValidationError):
    """杂鱼♡～枚举转换错误喵～当枚举值无效时抛出～"""
    
    def __init__(self, field_name: str, value: Any, enum_type: Any):
        chinese_msg = f"杂鱼♡～键{field_name}的枚举值无效喵：{value}，期望{enum_type}的成员～"
        english_msg = f"Invalid enum value for field '{field_name}': {value}, expected member of {enum_type}"
        
        super().__init__(
            english_msg,
            chinese_msg,
            field_name=field_name,
            expected_type=enum_type,
            actual_type=type(value),
            value=value
        )


class ContainerSizeError(ValidationError):
    """杂鱼♡～容器大小错误喵～当容器（如元组）长度不匹配时抛出～"""
    
    def __init__(self, field_name: str, expected_size: int, actual_size: int):
        chinese_msg = f"杂鱼♡～{field_name}的长度不匹配喵！期望{expected_size}，得到{actual_size}～"
        english_msg = f"Size mismatch for {field_name}: expected {expected_size}, got {actual_size}"
        
        super().__init__(
            english_msg,
            chinese_msg,
            field_name=field_name,
            expected_type=f"size={expected_size}",
            actual_type=f"size={actual_size}"
        )


class UnionConversionError(ValidationError):
    """杂鱼♡～联合类型转换错误喵～当无法转换为Union中任何类型时抛出～"""
    
    def __init__(self, field_name: str, value: Any, union_type: Any):
        chinese_msg = f"杂鱼♡～无法将键{field_name}的值{value}转换为{union_type}喵！～"
        english_msg = f"Cannot convert value {value} for field '{field_name}' to any type in {union_type}"
        
        super().__init__(
            english_msg,
            chinese_msg,
            field_name=field_name,
            expected_type=union_type,
            actual_type=type(value),
            value=value
        )


class KeyTypeError(ValidationError):
    """杂鱼♡～字典键类型错误喵～当字典键类型不支持时抛出～"""
    
    def __init__(self, key_type: Any, supported_types: tuple):
        chinese_msg = f"杂鱼♡～字典键类型 {key_type} 暂不支持喵！支持的键类型: {supported_types}～"
        english_msg = f"Dictionary key type {key_type} is not supported. Supported key types: {supported_types}"
        
        super().__init__(
            english_msg,
            chinese_msg,
            expected_type=f"one of {supported_types}",
            actual_type=key_type
        )


class FileSizeExceededError(FileOperationError):
    """杂鱼♡～文件大小超限错误喵～当文件太大时抛出～"""
    
    def __init__(self, file_path: str, current_size: int, max_size: int):
        chinese_msg = f"杂鱼♡～文件大小超过限制喵！{file_path} 当前大小：{current_size}字节，最大允许：{max_size}字节～"
        english_msg = f"File size exceeded limit: {file_path} current size: {current_size} bytes, max allowed: {max_size} bytes"
        
        super().__init__(english_msg, chinese_msg, field_name=file_path)


class JSONParsingError(DeserializationError):
    """杂鱼♡～JSON解析错误喵～当JSON格式无效时抛出～"""
    
    def __init__(self, original_error: str, file_path: Optional[str] = None):
        if file_path:
            chinese_msg = f"杂鱼♡～无效的JSON文件喵：{file_path}，错误：{original_error}～"
            english_msg = f"Invalid JSON file: {file_path}, error: {original_error}"
        else:
            chinese_msg = f"杂鱼♡～无效的JSON喵：{original_error}～"
            english_msg = f"Invalid JSON: {original_error}"
        
        super().__init__(english_msg, chinese_msg, field_name=file_path)


class EncodingError(FileOperationError):
    """杂鱼♡～编码错误喵～当文件编码有问题时抛出～"""
    
    def __init__(self, encoding: str, original_error: str, file_path: Optional[str] = None):
        if file_path:
            chinese_msg = f"杂鱼♡～用{encoding}编码文件{file_path}失败喵：{original_error}～杂鱼是不是编码搞错了？～"
            english_msg = f"Failed to encode file {file_path} with {encoding}: {original_error}"
        else:
            chinese_msg = f"杂鱼♡～用{encoding}编码失败喵：{original_error}～杂鱼是不是编码搞错了？～"
            english_msg = f"Failed to encode with {encoding}: {original_error}"
        
        super().__init__(english_msg, chinese_msg, field_name=file_path) 