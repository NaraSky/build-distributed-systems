# Implement Authentication and Authorization at Gateway

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-2-auth-gateway>

Track: 12. Proxies
Task order: 7
Short title: Gateway Auth
Difficulty: advanced
Subtrack: API Gateway

## Problem

API gateways centralize authentication and authorization logic, securing all backend services without duplicating auth code in each service.

**Authentication flow**:
```
1. Client sends request with auth token
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

2. Gateway validates token signature and expiration
   - Decode JWT without verifying signature (get header)
   - Verify signature using public key
   - Check expiration (exp claim)
   - Extract user claims (sub, name, roles, permissions)

3. Gateway enforces authorization
   - Check if user has required permissions
   - If authorized: add user context headers, forward to backend
   - If unauthorized: return 401/403 immediately

4. Backend receives request with user context
   X-User-ID: user123
   X-User-Role: admin
   X-User-Permissions: read,write,delete
```

**JWT validation**:
```typescript
function validateJWT(token: string): JWTClaims {
  try {
    // Decode and verify signature
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
```json
// Request with valid JWT:
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."}}
Response: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "user_context": {"user_id": "user123", "role": "admin", "permissions": ["read", "write"]}}

// Request with expired token:
Request:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/users/123", "headers": {"Authorization": "Bearer expired_token..."}}
Response: {"type": "api_response", "in_reply_to": 2, "status": 401, "error": "Token expired"}

// Request without permission:
Request:  {"type": "api_request", "msg_id": 3, "method": "DELETE", "path": "/api/users/123", "headers": {"Authorization": "Bearer user_token..."}, "required_permission": "delete"}
Response: {"type": "api_response", "in_reply_to": 3, "status": 403, "error": "Insufficient permissions: required [delete], have [read]"}
```

## Concepts

- API gateway authentication
- JWT validation
- OAuth2
- authorization
- centralized security
- token validation

## Hints

- Validate JWT tokens at the gateway before routing to backend
- Extract user claims (sub, roles, permissions) from token
- Enforce authorization: check permissions before allowing access
- Support multiple auth schemes: API keys, JWT, OAuth2 tokens
- Add user context headers to downstream requests

## Test Cases

### 1. Valid JWT passes through gateway

Valid JWT should result in 200 OK response with user_context headers added.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"jwt_public_key":"public_key_here"}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer valid_jwt_here"}}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Invalid JWT returns 401

Invalid JWT signature should return 401 Unauthorized.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Authorization":"Bearer invalid_jwt"}}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 401, "error": "Invalid or expired token"}}
```

## Resources

- [API Gateway Authentication](https://auth0.com/docs/secure-applications/architecture-scenarios/api-gateway): Auth0 documentation on API Gateway authentication patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
