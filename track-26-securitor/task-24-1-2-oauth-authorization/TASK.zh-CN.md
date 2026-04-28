# 实现 OAuth 2.0 授权流程

英文标题：Implement OAuth 2.0 Authorization Flow
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-2-oauth-authorization>

课程：26. 安全器
任务序号：2
短标题：OAuth 2.0 授权
难度：高级
子主题：认证与授权

## 中文导读

这道题要求你实现 OAuth 2.0 的授权码流程。OAuth 2.0 允许用户在不暴露密码的前提下，授予第三方应用对其账户的有限访问权限。这是现代互联网应用中最常见的授权方案，几乎所有"使用微信登录""使用 GitHub 登录"的场景背后都是它。

## 题目说明

OAuth 2.0 允许用户在不分享密码的情况下，授予第三方应用对其账户的有限访问权限。在授权码流程中，用户首先被引导到认证服务器进行身份验证和授权，认证服务器签发一个短期有效的授权码（Authorization Code），然后应用在服务端之间用这个授权码换取访问令牌（Access Token）。

可以把这个过程想象成酒店的房卡系统：你在前台（认证服务器）出示身份证后，前台给你一张房卡（令牌），这张房卡只能开指定的房间（权限范围）。第三方应用拿到的是房卡而非身份证，所以它只能在授权范围内操作，不能冒充你做其他事。

你需要实现一个节点来处理 OAuth 2.0 授权码流程：

```json
// 第一步：生成授权链接，将用户重定向过去
{ "type": "generate_auth_url", "msg_id": 1,
  "client_id": "abc123", "redirect_uri": "https://app.com/callback",
  "scopes": ["read","write"], "state": "xyz789" }
-> { "type": "auth_url_generated", "in_reply_to": 1,
    "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789" }

// 第二步：用户同意授权 -> 用授权码换取令牌
{ "type": "exchange_code", "msg_id": 2,
  "code": "AUTH_CODE", "redirect_uri": "https://app.com/callback",
  "client_id": "abc123", "client_secret": "secret" }
-> { "type": "token_issued", "in_reply_to": 2,
    "access_token": "<token>", "token_type": "Bearer",
    "expires_in": 3600 }

// 验证令牌是否具有所需的权限范围
{ "type": "check_scope", "msg_id": 3,
  "token": "ACCESS_TOKEN", "required_scope": "write" }
-> { "type": "scope_valid", "in_reply_to": 3, "has_scope": true }
```

PKCE（Proof Key for Code Exchange）是对授权码流程的安全增强，通过在请求中加入一个随机生成的校验码，防止授权码在传输过程中被截获后滥用。state 参数则用于防范跨站请求伪造攻击（CSRF），回调时需验证其是否与原始请求中的值匹配。

## 涉及概念

- OAuth 2.0
- authorization code flow
- PKCE
- access token
- scope
- token refresh

## 实现提示

- 授权链接必须包含：response_type=code、client_id、redirect_uri、scope（空格分隔）、state
- 授权链接中的 redirect_uri 需要进行 URL 编码
- 令牌交换：向 /token 端点发送 POST 请求，携带 code、redirect_uri、client_id、client_secret
- check_scope：验证令牌是否包含所需的权限范围字符串
- state 参数用于防范 CSRF 攻击，回调时需验证其是否匹配

## 测试用例

### 1. 生成授权链接

链接必须包含所有必需参数，且 redirect_uri 需要 URL 编码。

输入：

```json
{"src":"client","dest":"oauth","body":{"type":"generate_auth_url","msg_id":1,"client_id":"abc123","redirect_uri":"https://app.com/callback","scopes":["read","write"],"state":"xyz789"}}
```

期望输出：

```text
{"type": "auth_url_generated", "in_reply_to": 1, "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789"}
```

### 2. 用授权码换取令牌

有效的授权码应当换取到一个 Bearer 类型的访问令牌。

输入：

```json
{"src":"client","dest":"oauth","body":{"type":"exchange_code","msg_id":1,"code":"AUTH_CODE","redirect_uri":"https://app.com/callback","client_id":"abc123","client_secret":"secret"}}
```

期望输出：

```text
{"type": "token_issued", "in_reply_to": 1, "access_token": "[A-Za-z0-9-_]+", "token_type": "Bearer", "expires_in": 3600}
```

## 参考资料

- [OAuth 2.0](https://oauth.net/2/)：OAuth 2.0 框架概述及授权码流程说明
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)：授权码交换的证明密钥规范（RFC 7636）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
