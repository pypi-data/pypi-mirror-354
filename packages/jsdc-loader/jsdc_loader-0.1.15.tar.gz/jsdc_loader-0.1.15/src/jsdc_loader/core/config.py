"""杂鱼♡～本喵为你创建的配置类喵～用来管理序列化和反序列化的各种选项～"""

from dataclasses import dataclass, field
from typing import Optional, Any, Callable, Dict, Set
from pathlib import Path

from .exceptions import InvalidConfigurationError


@dataclass
class JSDCConfig:
    """杂鱼♡～本喵的配置类喵～管理JSDC Loader的所有选项～"""
    
    # 杂鱼♡～文件操作配置喵～
    encoding: str = "utf-8"
    max_file_size: Optional[int] = 100 * 1024 * 1024  # 100MB 杂鱼♡～默认最大文件大小喵～
    create_parent_dirs: bool = True  # 杂鱼♡～自动创建父目录喵～
    backup_existing: bool = False  # 杂鱼♡～备份现有文件喵～
    
    # 杂鱼♡～JSON格式配置喵～
    indent: int = 4
    ensure_ascii: bool = False  # 杂鱼♡～支持中文等Unicode字符喵～
    sort_keys: bool = False
    separators: Optional[tuple] = None  # 杂鱼♡～JSON分隔符，None表示使用默认喵～
    
    # 杂鱼♡～验证配置喵～
    strict_type_checking: bool = True  # 杂鱼♡～严格类型检查喵～
    validate_on_serialize: bool = True  # 杂鱼♡～序列化时验证类型喵～
    validate_on_deserialize: bool = True  # 杂鱼♡～反序列化时验证类型喵～
    allow_extra_fields: bool = False  # 杂鱼♡～允许多余字段喵～
    ignore_missing_fields: bool = False  # 杂鱼♡～忽略缺失字段喵～
    
    # 杂鱼♡～错误处理配置喵～
    language: str = "zh"  # 杂鱼♡～错误信息语言，zh或en喵～
    detailed_errors: bool = True  # 杂鱼♡～详细错误信息喵～
    collect_all_errors: bool = False  # 杂鱼♡～收集所有错误还是遇到第一个就停止喵～
    
    # 杂鱼♡～性能配置喵～
    enable_caching: bool = True  # 杂鱼♡～启用类型缓存喵～
    cache_size: int = 1000  # 杂鱼♡～缓存大小喵～
    enable_fast_path: bool = True  # 杂鱼♡～启用快速路径优化喵～
    
    # 杂鱼♡～高级配置喵～
    custom_type_handlers: Dict[type, Callable] = field(default_factory=dict)  # 杂鱼♡～自定义类型处理器喵～
    excluded_fields: Set[str] = field(default_factory=set)  # 杂鱼♡～排除的字段喵～
    field_aliases: Dict[str, str] = field(default_factory=dict)  # 杂鱼♡～字段别名映射喵～
    
    # 杂鱼♡～调试配置喵～
    debug_mode: bool = False  # 杂鱼♡～调试模式喵～
    log_level: str = "WARNING"  # 杂鱼♡～日志级别喵～
    profile_performance: bool = False  # 杂鱼♡～性能分析喵～
    
    def __post_init__(self):
        """杂鱼♡～本喵会在初始化后验证配置喵～"""
        self.validate()
    
    def validate(self) -> None:
        """杂鱼♡～验证配置是否合法喵～"""
        errors = []
        
        # 杂鱼♡～验证编码喵～
        try:
            "test".encode(self.encoding)
        except LookupError:
            errors.append(f"杂鱼♡～不支持的编码: {self.encoding}喵！～")
        
        # 杂鱼♡～验证文件大小限制喵～
        if self.max_file_size is not None and self.max_file_size <= 0:
            errors.append("杂鱼♡～最大文件大小必须大于0喵！～")
        
        # 杂鱼♡～验证缩进喵～
        if self.indent < 0:
            errors.append("杂鱼♡～JSON缩进不能为负数喵！～")
        
        # 杂鱼♡～验证语言设置喵～
        if self.language.lower() not in ("zh", "en", "chinese", "english"):
            errors.append(f"杂鱼♡～不支持的语言设置: {self.language}，支持 'zh' 或 'en'喵！～")
        
        # 杂鱼♡～验证缓存大小喵～
        if self.cache_size <= 0:
            errors.append("杂鱼♡～缓存大小必须大于0喵！～")
        
        # 杂鱼♡～验证日志级别喵～
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"杂鱼♡～无效的日志级别: {self.log_level}，支持 {valid_log_levels}喵！～")
        
        if errors:
            raise InvalidConfigurationError(
                f"Configuration validation failed: {'; '.join(errors)}",
                f"杂鱼♡～配置验证失败喵：{'; '.join(errors)}～"
            )
    
    def copy(self, **changes) -> 'JSDCConfig':
        """杂鱼♡～创建配置的副本并应用更改喵～"""
        import copy
        new_config = copy.deepcopy(self)
        for key, value in changes.items():
            if hasattr(new_config, key):
                setattr(new_config, key, value)
            else:
                raise InvalidConfigurationError(
                    f"Unknown configuration option: {key}",
                    f"杂鱼♡～未知的配置选项: {key}喵！～"
                )
        new_config.validate()
        return new_config
    
    def to_dict(self) -> Dict[str, Any]:
        """杂鱼♡～将配置转换为字典喵～"""
        import copy
        config_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                config_dict[key] = copy.deepcopy(value)
            elif isinstance(value, set):
                # 杂鱼♡～将set转换为list以支持JSON序列化喵～
                config_dict[key] = list(value)
            else:
                config_dict[key] = value
        return config_dict
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'JSDCConfig':
        """杂鱼♡～从字典创建配置喵～"""
        # 杂鱼♡～过滤掉不属于JSDCConfig的键喵～
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_dict = {}
        for k, v in config_dict.items():
            if k in valid_keys:
                # 杂鱼♡～将特定的list字段转换回set喵～
                if k in ('excluded_fields',) and isinstance(v, list):
                    filtered_dict[k] = set(v)
                else:
                    filtered_dict[k] = v
        return cls(**filtered_dict)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'JSDCConfig':
        """杂鱼♡～从文件加载配置喵～支持JSON格式～"""
        import json
        from pathlib import Path
        
        path = Path(file_path)
        if not path.exists():
            raise InvalidConfigurationError(
                f"Configuration file not found: {file_path}",
                f"杂鱼♡～配置文件不存在: {file_path}喵！～"
            )
        
        try:
            with path.open('r', encoding='utf-8') as f:
                config_dict = json.load(f)
            return cls.from_dict(config_dict)
        except json.JSONDecodeError as e:
            raise InvalidConfigurationError(
                f"Invalid JSON in configuration file: {e}",
                f"杂鱼♡～配置文件JSON格式无效: {e}喵！～"
            )
        except Exception as e:
            raise InvalidConfigurationError(
                f"Failed to load configuration: {e}",
                f"杂鱼♡～加载配置失败: {e}喵！～"
            )
    
    def save_to_file(self, file_path: str) -> None:
        """杂鱼♡～保存配置到文件喵～"""
        import json
        from pathlib import Path
        
        path = Path(file_path)
        
        # 杂鱼♡～创建父目录喵～
        if self.create_parent_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # 杂鱼♡～备份现有文件喵～
        if self.backup_existing and path.exists():
            backup_path = path.with_suffix(path.suffix + '.backup')
            path.rename(backup_path)
        
        try:
            with path.open('w', encoding=self.encoding) as f:
                json.dump(
                    self.to_dict(),
                    f,
                    indent=self.indent,
                    ensure_ascii=self.ensure_ascii,
                    sort_keys=self.sort_keys,
                    separators=self.separators
                )
        except Exception as e:
            raise InvalidConfigurationError(
                f"Failed to save configuration: {e}",
                f"杂鱼♡～保存配置失败: {e}喵！～"
            )
    
    def get_language_code(self) -> str:
        """杂鱼♡～获取标准化的语言代码喵～"""
        lang = self.language.lower()
        if lang in ("zh", "chinese"):
            return "zh"
        elif lang in ("en", "english"):
            return "en"
        else:
            return "zh"  # 杂鱼♡～默认中文喵～
    
    def is_chinese(self) -> bool:
        """杂鱼♡～检查是否使用中文喵～"""
        return self.get_language_code() == "zh"
    
    def __repr__(self) -> str:
        """杂鱼♡～配置的字符串表示喵～"""
        return f"JSDCConfig(language={self.language}, strict_type_checking={self.strict_type_checking}, debug_mode={self.debug_mode})"


# 杂鱼♡～默认配置实例喵～
DEFAULT_CONFIG = JSDCConfig()


# 杂鱼♡～一些预设配置喵～
class ConfigPresets:
    """杂鱼♡～本喵准备的一些预设配置喵～杂鱼可以直接使用～"""
    
    @staticmethod
    def development() -> JSDCConfig:
        """杂鱼♡～开发环境配置喵～启用调试和详细错误信息～"""
        return JSDCConfig(
            debug_mode=True,
            detailed_errors=True,
            collect_all_errors=True,
            log_level="DEBUG",
            profile_performance=True,
            strict_type_checking=True
        )
    
    @staticmethod
    def production() -> JSDCConfig:
        """杂鱼♡～生产环境配置喵～性能优先，错误信息简洁～"""
        return JSDCConfig(
            debug_mode=False,
            detailed_errors=False,
            collect_all_errors=False,
            log_level="WARNING",
            profile_performance=False,
            enable_fast_path=True,
            enable_caching=True
        )
    
    @staticmethod
    def strict() -> JSDCConfig:
        """杂鱼♡～严格模式配置喵～所有验证都开启～"""
        return JSDCConfig(
            strict_type_checking=True,
            validate_on_serialize=True,
            validate_on_deserialize=True,
            allow_extra_fields=False,
            ignore_missing_fields=False,
            detailed_errors=True
        )
    
    @staticmethod
    def permissive() -> JSDCConfig:
        """杂鱼♡～宽松模式配置喵～容忍更多错误～"""
        return JSDCConfig(
            strict_type_checking=False,
            validate_on_serialize=False,
            validate_on_deserialize=False,
            allow_extra_fields=True,
            ignore_missing_fields=True,
            detailed_errors=False
        )
    
    @staticmethod
    def fast() -> JSDCConfig:
        """杂鱼♡～快速模式配置喵～性能最优化～"""
        return JSDCConfig(
            strict_type_checking=False,
            validate_on_serialize=False,
            validate_on_deserialize=False,
            enable_fast_path=True,
            enable_caching=True,
            cache_size=2000,
            detailed_errors=False,
            debug_mode=False
        )
    
    @staticmethod
    def english() -> JSDCConfig:
        """杂鱼♡～英文错误信息配置喵～"""
        return JSDCConfig(
            language="en",
            detailed_errors=True
        ) 