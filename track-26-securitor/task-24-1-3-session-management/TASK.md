# Implement Secure Session Management

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-3-session-management>

Track: 26. The Securitor
Task order: 3
Short title: Session Management
Difficulty: intermediate
Subtrack: Authentication and Authorization

## Problem

Sessions store authentication state server-side. After login, the server creates a session record keyed by a random ID and sends that ID to the client as a cookie. On every subsequent request, the client presents the ID and the server looks up the session.

Implement a node that manages server-side sessions:

```json
// Create a new session after successful login
{ "type": "create_session", "msg_id": 1, "user_id": "user123" }
-> { "type": "session_created", "in_reply_to": 1,
    "session_id": "<crypto-random-uuid>",
    "expires_at": <unix-timestamp> }

// Validate a session cookie on incoming request
{ "type": "validate_session", "msg_id": 2, "session_id": "abc123" }
-> { "type": "session_valid", "in_reply_to": 2,
    "user_id": "user123", "expires_in": 3600 }

// Regenerate session ID after privilege change (prevents fixation)
{ "type": "regenerate_session", "msg_id": 3, "old_session_id": "abc123" }
-> { "type": "session_regenerated", "in_reply_to": 3,
    "new_session_id": "<new-uuid>" }

// Destroy session on logout
{ "type": "destroy_session", "msg_id": 4, "session_id": "abc123" }
-> { "type": "session_destroyed", "in_reply_to": 4,
    "message": "Session destroyed" }
```

## Concepts

- session
- session ID
- session fixation
- session expiry
- session storage

## Hints

- Session ID must be cryptographically random (use uuid or similar)
- validate_session returns user_id and expires_in from the stored session
- regenerate_session creates a NEW random session_id and copies all session data to it
- destroy_session removes the session from storage permanently
- Session expiry: track created_at + ttl; return session_invalid if expired

## Test Cases

### 1. Create session

Should create session with random session_id and expiry timestamp.

Input:

```json
{"src":"auth","dest":"session","body":{"type":"create_session","msg_id":1,"user_id":"user123"}}
```

Expected output:

```text
{"type": "session_created", "in_reply_to": 1, "session_id": ".*", "expires_at": ".*"}
```

### 2. Validate session

Valid session_id should return user_id and remaining time.

Input:

```json
{"src":"api","dest":"session","body":{"type":"validate_session","msg_id":1,"session_id":"abc123"}}
```

Expected output:

```text
{"type": "session_valid", "in_reply_to": 1, "user_id": "user123", "expires_in": 3600}
```

## Resources

- [OWASP Session Management](https://owasp.org/www-community/attacks/Session_fixation): Session fixation attacks and how to prevent them

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
