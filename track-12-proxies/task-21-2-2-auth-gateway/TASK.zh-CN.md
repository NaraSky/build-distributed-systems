# 实现 Authentication和Authorization at Gateway

英文标题：Implement Authentication和Authorization at Gateway
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-2-auth-gateway>

课程：12. 代理
任务序号：7
短标题：Gateway Auth
难度：advanced
子主题：API Gateway

## 中文导读

本题要求你完成 `实现 Authentication和Authorization at Gateway`。

重点关注：`API gateway authentication`、`JWT validation`、`OAuth2`、`authorization`、`centralized security`。

建议先按提示逐步实现：Validate JWT tokens at the gateway before routing to backend。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

API gateways centralize authentication和authorization logic, securing all backend services without duplicating auth code in each service.

**Authentication flow**:
```
1. 客户端 sends 请求，包含auth token
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

2. Gateway validates token signature和expiration
   - Decode JWT without verifying signature (get header)
   - Verify signature使用public key
   - Check expiration (exp claim)
   - Extract user claims (sub, name, roles, permissions)

3. Gateway enforces authorization
   - Check if user has required permissions
   - If authorized: add user context headers, forward to backend
   - If unauthorized: return 401/403 immediately

4. Backend receives 请求，包含user context
   X-User-ID: user123
   X-User-Role: admin
   X-User-Permissions: read,write,delete
```

**JWT validation**:
```typescript
function validateJWT(token: string): JWTClaims {
  try {
    // Decode和verify signature
    const claims = jwt.verify(token, publicKey);

    // Check expiration
    if (claims.exp < Date.now() / 1000) {
      throw new Error("Token expired");
    }

    // Check issuer
    if (claims.iss !== "https://auth.example.com") {
      throw new Error("Invalid issuer");
    }

    return claims;
  } catch (error) {
    throw new Error("Invalid token");
  }
}
```

**Example gateway auth**:
```JSON
// 请求，包含valid JWT:
请求:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."}}
响应: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "user_context": {"user_id": "user123", "role": "admin", "permissions": ["read", "write"]}}

// 请求，包含expired token:
请求:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer expired_token..."}}
响应: {"type": "api_response", "in_reply_to": 2, "status": 401, "error": "Token expired"}

// 请求 without permission:
请求:  {"type": "api_request", "msg_id": 3, "method": "DELETE", "path": "/api/users/123", "headers": {"Authorization": "Bearer user_token..."}, "required_permission": "delete"}
响应: {"type": "api_response", "in_reply_to": 3, "status": 403, "error": "Insufficient permissions: required [delete], have [read]"}
```

## 涉及概念

- `API gateway authentication`
- `JWT validation`
- `OAuth2`
- `authorization`
- `centralized security`
- `token validation`

## 实现提示

- Validate JWT tokens at the gateway before routing to backend
- Extract user claims (sub, roles, permissions) from token
- Enforce authorization: check permissions before allowing access
- Support multiple auth schemes: API keys, JWT, OAuth2 tokens
- Add user context headers to downstream requests

## 测试用例

### 1. Valid JWT passes through gateway

Valid JWT should result in 200 OK 响应，包含user_context headers added.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"jwt_public_key":"public_key_here"}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer valid_jwt_here"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Invalid JWT returns 401

Invalid JWT signature should return 401 Unauthorized.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer invalid_jwt"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 401, "error": "Invalid or expired token"}}
```

## 参考资料

- [API Gateway Authentication](https://auth0.com/docs/secure-applications/architecture-scenarios/api-gateway)：Auth0 documentation on API Gateway authentication patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
