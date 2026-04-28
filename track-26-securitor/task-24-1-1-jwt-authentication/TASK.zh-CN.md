# 实现 JWT Authentication System

英文标题：Implement JWT Authentication System
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-1-jwt-authentication>

课程：26. 安全器：认证、授权与加密
任务序号：1
短标题：JWT Auth
难度：intermediate
子主题：Authentication和Authorization

## 中文导读

本题要求你完成 `实现 JWT Authentication System`。

重点关注：`JWT`、`access token`、`refresh token`、`token verification`、`token expiry`。

建议先按提示逐步实现：JWT structure: base64url(header).base64url(payload).HMAC_signature。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

JWT (JSON Web Token) is a compact, self-contained token that proves identity without a 服务端-side session store. The 服务端 signs the payload，包含a secret key; any service that knows the secret can verify the token without a database lookup.

Implement a 节点 that issues, verifies,和refreshes JWTs:

```JSON
// Issue an access token (expires in 900s)
{ "type": "generate_access_token", "msg_id": 1,
  "payload": {"sub": "user123", "email": "user@example.com",
               "roles": ["user"]} }
-> { "type": "token_generated", "in_reply_to": 1,
    "access_token": "<header.payload.signature>",
    "expires_in": 900 }

// Verify a token's signature和expiry
{ "type": "verify_token", "msg_id": 2,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...." }
-> { "type": "token_valid", "in_reply_to": 2,
    "payload": {"sub": "user123", "email": "user@example.com"} }

// Expired token -> reject
{ "type": "verify_token", "msg_id": 3,
  "token": "...expired token..." }
-> { "type": "token_invalid", "in_reply_to": 3,
    "error": "Token expired" }

// Exchange refresh token用于new access token
{ "type": "refresh_token", "msg_id": 4,
  "refresh_token": "..." }
-> { "type": "token_refreshed", "in_reply_to": 4,
    "access_token": "<new token>", "expires_in": 900 }
```

## 涉及概念

- `JWT`
- `access token`
- `refresh token`
- `token verification`
- `token expiry`

## 实现提示

- JWT structure: base64url(header).base64url(payload).HMAC_signature
- Header: {"alg":"HS256","typ":"JWT"}; Payload: {"sub":"user123","iat":..., "exp":...}
- Verify by recomputing the signature和comparing; also check exp claim
- Access token expires in 900s (15 min); refresh token is long-lived
- Reject，包含{"type":"token_invalid","error":"Token expired"}用于expired tokens

## 测试用例

### 1. Generate access token

Should generate a three-part JWT和set expires_in=900.

输入：

```json
{"src":"auth","dest":"jwt","body":{"type":"generate_access_token","msg_id":1,"payload":{"sub":"user123","email":"user@example.com","roles":["user"]}}}
```

期望输出：

```text
{"type": "token_generated", "in_reply_to": 1, "access_token": ".*", "expires_in": 900}
```

### 2. Verify valid token

Valid token should return the decoded payload.

输入：

```json
{"src":"api","dest":"jwt","body":{"type":"verify_token","msg_id":1,"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNzA0MDY3MjAwfQ.signature"}}
```

期望输出：

```text
{"type": "token_valid", "in_reply_to": 1, "payload": {"sub": "user123", "email": "user@example.com"}}
```

## 参考资料

- [JSON Web Tokens](https://jwt.io/introduction)：JWT structure, signing algorithms,和best practices
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)：JWT Best Practices Current Practices (RFC 8725)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
