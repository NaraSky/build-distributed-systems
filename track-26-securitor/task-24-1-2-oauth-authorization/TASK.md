# Implement OAuth 2.0 Authorization Flow

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-2-oauth-authorization>

Track: 26. The Securitor
Task order: 2
Short title: OAuth 2.0
Difficulty: advanced
Subtrack: Authentication and Authorization

## Problem

OAuth 2.0 lets users grant third-party apps limited access to their account without sharing their password. The authorization code flow sends the user to the auth server, which issues a short-lived code. The app then exchanges the code for an access token server-to-server.

Implement a node that handles the OAuth 2.0 authorization code flow:

```json
// Step 1: Generate the authorization URL to redirect the user to
{ "type": "generate_auth_url", "msg_id": 1,
  "client_id": "abc123", "redirect_uri": "https://app.com/callback",
  "scopes": ["read","write"], "state": "xyz789" }
-> { "type": "auth_url_generated", "in_reply_to": 1,
    "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789" }

// Step 2: User approves -> exchange the code for tokens
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

## Concepts

- OAuth 2.0
- authorization code flow
- PKCE
- access token
- scope
- token refresh

## Hints

- Authorization URL must include: response_type=code, client_id, redirect_uri, scope (space-separated), state
- URL-encode the redirect_uri in the authorization URL
- Token exchange: POST to /token with code, redirect_uri, client_id, client_secret
- check_scope: verify the token includes the required scope string
- state parameter prevents CSRF — verify it matches on callback

## Test Cases

### 1. Generate authorization URL

URL must have all required parameters with redirect_uri URL-encoded.

Input:

```json
{"src":"client","dest":"oauth","body":{"type":"generate_auth_url","msg_id":1,"client_id":"abc123","redirect_uri":"https://app.com/callback","scopes":["read","write"],"state":"xyz789"}}
```

Expected output:

```text
{"type": "auth_url_generated", "in_reply_to": 1, "url": "https://accounts.example.com/authorize?response_type=code&client_id=abc123&redirect_uri=https%3A%2F%2Fapp.com%2Fcallback&scope=read+write&state=xyz789"}
```

### 2. Exchange code for token

Valid code should be exchanged for a Bearer access token.

Input:

```json
{"src":"client","dest":"oauth","body":{"type":"exchange_code","msg_id":1,"code":"AUTH_CODE","redirect_uri":"https://app.com/callback","client_id":"abc123","client_secret":"secret"}}
```

Expected output:

```text
{"type": "token_issued", "in_reply_to": 1, "access_token": "[A-Za-z0-9-_]+", "token_type": "Bearer", "expires_in": 3600}
```

## Resources

- [OAuth 2.0](https://oauth.net/2/): OAuth 2.0 framework overview and authorization code flow
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636): Proof Key for Code Exchange (RFC 7636)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
