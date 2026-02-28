# shuyx-wxminiprogram-fastapi

这是微信小程序的服务端代码，提供教育考试相关的接口服务，支持模拟考试、练习等功能。

## 技术栈

- **Web框架**: FastAPI
- **服务器**: Uvicorn
- **数据库**: MySQL
- **ORM**: SQLAlchemy 2.x
- **认证**: JWT
- **文档**: Swagger UI (自动生成)

## 本地运行服务

环境要求

- Python 3.8+
- MySQL 5.7+

```bash
python main.py
```

服务将在 `http://localhost:39666` 启动

可以访问 `http://localhost:39666/docs` 查看 Swagger UI 文档。

## 分层架构

项目采用清晰的三层架构设计：

Controller (路由层) → Service (业务逻辑层) → DAO (数据访问层) → Model (ORM模型层)

✅ 清晰的三层架构，类似 Spring Boot 风格，适合中大型项目。

> 各层职责
- **Controller层**: 处理HTTP请求，参数验证，响应格式化
- **Service层**: 实现业务逻辑，事务管理
- **DAO层**: 数据库操作，通用CRUD封装
- **Model层**: 数据库表结构映射，ORM模型定义

## 项目结构

├── config/ # 配置文件目录 
│ ├── database_config.py # 数据库配置 
│ └── log_config.py # 日志配置 
├── middlewares/ # 中间件 
│ ├── auth_middleware.py # 认证中间件 
│ ├── exception_middleware.py # 异常处理中间件 
│ └── logger_middleware.py # 日志中间件 
├── module_exam/ # 考试模块 
│ ├── controller/ # 路由层 
│ ├── service/ # 业务逻辑层 
│ ├── dao/ # 数据访问层 
│ ├── model/ # ORM模型层 
│ └── dto/ # 数据传输对象 
├── module_mall/ # 商城模块 
│ ├── controller/ # 路由层 
│ ├── service/ # 业务逻辑层 
│ ├── dao/ # 数据访问层 
│ ├── model/ # ORM模型层 
│ └── dto/ # 数据传输对象 
├── utils/ # 工具类 
│ ├── conversion_util.py # 转换工具 
│ ├── jwt_util.py # JWT工具 
│ └── response_util.py # 响应工具 
├── main.py # 项目入口 
├── requirements.txt # 依赖声明 
└── README.md # 项目说明

## 数据库

可以直接编辑 `config/database_config.py` 文件，配置数据库连接：

```python
MYSQL_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/shuyx_db"
```

## 依赖库 requirements.txt

> 如何生成requirements.txt？

```bash
# 通过该命令生成requirements.txt
pip freeze > requirements.txt

# 说明：
# 1. 该文件包含项目所有依赖库的版本信息，用于确保项目在不同环境中的一致性。
# 2. 建议在项目根目录下执行该命令，将所有直接依赖库及其子依赖库写入requirements.txt。
```

> 如何一次性安装所有依赖库？

```bash
pip install -r requirements.txt
```

## API文档

服务启动后，可通过以下地址访问自动生成的API文档：

- Swagger UI: `http://localhost:39666/docs`
- ReDoc: `http://localhost:39666/redoc`

## 开发规范

### BaseDao（数据访问基类）
- ✅ 泛型设计，支持所有 Model 复用
- ✅ 支持动态filters、排序、分页
- `add/update/delete`方法支持事务控制

通用CRUD中，已经封装了数据库的更新，删除，增加，等值查询等操作。其余非等值查询操作：模糊查询，范围查询等，建议在Service层中手动实现。

### BaseService（业务逻辑基类）
- ✅ 透传 DAO 方法，统一 session 管理


### DTO 使用方式


### 统一响应格式

- `ResponseDTO`支持泛型，可声明精确类型
- 全局异常处理器，自动转换异常为统一格式
- 支持HTTP状态码与业务code同步

```python
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```


## 中间件

- 实现认证中间件，基于JWT验证
- 全局异常处理中间件
- 请求日志中间件





