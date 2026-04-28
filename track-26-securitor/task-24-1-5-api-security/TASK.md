# Implement API Security Best Practices

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-5-api-security>

Track: 26. The Securitor
Task order: 5
Short title: API Security
Difficulty: advanced
Subtrack: Authentication and Authorization

## Problem

API security is a set of layers: rate limiting prevents abuse, input validation rejects malformed data before it reaches business logic, parameterised queries prevent SQL injection, and security headers protect browsers from common attacks.

Implement a node that enforces all four security layers:

```json
// Rate limiting: 100 requests per minute per IP
{ "type": "rate_limit_test", "msg_id": 1,
  "requests": 105, "window": "1m" }
-> { "type": "rate_limit_exceeded", "in_reply_to": 1,
    "allowed_requests": 100, "blocked_requests": 5 }

// Input validation: report all errors at once
{ "type": "create_user", "msg_id": 2,
  "email": "invalid-email", "password": "weak" }
-> { "type": "validation_error", "in_reply_to": 2,
    "errors": [{"field":"email","message":"Invalid email format"},
                {"field":"password","message":"Password must be at least 8 characters"}] }

// SQL injection attempt -> safe empty result (parameterised query)
{ "type": "search_users", "msg_id": 3,
  "email": "' OR '1'='1" }
-> { "type": "search_results", "in_reply_to": 3, "users": [] }

// Security headers on every response
{ "type": "get_options", "msg_id": 4 }
-> { "type": "options", "in_reply_to": 4,
    "headers": {"X-Frame-Options":"DENY",
                 "X-Content-Type-Options":"nosniff",
                 "Strict-Transport-Security":"max-age=31536000"} }
```

## Concepts

- rate limiting
- input validation
- SQL injection prevention
- security headers
- OWASP

## Hints

- Rate limiting: track request count per IP per window; block once count > limit
- Input validation: check field types and formats before processing (email regex, min password length)
- SQL injection: use parameterised queries — never interpolate user input into SQL strings
- Security headers: X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security
- Return all validation errors together in the errors array, not just the first one

## Test Cases

### 1. Rate limiting

105 requests with limit 100 should block 5.

Input:

```json
{"src":"attacker","dest":"api","body":{"type":"rate_limit_test","msg_id":1,"requests":105,"window":"1m"}}
```

Expected output:

```text
{"type": "rate_limit_exceeded", "in_reply_to": 1, "allowed_requests": 100, "blocked_requests": 5}
```

### 2. Input validation

Both validation errors should be returned together.

Input:

```json
{"src":"client","dest":"api","body":{"type":"create_user","msg_id":1,"email":"invalid-email","password":"weak"}}
```

Expected output:

```text
{"type": "validation_error", "in_reply_to": 1, "errors": [{"field": "email", "message": "Invalid email format"}, {"field": "password", "message": "Password must be at least 8 characters"}]}
```

## Resources

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/): The ten most critical web application security risks
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/): OWASP Cheat Sheet Series

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
