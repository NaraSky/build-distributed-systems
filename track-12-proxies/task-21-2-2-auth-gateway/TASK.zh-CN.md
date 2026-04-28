# 在网关层实现认证与授权

英文标题：Implement Authentication and Authorization at Gateway
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-2-auth-gateway>

课程：12. 代理
任务序号：7
短标题：网关认证
难度：高级
子主题：API 网关

## 中文导读

这道题要求你在 API 网关层实现集中式的认证（Authentication）和授权（Authorization）。在微服务架构中，如果每个服务都各自实现一套认证逻辑，既重复又容易出错。通过在网关层统一处理认证和授权，后端服务可以专注于业务逻辑，而安全控制只需在一个地方维护。

## 题目说明

API 网关可以将认证和授权逻辑集中管理，在不需要每个后端服务都重复编写认证代码的情况下，保障所有服务的安全。

**认证流程**：
```
1. 客户端发送携带认证令牌的请求
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

2. 网关验证令牌的签名和有效期
   - 解码 JWT（先获取头部信息，不验证签名）
   - 使用公钥验证签名
   - 检查过期时间（exp 字段）
   - 提取用户声明信息（sub、name、roles、permissions）

3. 网关执行授权检查
   - 检查用户是否拥有所需权限
   - 如果授权通过：添加用户上下文头部，转发给后端
   - 如果授权失败：立即返回 401/403 错误

4. 后端收到带有用户上下文的请求
   X-User-ID: user123
   X-User-Role: admin
   X-User-Permissions: read,write,delete
```

**JWT 验证逻辑**：
```typescript
function validateJWT(token: string): JWTClaims {
  try {
    // 解码并验证签名
    const claims = jwt.verify(token, publicKey);

    // 检查是否过期
    if (claims.exp < Date.now() / 1000) {
      throw new Error("Token expired");
    }

    // 检查签发者
    if (claims.iss !== "https://auth.example.com") {
      throw new Error("Invalid issuer");
    }

    return claims;
  } catch (error) {
    throw new Error("Invalid token");
  }
}
```

**网关认证示例**：
```json
// 携带有效 JWT 的请求：
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."}}
Response: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "user_context": {"user_id": "user123", "role": "admin", "permissions": ["read", "write"]}}

// 携带过期令牌的请求：
Request:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer expired_token..."}}
Response: {"type": "api_response", "in_reply_to": 2, "status": 401, "error": "Token expired"}

// 权限不足的请求：
Request:  {"type": "api_request", "msg_id": 3, "method": "DELETE", "path": "/api/users/123", "headers": {"Authorization": "Bearer user_token..."}, "required_permission": "delete"}
Response: {"type": "api_response", "in_reply_to": 3, "status": 403, "error": "Insufficient permissions: required [delete], have [read]"}
```

## 涉及概念

- `API gateway authentication`
- `JWT validation`
- `OAuth2`
- `authorization`
- `centralized security`
- `token validation`

## 实现提示

- 在将请求路由到后端之前，先在网关层验证 JWT 令牌
- 从令牌中提取用户声明信息（sub、roles、permissions）
- 执行授权检查：在允许访问之前确认用户拥有所需权限
- 支持多种认证方案：API 密钥、JWT、OAuth2 令牌
- 在转发给下游服务的请求中添加用户上下文头部

## 测试用例

### 1. 有效 JWT 通过网关

有效的 JWT 应该返回 200 OK 响应，并附带用户上下文头部。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"jwt_public_key":"public_key_here"}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer valid_jwt_here"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 无效 JWT 返回 401

无效的 JWT 签名应返回 401 未授权错误。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer invalid_jwt"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 401, "error": "Invalid or expired token"}}
```

## 参考资料

- [API Gateway Authentication](https://auth0.com/docs/secure-applications/architecture-scenarios/api-gateway)：Auth0 上关于 API 网关认证模式的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
