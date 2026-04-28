# 实现 API 安全 Best Practices

英文标题：Implement API Security Best Practices
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-5-api-security>

课程：26. 安全器：认证、授权与加密
任务序号：5
短标题：API 安全
难度：advanced
子主题：Authentication和Authorization

## 中文导读

本题要求你完成 `实现 API 安全 Best Practices`。

重点关注：`rate limiting`、`input validation`、`SQL injection prevention`、`security headers`、`OWASP`。

建议先按提示逐步实现：Rate limiting: track 请求 count per IP per window; block once count > limit。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

API security is a set of layers: rate limiting prevents abuse, input validation rejects malformed data before it reaches business logic, parameterised queries prevent SQL injection,和security headers protect browsers from common attacks.

Implement a 节点 that enforces all four security layers:

```JSON
// Rate limiting: 100 requests per minute per IP
{ "type": "rate_limit_test", "msg_id": 1,
  "requests": 105, "window": "1m" }
-> { "type": "rate_limit_exceeded", "in_reply_to": 1,
    "allowed_requests": 100, "blocked_requests": 5 }

// Input validation: report all errors at once
{ "type": "create_user", "msg_id": 2,
  "email": "invalid-email", "password": "weak" }
-> { "type": "validation_error", "in_reply_to": 2,
    "errors": [{"field":"email","消息":"Invalid email format"},
                {"field":"password","消息":"Password must be at least 8 characters"}] }

// SQL injection attempt -> safe empty result (parameterised query)
{ "type": "search_users", "msg_id": 3,
  "email": "' OR '1'='1" }
-> { "type": "search_results", "in_reply_to": 3, "users": [] }

// Security headers on every 响应
{ "type": "get_options", "msg_id": 4 }
-> { "type": "options", "in_reply_to": 4,
    "headers": {"X-Frame-Options":"DENY",
                 "X-Content-Type-Options":"nosniff",
                 "Strict-Transport-Security":"max-age=31536000"} }
```

## 涉及概念

- `rate limiting`
- `input validation`
- `SQL injection prevention`
- `security headers`
- `OWASP`

## 实现提示

- Rate limiting: track 请求 count per IP per window; block once count > limit
- Input validation: check field types和formats before processing (email regex, min password length)
- SQL injection: use parameterised queries — never interpolate user input into SQL strings
- Security headers: X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security
- Return all validation errors together in the errors array, not just the first one

## 测试用例

### 1. Rate limiting

105 requests，包含limit 100 should block 5.

输入：

```json
{"src":"attacker","dest":"api","body":{"type":"rate_limit_test","msg_id":1,"requests":105,"window":"1m"}}
```

期望输出：

```text
{"type": "rate_limit_exceeded", "in_reply_to": 1, "allowed_requests": 100, "blocked_requests": 5}
```

### 2. Input 校验

Both validation errors should be returned together.

输入：

```json
{"src":"client","dest":"api","body":{"type":"create_user","msg_id":1,"email":"invalid-email","password":"weak"}}
```

期望输出：

```text
{"type": "validation_error", "in_reply_to": 1, "errors": [{"field": "email", "message": "Invalid email format"}, {"field": "password", "message": "Password must be at least 8 characters"}]}
```

## 参考资料

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)：The ten most critical web application security risks
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)：OWASP Cheat Sheet Series

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
