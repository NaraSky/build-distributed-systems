# Implement Role-Based Access Control (RBAC)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-4-role-based-access-control>

Track: 26. The Securitor
Task order: 4
Short title: RBAC
Difficulty: intermediate
Subtrack: Authentication and Authorization

## Problem

RBAC assigns permissions to roles and roles to users. A user can perform an action on a resource only if they hold a role that grants that permission. Admins have a wildcard that grants everything.

Implement a node that enforces RBAC:

```json
// Check if user can write to posts
{ "type": "check_permission", "msg_id": 1,
  "user_id": "user123", "resource": "posts", "action": "write" }
-> { "type": "permission_check", "in_reply_to": 1,
    "allowed": true, "permission": "posts.write" }

// Admin wildcard grants any permission
{ "type": "check_permission", "msg_id": 2,
  "user_id": "admin123", "resource": "settings", "action": "delete" }
-> { "type": "permission_check", "in_reply_to": 2,
    "allowed": true, "reason": "admin has wildcard permission" }

// Assign a role to a user
{ "type": "assign_role", "msg_id": 3,
  "user_id": "user123", "role": "moderator" }
-> { "type": "role_assigned", "in_reply_to": 3,
    "user_id": "user123", "role": "moderator",
    "roles": ["user", "moderator"] }

// Owner can always edit their own resource
{ "type": "check_ownership", "msg_id": 4,
  "user_id": "user123", "resource": "posts",
  "resource_id": "post123", "action": "edit" }
-> { "type": "ownership_check", "in_reply_to": 4,
    "allowed": true, "reason": "resource owner" }
```

## Concepts

- RBAC
- roles
- permissions
- resource ownership
- wildcard permissions

## Hints

- Permission format: resource.action (e.g. "posts.write", "settings.delete")
- Admin role has wildcard permission "*" which grants access to everything
- assign_role adds the role to the user and returns the updated full roles list
- check_ownership: users can always perform actions on resources they own
- allowed is true if the user has the required permission OR is the resource owner

## Test Cases

### 1. Check user permission

User with posts.write permission should be allowed.

Input:

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"user123","resource":"posts","action":"write"}}
```

Expected output:

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "permission": "posts.write"}
```

### 2. Admin wildcard permission

Admin wildcard should grant access to any resource and action.

Input:

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"admin123","resource":"settings","action":"delete"}}
```

Expected output:

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "reason": "admin has wildcard permission"}
```

## Resources

- [Role-Based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control): RBAC model: roles, permissions, and assignment
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): OWASP Authorization Cheat Sheet

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
