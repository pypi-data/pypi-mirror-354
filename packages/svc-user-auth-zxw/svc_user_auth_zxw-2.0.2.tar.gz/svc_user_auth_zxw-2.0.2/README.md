# svc_user_auth_zxw 用户认证权限管理库

## 简介

`svc_user_auth_zxw` 是一个基于 FastAPI 的用户认证和权限管理 Python 库，提供完整的用户注册、登录、权限验证等功能。支持多种登录方式，包括账号密码、微信登录、手机号验证码登录等。

## 📚 版本历史

### 非兼容性更新，与之前的版本不兼容
- **2.0.2**
  - 阿里云sms发送配置使用config中配置, 为None时使用默认配置
- **2.0.1**
    - 修正使用文档错误
- **2.0.0**
  - 项目由 user_auth_zxw 更名为 svc_svc_user_auth_zxw
  - 尚未进行任何测试,可能存在错误
### 非兼容性更新，与之前的版本不兼容
#### 1.0.0以上版本，适配VUE-ELEMENT-PLUS-ADMIN框架
- **1.0.5**
  - 用户文档错误修正
- **1.0.4**: 添加用户文档
- **1.0.3**: 
  - bug fix
  - 新用户注册后，to_payload()报错修复
  - 优化: 用户角色关联数据加载
- **1.0.2**: 
  - 优化账号密码注册登录返回值；
  - bug fix - 变更数据表结构：Role采用联合主键：(app_id, name)
  - 与VUE-ELEMENT-PLUS-ADMIN框架保持一致，完成账号密码注册登录API对接
- **1.0.1**: 新增vue-element-plus-admin api: 退出登录
- **1.0.0**: 统一API返回值，符合vue-element-plus-admin框架原生标准
  - 返回值格式: `{"code": 200, "data": {}}`

### 早期版本
- **0.1.1**: 支持多线程任务，集成修改: 短信验证码验证，redis存储与验证
- **0.1.0**: 修改: jwt验证失败, 弹出401 HTTPException_AppToolsSZXW异常
- **0.0.9**: 表结构User新增字段:referer_id,referer,invitees , 手机号注册登录新增相应字段.  对应功能: 增加邀请人信息
- **0.0.8**: 新增:批量删除用户角色(delete_roles)
- **0.0.7.4**: 优化configs.py导入
- **0.0.7.3**: 上传vue前端页面
- **0.0.7.2**: 取消get_current_user的print(token)
- **0.0.7.1**: 新增api: /register-or-login-phone/ 手机号注册或登录
- **0.0.7**: bug fix : add new role
- **0.0.6.9**: bug fix : 注册登录 import add_new_role
- **0.0.6.8**: 新增:require_roles函数, 批量验证权限
- **0.0.6.7**: 新增:delete_role函数, 解除用户权限(只解除关联, 不删除role表)
- **0.0.6.6**: 新增:add_new_role函数, 新增app name, 用户权限
- **0.0.6.5**: 去掉地址中冗余地址../api/...，tags优化

## 📋 目录

1. [特性](#特性)
2. [安装](#安装)
3. [快速开始](#快速开始)
4. [完整API使用说明](#完整api使用说明)
5. [权限管理](#权限管理)
6. [前端集成](#前端集成)
7. [高级功能](#高级功能)
8. [错误处理](#错误处理)
9. [部署注意事项](#部署注意事项)

## ✨ 特性

- 🔐 多种登录方式：账号密码、微信、手机验证码
- 🎯 灵活的角色权限管理系统
- 🔑 JWT Token 认证机制
- 📱 短信验证码支持
- 🗄️ Redis 缓存支持
- 🎨 适配 Vue-Element-Plus-Admin 框架
- 🚀 异步数据库操作（PostgreSQL）
- 🔄 Token 刷新机制

## 🚀 安装

### 1. 通过 pip 安装

```bash
pip install svc_user_auth_zxw
```


## ⚡ 快速开始

### 1. 项目配置

- （推荐）在项目根目录创建 `configs/config_user_auth.py` 文件：

```python
import os
from datetime import timedelta

# PostgreSQL 数据库配置
DATABASE_URL = os.environ.get('USER_CENTER_DATABASE_URL')
if not DATABASE_URL:
    DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/database_name"
    os.environ['USER_CENTER_DATABASE_URL'] = DATABASE_URL

# Redis 数据库配置
REDIS_URL_AUTH = os.environ.get('REDIS_URL_AUTH')
if not REDIS_URL_AUTH:
    REDIS_URL_AUTH = "redis://:your_redis_password@localhost:6379/0"
    os.environ['REDIS_URL_AUTH'] = REDIS_URL_AUTH

# JWT 配置
class JWT:
    SECRET_KEY = "your-secret-key-here"
    ALGORITHM = "HS256"
    expire_time = timedelta(seconds=3600)  # 1小时

# 应用配置
app_name = "your_app_name"

# 微信配置（可选）
class WeChatPub:
    app_id = "your_wechat_app_id"
    app_secret = "your_wechat_app_secret"
    scope = "snsapi_login"
    state = "your_custom_state"

# 阿里云短信配置（可选）
class AliyunSMS:
    ali_access_key_id = "your_access_key_id"
    ali_access_key_secret = "your_access_key_secret"
```

### 2. FastAPI 应用集成

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from svc_user_auth_zxw import router as user_auth_router

# 创建 FastAPI 应用
app = FastAPI(title="你的应用")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

# 注册用户认证路由
app.include_router(user_auth_router, prefix="/user_center")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3. 数据库初始化

在项目主函数导入from svc_user_auth_zxw import router模块时，自动进行数据库初始化.

## 📖 完整API使用说明

> **前缀说明**: 所有API都需要加上前缀 `/user_center`（如果在集成时设置了prefix）

### 🔐 账号密码认证

#### 1. 用户注册
- **URL**: `/api/account/normal/register/`
- **方法**: `POST`
- **描述**: 使用账号密码注册新用户

```json
// 请求参数
{
    "username": "testuser",
    "password": "password123",
    "role_name": "user",      // 可选，默认 "l0"
    "app_name": "your_app"    // 可选，默认 "app0"
}

// 响应示例
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "testuser",
            "nickname": "testuser",
            "roles": [...],
            "email": "testuser",
            "phone": "testuser"
        }
    }
}
```

#### 2. 用户登录
- **URL**: `/api/account/normal/login/`
- **方法**: `POST`
- **描述**: 使用账号密码登录

```json
// 请求参数
{
    "username": "testuser",
    "password": "password123"
}

// 响应示例（同注册格式）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "testuser",
            "nickname": "testuser",
            "roles": [...],
            "email": "testuser",
            "phone": "testuser"
        }
    }
}
```

#### 3. 表单登录
- **URL**: `/api/account/normal/login-form/`
- **方法**: `POST`
- **描述**: 使用OAuth2PasswordRequestForm格式登录
- **Content-Type**: `application/x-www-form-urlencoded`

```
// 请求参数
username=testuser&password=password123&grant_type=password

// 响应示例（同账号密码登录格式）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "testuser",
            "nickname": "testuser",
            "roles": [...]
        }
    }
}
```

### 📱 手机号认证

#### 1. 发送验证码
- **URL**: `/api/account/phone/send-verification-code/`
- **方法**: `POST`

```json
// 请求参数
{
    "phone": "13800138000"
}

// 响应示例
{
    "code": 200,
    "data": {
        "message": "验证码已发送"
    }
}
```

#### 2. 手机号注册
- **URL**: `/api/account/phone/register-phone/`
- **方法**: `POST`

```json
// 请求参数
{
    "phone": "13800138000",
    "sms_code": "123456",
    "email": "user@example.com",     // 可选
    "referer_id": 123,               // 可选，邀请人ID
    "role_name": "user",             // 可选，默认 "l0"
    "app_name": "your_app"           // 可选，默认 "app0"
}

// 响应示例（同登录格式）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "13800138000",
            "nickname": "13800138000",
            "roles": [...],
            "email": "user@example.com",
            "phone": "13800138000"
        }
    }
}
```

#### 3. 手机号登录
- **URL**: `/api/account/phone/login-phone/`
- **方法**: `POST`

```json
// 请求参数
{
    "phone": "13800138000",
    "sms_code": "123456"
}

// 响应示例（同注册格式）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "13800138000",
            "nickname": "13800138000",
            "roles": [...],
            "email": "user@example.com",
            "phone": "13800138000"
        }
    }
}
```

#### 4. 手机号注册或登录（推荐）
- **URL**: `/api/account/phone/register-or-login-phone/`
- **方法**: `POST`
- **描述**: 自动判断用户是否存在，存在则登录，不存在则注册

```json
// 请求参数
{
    "phone": "13800138000",
    "sms_code": "123456",
    "referer_id": 123,        // 可选，邀请人ID
    "app_name": "your_app"    // 可选
}

// 响应示例（同登录格式）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "13800138000",
            "nickname": "13800138000",
            "roles": [...],
            "email": null,
            "phone": "13800138000"
        }
    }
}
```

#### 5. 更换绑定手机号
- **URL**: `/api/account/phone/change-phone/`
- **方法**: `POST`
- **需要认证**: ✅

```json
// 请求参数
{
    "new_phone": "13900139000",
    "sms_code": "123456"
}

// 响应示例（返回更新后的用户信息）
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "testuser",
            "nickname": "testuser",
            "roles": [...],
            "email": "test@example.com",
            "phone": "13900139000"
        }
    }
}
```

### 🔗 微信登录认证

#### 1. 获取登录二维码URL
- **URL**: `/api/account/wechat/qr-login/get-qrcode`
- **方法**: `POST`

```json
// 请求参数
{
    "WECHAT_REDIRECT_URI": "https://your-domain.com/callback"
}

// 响应示例
{
    "code": 200,
    "data": {
        "qr_code_url": "https://open.weixin.qq.com/connect/qrconnect?..."
    }
}
```

#### 2. 微信一键登录
- **URL**: `/api/account/wechat/qr-login/login/`
- **方法**: `POST`

```json
// 请求参数
{
    "code": "微信返回的授权码",
    "app_name": "your_app"
}

// 响应示例
{
    "code": 200,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user_info": {
            "username": "wx_openid",
            "nickname": "WeChatPub User",
            "roles": [...],
            "email": "wx_openid",
            "phone": "wx_openid"
        }
    }
}
```

### 🎫 JWT Token管理

#### 1. 获取当前用户信息
- **URL**: `/api/token/get-current-user/`
- **方法**: `POST`
- **需要认证**: ✅

```bash
# Headers
Authorization: Bearer your_access_token
```

```json
// 响应示例
{
    "code": 200,
    "data": {
        "username": "testuser",
        "nickname": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "roles": [
            {
                "role_name": "admin",
                "app_name": "your_app",
                "app_id": 1
            }
        ]
    }
}
```

#### 2. 刷新访问令牌
- **URL**: `/api/token/refresh-token/`
- **方法**: `POST`

```json
// 请求参数
{
    "refresh_token": "your_refresh_token"
}

// 响应示例
{
    "code": 200,
    "data": {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token"
    }
}
```

#### 3. 验证令牌（请求体方式）
- **URL**: `/api/token/check-token-from-body/`
- **方法**: `POST`

```json
// 请求参数
{
    "access_token": "your_access_token"
}

// 响应示例
{
    "code": 200,
    "data": {
        "username": "testuser",
        "nickname": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "roles": [
            {
                "role_name": "admin",
                "app_name": "your_app",
                "app_id": 1
            }
        ]
    }
}
```

#### 4. 验证令牌（请求头方式）
- **URL**: `/api/token/check-token-from-header/`
- **方法**: `POST`
- **需要认证**: ✅

```bash
# Headers
Authorization: Bearer your_access_token
```

```json
// 响应示例（同请求体方式）
{
    "code": 200,
    "data": {
        "username": "testuser",
        "nickname": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "roles": [
            {
                "role_name": "admin",
                "app_name": "your_app",
                "app_id": 1
            }
        ]
    }
}
```

### 👥 用户权限管理API

#### 1. 分配或创建角色
- **URL**: `/api/roles/assign-role/`
- **方法**: `POST`

```json
// 请求参数
{
    "user_id": 1,
    "role_name": "admin",
    "app_name": "your_app"
}

// 响应示例
{
    "code": 200,
    "data": {
        "status": true,
        "message": "角色分配成功"
    }
}
```

#### 2. 验证用户角色
- **URL**: `/api/roles/role-auth/`
- **方法**: `POST`
- **需要认证**: ✅

```json
// 请求参数
{
    "role_name": "admin",
    "app_name": "your_app"
}

// 响应示例
{
    "code": 200,
    "data": {
        "status": true
    }
}
```

#### 3. Admin角色验证示例
- **URL**: `/api/roles/admin-data/`
- **方法**: `GET`
- **需要认证**: ✅（需要admin角色）

```json
// 响应示例
{
    "code": 200,
    "data": "This is admin data"
}
```

### 🚪 用户登出

#### 退出登录
- **URL**: `/api/account/logout`
- **方法**: `GET`

```json
// 响应示例
{
    "code": 200,
    "data": "退出成功"
}
```

## 🛡️ 权限管理

### 1. 基本概念

- **用户 (User)**: 系统中的个人账户
- **角色 (Role)**: 权限的集合，如 admin、user、editor 等
- **应用 (App)**: 不同的应用系统，支持多应用权限隔离

### 2. 权限验证装饰器

```python
from svc_user_auth_zxw import require_role, require_roles, get_current_user
from fastapi import Depends


# 单个角色验证
@app.get("/admin-only")
async def admin_endpoint(user=Depends(require_role("admin", "your_app"))):
  return {"message": "只有admin可以访问"}


# 多个角色验证
@app.get("/multi-roles")
async def multi_roles_endpoint(user=Depends(require_roles(["admin", "moderator"], "your_app"))):
  return {"message": "admin或moderator可以访问"}


# 获取当前用户
@app.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
  return {"user": current_user.username}
```

### 3. 角色管理代码示例

#### 删除用户角色（代码调用）

```python
from svc_user_auth_zxw.apis.api_用户权限_增加 import delete_role, delete_roles

# 删除单个角色
await delete_role(user_id=1, role_name="admin", db=db_session)

# 批量删除角色
await delete_roles(user_id=1, role_names=["admin", "editor"], db=db_session)
```

### 4. 高级权限管理示例

参考 `useExamples/api_权限管理.py` 中的权限管理实现：

```python
from svc_user_auth_zxw import add_new_role, require_roles, get_current_user
from svc_user_auth_zxw.apis.schemas import 请求_分配或创建角色


# 新增权限
async def 新增权限_教案(user: User, db: AsyncSession, 新增数量: int):
  for i in range(1, 新增数量 + 1):
    await add_new_role(
      请求_分配或创建角色(
        user_id=user.id,
        role_name=f"gen_content_{i}",
        app_name="your_app"
      ),
      db=db
    )


# 使用权限
async def 使用权限_教案(user: User, db: AsyncSession):
  await require_roles(["gen_content_1"], "your_app")(user, db)
  # 权限使用后可以选择性删除
  await delete_roles(user.id, ["gen_content_1"], db)
```

## 🎨 前端集成

### 1. Vue-Element-Plus-Admin 框架集成

该库已适配 Vue-Element-Plus-Admin 框架的 API 标准格式：

```javascript
// API 返回格式
{
    "code": 200,
    "data": {
        // 实际数据
    }
}
```

### 2. 前端登录示例

```javascript
// 登录函数
async function login(username, password) {
    const response = await fetch('/user_center/api/account/normal/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });
    
    const result = await response.json();
    if (result.code === 200) {
        localStorage.setItem('access_token', result.data.access_token);
        localStorage.setItem('refresh_token', result.data.refresh_token);
        return result.data.user_info;
    }
    throw new Error(result.message);
}

// 请求拦截器
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 响应拦截器（自动刷新Token）
axios.interceptors.response.use(
    response => response,
    async error => {
        if (error.response?.status === 401) {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post('/user_center/api/token/refresh-token/', {
                        refresh_token: refreshToken
                    });
                    const { access_token, refresh_token } = response.data.data;
                    localStorage.setItem('access_token', access_token);
                    localStorage.setItem('refresh_token', refresh_token);
                    // 重试原请求
                    return axios.request(error.config);
                } catch {
                    // 刷新失败，跳转到登录页
                    localStorage.clear();
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);
```

## 🚀 高级功能

### 1. 短信验证码

库集成了阿里云短信服务，支持验证码发送和验证：

```python
# 发送验证码 API 会自动处理
# 验证时在登录/注册接口传入 sms_code 参数
```

### 2. 微信登录

支持微信公众号扫码登录：

```python
# 获取二维码
# POST /user_center/api/account/wechat/qr-login/get-qrcode

# 微信登录
# POST /user_center/api/account/wechat/qr-login/login/
{
    "code": "微信返回的code",
    "app_name": "your_app"
}
```

### 3. 邀请系统

支持用户邀请功能，注册时可以指定邀请人：

```python
{
    "phone": "13800138000",
    "sms_code": "123456",
    "referer_id": 123  # 邀请人用户ID
}
```

## ⚠️ 错误处理

库使用统一的错误处理机制：

```python
from svc_user_auth_zxw.tools.http_exception import HTTPException_VueElementPlusAdmin
from app_tools_zxw.Errors.api_errors import ErrorCode

# 自定义错误处理
try:
  # 业务逻辑
  pass
except HTTPException_VueElementPlusAdmin as e:
  # 统一错误格式
  return {"code": e.detail["code"], "data": e.detail["data"]}
```

### 完整错误代码说明

#### HTTP状态码说明
- `200`: 成功
- `400`: 请求参数错误
- `401`: 未授权（Token无效或过期）
- `403`: 权限不足
- `404`: 资源未找到
- `500`: 服务器内部错误

#### 业务错误代码详解

**用户认证相关错误（400状态码）**
- `用户名已注册`: 注册时用户名已存在
- `手机号已注册`: 注册时手机号已存在  
- `邮箱已注册`: 注册时邮箱已存在
- `无效的用户名或密码`: 登录时用户名或密码错误
- `无效的手机号或验证码`: 手机登录时手机号或验证码错误
- `用户未找到`: 操作的用户不存在（404状态码）

**Token认证相关错误（401状态码）**
- `token验证失败`: JWT Token验证失败或已过期
- `jwt解码错误`: JWT解码时发生错误
- `Token已过期`: Token超过有效期

**验证码相关错误**
- `验证码发送失败`: 短信验证码发送失败（500状态码）
- `验证码验证失败`: 验证码错误或已过期（400状态码）
- `验证码已过期`: 验证码超过5分钟有效期（400状态码）

**微信登录相关错误**
- `微信登录失败`: 微信授权登录失败（400状态码）
- `生成二维码失败`: 微信二维码生成失败（500状态码）
- `微信授权码无效`: 微信返回的授权码无效（400状态码）

**权限管理相关错误（403状态码）**
- `角色未找到`: 操作的角色不存在（404状态码）
- `角色创建失败`: 新建角色时失败（500状态码）
- `应用未找到`: 操作的应用不存在（403/404状态码）
- `权限不足`: 用户没有执行该操作的权限（403状态码）

**数据库相关错误（500状态码）**
- `数据创建失败`: 数据库创建记录失败
- `数据库连接失败`: 数据库连接异常
- `唯一约束违反`: 违反数据库唯一性约束
- `外键约束违反`: 违反数据库外键约束

**业务逻辑错误（400状态码）**
- `商品名称不能为空`: 业务逻辑参数验证失败
- `参数格式错误`: 请求参数格式不正确
- `必填参数缺失`: 缺少必要的请求参数

**服务器错误（500状态码）**
- `内部服务器错误`: 服务器内部未处理的异常
- `第三方服务调用失败`: 调用外部服务（如阿里云短信）失败
- `配置错误`: 服务器配置不正确

#### 错误响应格式

```json
{
    "code": 400,
    "data": "具体错误信息描述"
}
```

#### 前端错误处理示例

```javascript
// Axios 响应拦截器
axios.interceptors.response.use(
    response => {
        // 成功响应
        if (response.data.code === 200) {
            return response.data.data;
        }
        // 业务错误
        throw new Error(response.data.data);
    },
    error => {
        // HTTP错误
        if (error.response?.status === 401) {
            // Token过期，跳转登录
            localStorage.clear();
            window.location.href = '/login';
        } else if (error.response?.status === 403) {
            // 权限不足
            ElMessage.error('权限不足，请联系管理员');
        } else if (error.response?.status === 400) {
            // 业务逻辑错误
            ElMessage.error(error.response?.data?.data || '请求参数错误');
        } else if (error.response?.status === 500) {
            // 服务器错误
            ElMessage.error('服务器内部错误，请稍后重试');
        } else {
            // 其他错误
            ElMessage.error(error.response?.data?.data || '请求失败');
        }
        return Promise.reject(error);
    }
);
```

#### UniApp 错误处理示例

```typescript
const request = (url, method, data = null) => {
    return new Promise((resolve, reject) => {
        uni.request({
            url: `${BASE_URL}${url}`,
            method,
            data,
            header: setHeaderToken(),
            success: (res) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(res.data)
                } else {
                    const error_detail = res.data["detail"];
                    uni.showToast({
                        title: `请求失败: ${error_detail.code}, ${error_detail.data}`,
                        icon: 'none',
                        duration: 3000
                    })
                    reject(new Error(`请求失败: ${error_detail.code}, ${error_detail.data}`))
                }
            },
            fail: (err) => {
                console.error('网络请求错误:', err)
                uni.showToast({
                    title: `网络请求失败，请检查网络连接或服务器地址`,
                    icon: 'none',
                    duration: 3000
                })
                reject(new Error('网络请求失败，请检查网络连接或服务器地址'))
            }
        })
    })
}
```

## 🚀 部署注意事项

### 1. 环境变量

确保设置以下环境变量：

```bash
export USER_CENTER_DATABASE_URL="postgresql+asyncpg://user:pass@host:port/db"
export REDIS_URL_AUTH="redis://:password@host:port/db"
```

### 2. 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
alembic upgrade head
```

### 3. 生产环境配置

- 使用强密码和复杂的 JWT Secret Key
- 配置合适的 Token 过期时间
- 设置 Redis 密码和访问控制
- 配置 HTTPS

### 4. 注意事项

1. **Token安全**: 访问令牌应安全存储，避免XSS攻击
2. **刷新令牌**: 刷新令牌有效期更长，应妥善保管
3. **权限隔离**: 不同应用的权限相互隔离
4. **验证码**: 短信验证码有效期为5分钟
5. **并发限制**: 建议对发送验证码等敏感操作进行频率限制

## 📁 示例项目

完整的使用示例请参考项目中的 `useExamples` 目录：

- `main.py`: FastAPI 应用集成示例
- `api_权限管理.py`: 高级权限管理示例

## 👨‍💻 技术支持

- **作者**: 张薛伟 (Zhang Xuewei)
- **邮箱**: shuiheyangguang@gmail.com
- **GitHub**: https://github.com/sunshineinwater/

## 📄 许可证

MIT License
