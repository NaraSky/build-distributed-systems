# 实现 JWT 认证系统

英文标题：Implement JWT Authentication System
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-1-jwt-authentication>

课程：26. 安全器
任务序号：1
短标题：JWT 认证
难度：进阶
子主题：认证与授权

## 中文导读

这道题要求你实现一个基于 JWT 的认证系统，包括令牌的签发、验证和刷新。JWT 是分布式系统中最常用的身份认证方案之一，它的核心优势是无需服务端存储会话状态，任何知道密钥的服务都可以独立验证令牌的有效性。

## 题目说明

JWT（JSON Web Token）是一种紧凑的、自包含的令牌，能在不依赖服务端会话存储的情况下证明用户身份。服务端用密钥对载荷进行签名，之后任何知道该密钥的服务都可以直接验证令牌，无需查询数据库。

可以把 JWT 想象成一张加密的身份名片：上面写着你是谁、有什么权限，并且盖了服务器的"印章"（签名）。拿到这张名片的任何服务只要能验证印章的真伪，就能确认你的身份，不需要再去数据库核实。访问令牌有效期短（通常 15 分钟），过期后用刷新令牌换取新的，这样即使令牌泄露，影响范围也有限。

你需要实现一个节点来签发、验证和刷新 JWT：

```json
// 签发一个访问令牌（900 秒后过期）
{ "type": "generate_access_token", "msg_id": 1,
  "payload": {"sub": "user123", "email": "user@example.com",
               "roles": ["user"]} }
-> { "type": "token_generated", "in_reply_to": 1,
    "access_token": "<header.payload.signature>",
    "expires_in": 900 }

// 验证令牌的签名和有效期
{ "type": "verify_token", "msg_id": 2,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...." }
-> { "type": "token_valid", "in_reply_to": 2,
    "payload": {"sub": "user123", "email": "user@example.com"} }

// 过期的令牌 -> 拒绝
{ "type": "verify_token", "msg_id": 3,
  "token": "...expired token..." }
-> { "type": "token_invalid", "in_reply_to": 3,
    "error": "Token expired" }

// 用刷新令牌换取新的访问令牌
{ "type": "refresh_token", "msg_id": 4,
  "refresh_token": "..." }
-> { "type": "token_refreshed", "in_reply_to": 4,
    "access_token": "<new token>", "expires_in": 900 }
```

## 涉及概念

- JWT
- access token
- refresh token
- token verification
- token expiry

## 实现提示

- JWT 的结构为：`base64url(header).base64url(payload).HMAC_signature`
- 头部：`{"alg":"HS256","typ":"JWT"}`；载荷：`{"sub":"user123","iat":..., "exp":...}`
- 验证时需要重新计算签名并比对，同时检查 exp 声明是否过期
- 访问令牌有效期为 900 秒（15 分钟）；刷新令牌的有效期较长
- 过期令牌应返回 `{"type":"token_invalid","error":"Token expired"}`

## 测试用例

### 1. 签发访问令牌

应当生成一个由三部分组成的 JWT，并设置 expires_in=900。

输入：

```json
{"src":"auth","dest":"jwt","body":{"type":"generate_access_token","msg_id":1,"payload":{"sub":"user123","email":"user@example.com","roles":["user"]}}}
```

期望输出：

```text
{"type": "token_generated", "in_reply_to": 1, "access_token": ".*", "expires_in": 900}
```

### 2. 验证有效令牌

有效的令牌应当返回解码后的载荷内容。

输入：

```json
{"src":"api","dest":"jwt","body":{"type":"verify_token","msg_id":1,"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNzA0MDY3MjAwfQ.signature"}}
```

期望输出：

```text
{"type": "token_valid", "in_reply_to": 1, "payload": {"sub": "user123", "email": "user@example.com"}}
```

## 参考资料

- [JSON Web Tokens](https://jwt.io/introduction)：介绍 JWT 的结构、签名算法和最佳实践
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)：JWT 最佳实践指南（RFC 8725）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
