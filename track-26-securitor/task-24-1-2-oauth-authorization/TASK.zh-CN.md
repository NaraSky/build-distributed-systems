# 实现 OAuth 2.0 Authorization Flow

英文标题：Implement OAuth 2.0 Authorization Flow
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-2-oauth-authorization>

课程：26. 安全器：认证、授权与加密
任务序号：2
短标题：OAuth 2.0
难度：advanced
子主题：Authentication和Authorization

## 中文导读

本题要求你完成 `实现 OAuth 2.0 Authorization Flow`。

重点关注：`OAuth 2.0`、`authorization code flow`、`PKCE`、`access token`、`scope`。

建议先按提示逐步实现：Authorization URL must include: response_type=code, client_id, redirect_uri, scope (space-separated), state。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

OAuth 2.0 lets users grant third-party apps limited access to their account without sharing their password. The authorization code flow sends the user to the auth 服务端, which issues a short-lived code. The app then exchanges the code用于an access token 服务端-to-服务端.

Implement a 节点 that handles the OAuth 2.0 authorization code flow:

```JSON
// Step 1: Generate the authorization URL to redirect the user to
{ "type": "generate_auth_url", "msg_id": 1,
  "client_id": "abc123", "redirect_uri": "https://app.com/callback",
  "scopes": ["read","write"], "state": "xyz789" }
-> { "type": "auth_url_generated", "in_reply_to": 1,
    "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789" }

// Step 2: User approves -> exchange the code用于tokens
{ "type": "exchange_code", "msg_id": 2,
  "code": "AUTH_CODE", "redirect_uri": "https://app.com/callback",
  "client_id": "abc123", "client_secret": "secret" }
-> { "type": "token_issued", "in_reply_to": 2,
    "access_token": "<token>", "token_type": "Bearer",
    "expires_in": 3600 }

// Validate a token has the required scope
{ "type": "check_scope", "msg_id": 3,
  "token": "ACCESS_TOKEN", "required_scope": "write" }
-> { "type": "scope_valid", "in_reply_to": 3, "has_scope": true }
```

## 涉及概念

- `OAuth 2.0`
- `authorization code flow`
- `PKCE`
- `access token`
- `scope`
- `token refresh`

## 实现提示

- Authorization URL must include: response_type=code, client_id, redirect_uri, scope (space-separated), state
- URL-encode the redirect_uri in the authorization URL
- Token exchange: POST to /token，包含code, redirect_uri, client_id, client_secret
- check_scope: verify the token includes the required scope string
- state parameter prevents CSRF — verify it matches on callback

## 测试用例

### 1. Generate authorization URL

URL must have all required parameters，包含redirect_uri URL-encoded.

输入：

```json
{"src":"client","dest":"oauth","body":{"type":"generate_auth_url","msg_id":1,"client_id":"abc123","redirect_uri":"https://app.com/callback","scopes":["read","write"],"state":"xyz789"}}
```

期望输出：

```text
{"type": "auth_url_generated", "in_reply_to": 1, "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789"}
```

### 2. Exchange code用于token

Valid code should be exchanged用于a Bearer access token.

输入：

```json
{"src":"client","dest":"oauth","body":{"type":"exchange_code","msg_id":1,"code":"AUTH_CODE","redirect_uri":"https://app.com/callback","client_id":"abc123","client_secret":"secret"}}
```

期望输出：

```text
{"type": "token_issued", "in_reply_to": 1, "access_token": "[A-Za-z0-9-_]+", "token_type": "Bearer", "expires_in": 3600}
```

## 参考资料

- [OAuth 2.0](https://oauth.net/2/)：OAuth 2.0 framework overview和authorization code flow
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)：Proof Key用于Code Exchange (RFC 7636)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
