# 实现 API 安全最佳实践

英文标题：Implement API Security Best Practices
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-5-api-security>

课程：26. 安全器
任务序号：5
短标题：API 安全
难度：高级
子主题：认证与授权

## 中文导读

这道题要求你实现 API 安全的四个核心防护层：限流防止滥用、输入校验拒绝畸形数据、参数化查询防止 SQL 注入、安全响应头保护浏览器免受常见攻击。这些是每个面向互联网的 API 都必须具备的基本防护能力，也是 OWASP 安全指南的核心内容。

## 题目说明

API 安全是一套多层防护体系，每一层解决一类特定的安全威胁。限流（Rate Limiting）通过限制单位时间内的请求数量来防止滥用；输入校验在数据到达业务逻辑之前就拒绝格式不合法的请求；参数化查询将用户输入与 SQL 语句分离，从根本上杜绝 SQL 注入；安全响应头告诉浏览器如何防范点击劫持等攻击。

可以把 API 安全想象成银行的多道安全门：限流是门卫，超过来访频率的一律拦截；输入校验是安检机，检查携带物品是否合规；参数化查询是防弹玻璃，即使有人企图捣乱也无法伤害到内部系统；安全响应头是监控摄像头，告诉浏览器如何自我保护。每一层都不可或缺。

你需要实现一个节点来执行这四层安全防护：

```json
// 限流：每分钟每个 IP 最多 100 个请求
{ "type": "rate_limit_test", "msg_id": 1,
  "requests": 105, "window": "1m" }
-> { "type": "rate_limit_exceeded", "in_reply_to": 1,
    "allowed_requests": 100, "blocked_requests": 5 }

// 输入校验：一次性报告所有错误
{ "type": "create_user", "msg_id": 2,
  "email": "invalid-email", "password": "weak" }
-> { "type": "validation_error", "in_reply_to": 2,
    "errors": [{"field":"email","message":"Invalid email format"},
                {"field":"password","message":"Password must be at least 8 characters"}] }

// SQL 注入尝试 -> 参数化查询返回安全的空结果
{ "type": "search_users", "msg_id": 3,
  "email": "' OR '1'='1" }
-> { "type": "search_results", "in_reply_to": 3, "users": [] }

// 每个响应都携带安全头
{ "type": "get_options", "msg_id": 4 }
-> { "type": "options", "in_reply_to": 4,
    "headers": {"X-Frame-Options":"DENY",
                 "X-Content-Type-Options":"nosniff",
                 "Strict-Transport-Security":"max-age=31536000"} }
```

## 涉及概念

- rate limiting
- input validation
- SQL injection prevention
- security headers
- OWASP

## 实现提示

- 限流：按 IP 和时间窗口记录请求数量，超过上限后拦截后续请求
- 输入校验：在处理之前检查字段类型和格式（邮箱格式正则、最小密码长度）
- SQL 注入防范：使用参数化查询，绝不将用户输入直接拼接到 SQL 字符串中
- 安全响应头：X-Frame-Options、X-Content-Type-Options、Strict-Transport-Security
- 将所有校验错误一并返回在 errors 数组中，而不是只返回第一个

## 测试用例

### 1. 限流测试

105 个请求在上限为 100 的情况下，应当拦截 5 个。

输入：

```json
{"src":"attacker","dest":"api","body":{"type":"rate_limit_test","msg_id":1,"requests":105,"window":"1m"}}
```

期望输出：

```text
{"type": "rate_limit_exceeded", "in_reply_to": 1, "allowed_requests": 100, "blocked_requests": 5}
```

### 2. 输入校验

两个校验错误应当一并返回。

输入：

```json
{"src":"client","dest":"api","body":{"type":"create_user","msg_id":1,"email":"invalid-email","password":"weak"}}
```

期望输出：

```text
{"type": "validation_error", "in_reply_to": 1, "errors": [{"field": "email", "message": "Invalid email format"}, {"field": "password", "message": "Password must be at least 8 characters"}]}
```

## 参考资料

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)：十大最关键的 Web 应用安全风险
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)：OWASP 安全速查表系列

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
