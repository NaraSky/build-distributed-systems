# 实现 Role-Based Access Control (RBAC)

英文标题：Implement Role-Based Access Control (RBAC)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-4-role-based-access-control>

课程：26. 安全器：认证、授权与加密
任务序号：4
短标题：RBAC
难度：intermediate
子主题：Authentication和Authorization

## 中文导读

本题要求你完成 `实现 Role-Based Access Control (RBAC)`。

重点关注：`RBAC`、`roles`、`permissions`、`resource ownership`、`wildcard permissions`。

建议先按提示逐步实现：Permission format: resource.action (e.g. "posts.write", "settings.delete")。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

RBAC assigns permissions to roles和roles to users. A user can perform an action on a resource only if they hold a role that grants that permission. Admins have a wildcard that grants everything.

Implement a 节点 that enforces RBAC:

```JSON
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

## 涉及概念

- `RBAC`
- `roles`
- `permissions`
- `resource ownership`
- `wildcard permissions`

## 实现提示

- Permission format: resource.action (e.g. "posts.write", "settings.delete")
- Admin role has wildcard permission "*" which grants access to everything
- assign_role adds the role to the user和returns the updated full roles list
- check_ownership: users can always perform actions on resources they own
- allowed is true if the user has the required permission OR is the resource owner

## 测试用例

### 1. Check user permission

User，包含posts.write permission should be allowed.

输入：

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"user123","resource":"posts","action":"write"}}
```

期望输出：

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "permission": "posts.write"}
```

### 2. Admin wildcard permission

Admin wildcard should grant access to any resource和action.

输入：

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"admin123","resource":"settings","action":"delete"}}
```

期望输出：

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "reason": "admin has wildcard permission"}
```

## 参考资料

- [Role-Based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control)：RBAC model: roles, permissions,和assignment
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)：OWASP Authorization Cheat Sheet

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
