# Implement JWT Authentication System

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-1-jwt-authentication>

Track: 26. The Securitor
Task order: 1
Short title: JWT Auth
Difficulty: intermediate
Subtrack: Authentication and Authorization

## Problem

JWT (JSON Web Token) is a compact, self-contained token that proves identity without a server-side session store. The server signs the payload with a secret key; any service that knows the secret can verify the token without a database lookup.

Implement a node that issues, verifies, and refreshes JWTs:

```json
// Issue an access token (expires in 900s)
{ "type": "generate_access_token", "msg_id": 1,
  "payload": {"sub": "user123", "email": "user@example.com",
               "roles": ["user"]} }
-> { "type": "token_generated", "in_reply_to": 1,
    "access_token": "<header.payload.signature>",
    "expires_in": 900 }

// Verify a token's signature and expiry
{ "type": "verify_token", "msg_id": 2,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...." }
-> { "type": "token_valid", "in_reply_to": 2,
    "payload": {"sub": "user123", "email": "user@example.com"} }

// Expired token -> reject
{ "type": "verify_token", "msg_id": 3,
  "token": "...expired token..." }
-> { "type": "token_invalid", "in_reply_to": 3,
    "error": "Token expired" }

// Exchange refresh token for new access token
{ "type": "refresh_token", "msg_id": 4,
  "refresh_token": "..." }
-> { "type": "token_refreshed", "in_reply_to": 4,
    "access_token": "<new token>", "expires_in": 900 }
```

## Concepts

- JWT
- access token
- refresh token
- token verification
- token expiry

## Hints

- JWT structure: base64url(header).base64url(payload).HMAC_signature
- Header: {"alg":"HS256","typ":"JWT"}; Payload: {"sub":"user123","iat":..., "exp":...}
- Verify by recomputing the signature and comparing; also check exp claim
- Access token expires in 900s (15 min); refresh token is long-lived
- Reject with {"type":"token_invalid","error":"Token expired"} for expired tokens

## Test Cases

### 1. Generate access token

Should generate a three-part JWT and set expires_in=900.

Input:

```json
{"src":"auth","dest":"jwt","body":{"type":"generate_access_token","msg_id":1,"payload":{"sub":"user123","email":"user@example.com","roles":["user"]}}}
```

Expected output:

```text
{"type": "token_generated", "in_reply_to": 1, "access_token": ".*", "expires_in": 900}
```

### 2. Verify valid token

Valid token should return the decoded payload.

Input:

```json
{"src":"api","dest":"jwt","body":{"type":"verify_token","msg_id":1,"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNzA0MDY3MjAwfQ.signature"}}
```

Expected output:

```text
{"type": "token_valid", "in_reply_to": 1, "payload": {"sub": "user123", "email": "user@example.com"}}
```

## Resources

- [JSON Web Tokens](https://jwt.io/introduction): JWT structure, signing algorithms, and best practices
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725): JWT Best Practices Current Practices (RFC 8725)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
