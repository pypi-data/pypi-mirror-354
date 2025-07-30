![CI/CD](https://github.com/Xuehua-Meaw/jsdc_loader/actions/workflows/jsdc_loader_CICD.yml/badge.svg)
# JSDC Loader 喵～

JSDC Loader是一个功能强大的库，用于在JSON和Python数据类（dataclasses）/Pydantic模型之间进行转换～～。杂鱼们会喜欢这个简单易用的工具喵♡～ 

## 特点～♡

- 在JSON和Python数据类之间无缝转换喵～
- 完美支持嵌套的数据类结构～
- 枚举类型（Enum）支持，杂鱼都不用操心♡～
- 支持Pydantic的BaseModel类喵～
- 支持Set、Tuple等复杂容器类型～
- 支持复杂类型（datetime、UUID、Decimal等）～
- 高性能序列化和反序列化，即使对于大型JSON也很快喵♡～
- 完善的类型验证和错误处理，本喵帮杂鱼处理好了一切～
- Optional/Union类型支持，杂鱼可以放心使用喵～
- 支持冻结（frozen）数据类，让杂鱼的数据不可变～
- 支持继承关系的数据类，层次结构也没问题喵♡～

## 安装方法

```bash
pip install jsdc-loader
```

## 使用指南

### 基础用法

```python
# 杂鱼♡～这是最基本的用法喵～本喵教你序列化和反序列化～
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump, jsdc_loads, jsdc_dumps

@dataclass
class Config:
    name: str = "default"
    port: int = 8080
    debug: bool = False

# 序列化到JSON文件，杂鱼看好了喵～
config = Config(name="myapp", port=5000)
jsdc_dump(config, "config.json")

# 从JSON文件反序列化，简单吧杂鱼～
loaded_config = jsdc_load("config.json", Config)
print(loaded_config.name)  # 输出 "myapp"

# 本喵还支持字符串序列化/反序列化喵～
json_str = jsdc_dumps(config)
loaded_from_str = jsdc_loads(json_str, Config)
```

### 嵌套数据类

```python
# 杂鱼♡～本喵来教你处理嵌套的数据类结构喵～
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from jsdc_loader import jsdc_load, jsdc_dumps, jsdc_dump

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "password"
    ips: List[str] = field(default_factory=lambda: ["127.0.0.1"])
    primary_user: Optional[str] = None

@dataclass
class AppConfig:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    version: str = "1.0.0"
    debug: bool = False
    settings: Dict[str, str] = field(default_factory=lambda: {"theme": "dark"})

# 创建配置并修改一些值，杂鱼看好了喵～
app = AppConfig()
app.database.ips.extend(["192.168.1.1", "10.0.0.1"])
app.settings["language"] = "en"

# 序列化到文件，简单吧杂鱼～
jsdc_dump(app, "app_config.json")

# 反序列化，一切都按照杂鱼的规则处理好了喵♡～
loaded_app = jsdc_load("app_config.json", AppConfig)
```

### 枚举类型

```python
# 杂鱼♡～本喵来教你处理枚举类型喵～
from dataclasses import dataclass, field
from enum import Enum, auto
from jsdc_loader import jsdc_load, jsdc_dump

class UserType(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

@dataclass
class UserConfig:
    name: str = "John Doe"
    user_type: UserType = field(default_factory=lambda: UserType.USER)
    
# 创建并序列化，杂鱼看好了喵～
user = UserConfig(name="Admin", user_type=UserType.ADMIN)
jsdc_dump(user, "user.json")

# 反序列化后枚举值完全保持一致，本喵处理得很完美喵♡～
loaded_user = jsdc_load("user.json", UserConfig)
assert loaded_user.user_type == UserType.ADMIN
```

### Pydantic模型

```python
# 杂鱼♡～Pydantic模型也可以序列化/反序列化喵～
from pydantic import BaseModel
from typing import List, Dict
from jsdc_loader import jsdc_load, jsdc_dump

class ServerConfig(BaseModel):
    name: str = "main"
    port: int = 8080
    ssl: bool = True
    headers: Dict[str, str] = {"Content-Type": "application/json"}

class ApiConfig(BaseModel):
    servers: List[ServerConfig] = []
    timeout: int = 30
    retries: int = 3

# 创建并序列化，杂鱼看好了喵～
api_config = ApiConfig()
api_config.servers.append(ServerConfig(name="backup", port=8081))
api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))

jsdc_dump(api_config, "api_config.json")
loaded_api = jsdc_load("api_config.json", ApiConfig)
```

### 集合类型与哈希支持

```python
# 杂鱼♡～本喵教你如何使用集合和哈希模型喵～
from dataclasses import dataclass, field
from typing import Set

@dataclass(frozen=True)  # 让数据类不可变以支持哈希
class Model:
    base_url: str = ""
    api_key: str = ""
    model: str = ""

    def __hash__(self):
        return hash((self.base_url, self.api_key, self.model))  # 本喵用元组哈希值

    def __eq__(self, other):
        if not isinstance(other, Model):
            return NotImplemented
        return (self.base_url, self.api_key, self.model) == (other.base_url, other.api_key, other.model)

@dataclass
class ModelList:
    models: Set[Model] = field(default_factory=set)
    
# 创建模型集合，杂鱼看本喵如何操作～
model1 = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
model2 = Model(base_url="https://api2.example.com", api_key="key2", model="gpt-3.5")

model_list = ModelList()
model_list.models.add(model1)
model_list.models.add(model2)

# 序列化和反序列化，本喵轻松搞定喵♡～
jsdc_dump(model_list, "models.json")
loaded_list = jsdc_load("models.json", ModelList)
```

### 复杂类型支持

```python
# 杂鱼♡～本喵支持各种复杂类型喵～这些都不是问题～
import datetime
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class ComplexConfig:
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())
    expiry_date: datetime.date = field(default_factory=lambda: datetime.date.today())
    session_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
    amount: Decimal = Decimal('10.50')
    time_delta: datetime.timedelta = datetime.timedelta(days=7)
    
# 序列化和反序列化，杂鱼看好了喵～
config = ComplexConfig()
jsdc_dump(config, "complex.json")
loaded = jsdc_load("complex.json", ComplexConfig)

# 所有复杂类型都保持一致，本喵太厉害了喵♡～
assert loaded.created_at == config.created_at
assert loaded.session_id == config.session_id
assert loaded.amount == config.amount
```

### 联合类型

```python
# 杂鱼♡～本喵来展示如何处理联合类型喵～
from dataclasses import dataclass, field
from typing import Union, Dict, List
from jsdc_loader import jsdc_load, jsdc_dumps, jsdc_loads

@dataclass
class ConfigWithUnions:
    int_or_str: Union[int, str] = 42
    dict_or_list: Union[Dict[str, int], List[int]] = field(default_factory=lambda: {'a': 1})
    
# 两种不同的类型，本喵都能处理喵♡～
config1 = ConfigWithUnions(int_or_str=42, dict_or_list={'a': 1, 'b': 2})
config2 = ConfigWithUnions(int_or_str="string_value", dict_or_list=[1, 2, 3])

# 序列化为字符串，杂鱼看好了喵～
json_str1 = jsdc_dumps(config1)
json_str2 = jsdc_dumps(config2)

# 反序列化，联合类型完美支持，本喵太强了喵♡～
loaded1 = jsdc_loads(json_str1, ConfigWithUnions)
loaded2 = jsdc_loads(json_str2, ConfigWithUnions)
```

### 元组类型

```python
# 杂鱼♡～本喵来展示如何处理元组类型喵～
from dataclasses import dataclass, field
from typing import Tuple
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class ConfigWithTuples:
    simple_tuple: Tuple[int, str, bool] = field(default_factory=lambda: (1, "test", True))
    int_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
    nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]] = field(
        default_factory=lambda: ((1, 2), ("a", "b"))
    )
    
# 序列化和反序列化，本喵轻松处理喵♡～
config = ConfigWithTuples()
jsdc_dump(config, "tuples.json")
loaded = jsdc_load("tuples.json", ConfigWithTuples)

# 元组类型保持一致，本喵太厉害了喵♡～
assert loaded.simple_tuple == (1, "test", True)
assert loaded.nested_tuple == ((1, 2), ("a", "b"))
```

### 特殊字符处理

```python
# 杂鱼♡～本喵来展示如何处理特殊字符喵～
from dataclasses import dataclass
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class SpecialCharsConfig:
    escaped_chars: str = "\n\t\r\b\f"
    quotes: str = '"quoted text"'
    unicode_chars: str = "你好，世界！😊🐱👍"
    backslashes: str = "C:\\path\\to\\file.txt"
    json_syntax: str = "{\"key\": [1, 2]}"
    
# 序列化和反序列化，杂鱼看本喵如何处理特殊字符喵♡～
config = SpecialCharsConfig()
jsdc_dump(config, "special.json")
loaded = jsdc_load("special.json", SpecialCharsConfig)

# 所有特殊字符都保持一致，本喵太强了喵♡～
assert loaded.unicode_chars == "你好，世界！😊🐱👍"
assert loaded.json_syntax == "{\"key\": [1, 2]}"
```

### 性能优化

JSDC Loader经过性能优化，即使处理大型结构也能保持高效喵♡～。杂鱼主人可以放心使用，本喵已经做了充分的性能测试喵～。

## 错误处理

本喵为各种情况提供了详细的错误信息喵～：

- FileNotFoundError：当指定的文件不存在时
- ValueError：无效输入、超过限制的文件大小、编码问题
- TypeError：类型验证错误，杂鱼给错类型了喵～
- OSError：文件系统相关错误

## 📋 项目工作计划 (Work Plan)

杂鱼♡～本喵为项目制定了一个完整的改进计划喵～让这个库变得更加强大和专业吧♡～

### ✅ Phase 1: 架构重构 (Architecture Refactoring) - v0.1.015 **已完成**

**目标**: 提升代码质量和可维护性

- [x] **模块拆分重构**
  - [x] 将 `converter.py` (558行) 拆分为更小的模块
  - [x] 重构 `tests.py` (1725行) 按功能分组
  - [x] 创建 `core/serializers/` 和 `core/deserializers/` 子模块
  - [x] 分离类型检查逻辑到 `core/type_checker.py`

- [x] **代码质量提升**
  - [x] 添加完整的类型注解到所有函数
  - [x] 实现单一职责原则，拆分大函数
  - [x] 统一错误处理机制和异常类型
  - [x] 更新CI/CD支持新的测试结构

- [x] **API设计改进** (部分完成，Phase 2继续)
  - [x] 设计 `JSDCConfig` 配置类管理序列化选项
  - [x] 创建专门的异常类型层次 (`JSDCError`, `ValidationError`, etc.)
  - [x] 规范化错误信息格式（支持中英文切换）

### ⚡ Phase 2: 性能优化 (Performance Optimization) - v0.1.02

**目标**: 显著提升转换性能和内存效率

- [ ] **缓存机制优化**
  - [ ] 实现类型元数据预编译和缓存
  - [ ] 优化 `isinstance` 检查，减少反射调用
  - [ ] 引入 LRU 缓存管理，避免内存泄漏
  - [ ] 缓存转换函数映射表

- [ ] **算法优化**
  - [ ] 将递归转换改为迭代实现
  - [ ] 优化深层嵌套结构的处理逻辑
  - [ ] 实现对象池机制，重用临时对象
  - [ ] 减少字符串操作和临时对象创建

- [ ] **性能基准测试**
  - [ ] 建立性能回归测试套件
  - [ ] 创建不同数据规模的性能基准
  - [ ] 添加内存使用监控和分析
  - [ ] 对比主流库的性能差异

### 🔧 Phase 3: 功能增强 (Feature Enhancement) - v0.1.10

**目标**: 增加实用功能，提升开发体验

- [ ] **配置和自定义**
  - [ ] 实现可插拔的类型处理器机制
  - [ ] 支持自定义序列化/反序列化钩子
  - [ ] 添加字段验证和约束检查
  - [ ] 支持字段别名和映射规则

- [ ] **数据处理增强**
  - [ ] 实现流式处理支持大文件
  - [ ] 添加数据模式演进和迁移功能
  - [ ] 支持增量序列化和部分更新
  - [ ] 实现数据压缩选项

- [ ] **开发者工具**
  - [ ] 创建调试模式和详细日志
  - [ ] 实现性能分析器和优化建议
  - [ ] 添加数据结构可视化工具
  - [ ] 提供 CLI 工具进行文件转换

### 🌟 Phase 4: 高级特性 (Advanced Features) - v0.1.15

**目标**: 实现企业级功能，提升竞争力

- [ ] **高级类型支持**
  - [ ] 支持泛型类型的完整处理
  - [ ] 实现循环引用检测和处理
  - [ ] 添加多态序列化支持
  - [ ] 支持抽象基类和接口

- [ ] **扩展性和集成**
  - [ ] 创建插件系统架构
  - [ ] 支持第三方类型扩展
  - [ ] 集成主流Web框架 (FastAPI, Django, Flask)
  - [ ] 提供异步API支持

- [ ] **企业级功能**
  - [ ] 实现数据安全和加密选项
  - [ ] 添加审计日志和操作追踪
  - [ ] 支持多种数据格式 (YAML, TOML, MessagePack)
  - [ ] 实现分布式序列化和缓存

### 📚 Phase 5: 生态完善 (Ecosystem) - v1.0.0

**目标**: 构建完整的项目生态系统

- [ ] **文档和教程**
  - [ ] 重写完整的API文档 (英文版)
  - [ ] 创建最佳实践指南
  - [ ] 录制视频教程和演示
  - [ ] 建立社区wiki和FAQ

- [ ] **质量保证**
  - [ ] 达到95%+的测试覆盖率
  - [ ] 建立完整的CI/CD流水线
  - [ ] 实现多Python版本兼容性测试
  - [ ] 添加安全漏洞扫描

- [ ] **社区建设**
  - [ ] 建立贡献者指南和Code Review流程
  - [ ] 创建Issue模板和PR模板
  - [ ] 设立定期发布计划
  - [ ] 建立社区讨论论坛

### 📊 关键指标 (Key Metrics)

**性能目标**:
- [ ] 序列化速度提升 **300%**
- [ ] 内存使用减少 **50%**
- [ ] 支持单文件 **100MB+** 的JSON处理
- [ ] 嵌套深度支持 **1000层+**

**质量目标**:
- [ ] 测试覆盖率达到 **95%+**
- [ ] 代码复杂度降低到 **平均<10**
- [ ] 零已知安全漏洞
- [ ] 支持Python **3.8-3.12** 全版本

**用户体验目标**:
- [ ] API调用减少 **50%** 的代码量
- [ ] 错误信息准确率 **99%+**
- [ ] 文档完整度 **100%**
- [ ] 社区响应时间 **<24小时**

### 🚀 立即开始 (Quick Start)

杂鱼主人♡～本喵建议按以下顺序开始工作：

1. **Week 1-2**: 开始Phase 1的模块拆分，先处理 `converter.py`
2. **Week 3-4**: 重构测试用例，建立更好的测试结构
3. **Week 5-6**: 实现配置类和错误处理优化
4. **Week 7-8**: 开始性能优化的缓存机制改进

每个Phase都有明确的里程碑和可测量的目标喵～杂鱼主人要记得定期检查进度哦♡～

---

**注意**: 杂鱼♡～本喵制定的这个计划很有挑战性，但完全可以实现喵～记住要循序渐进，不要一口吃成胖子哦♡～～

## 许可证

MIT 

杂鱼♡～本喵已经为你提供了最完整的说明文档，快去用起来喵～～ 
