# 实现基于角色的访问控制

英文标题：Implement Role-Based Access Control (RBAC)
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-4-role-based-access-control>

课程：26. 安全器
任务序号：4
短标题：基于角色的访问控制
难度：进阶
子主题：认证与授权

## 中文导读

这道题要求你实现基于角色的访问控制。RBAC 的核心思想是：将权限分配给角色，再将角色分配给用户，而不是把权限直接发给每个人。用户只有在持有授予了对应权限的角色时，才能对资源执行操作。这是企业级应用中最常见的权限管理模型。

## 题目说明

RBAC（Role-Based Access Control，基于角色的访问控制）将权限分配给角色，再将角色分配给用户。用户只有在拥有授予了对应权限的角色时，才能对资源执行某项操作。管理员拥有通配符权限，可以访问一切资源。

可以把 RBAC 想象成公司的门禁系统：不是给每个员工单独配一把钥匙，而是按角色发放门禁卡。"工程师"角色的卡能进实验室，"行政"角色的卡能进财务室，"管理员"角色的卡能进所有房间（通配符权限）。资源所有权是一个补充规则：你自己发布的文章，你当然可以编辑，不需要额外授权。

你需要实现一个节点来执行 RBAC 权限控制：

```json
// 检查用户是否有写入文章的权限
{ "type": "check_permission", "msg_id": 1,
  "user_id": "user123", "resource": "posts", "action": "write" }
-> { "type": "permission_check", "in_reply_to": 1,
    "allowed": true, "permission": "posts.write" }

// 管理员通配符权限允许所有操作
{ "type": "check_permission", "msg_id": 2,
  "user_id": "admin123", "resource": "settings", "action": "delete" }
-> { "type": "permission_check", "in_reply_to": 2,
    "allowed": true, "reason": "admin has wildcard permission" }

// 为用户分配角色
{ "type": "assign_role", "msg_id": 3,
  "user_id": "user123", "role": "moderator" }
-> { "type": "role_assigned", "in_reply_to": 3,
    "user_id": "user123", "role": "moderator",
    "roles": ["user", "moderator"] }

// 资源所有者始终可以编辑自己的资源
{ "type": "check_ownership", "msg_id": 4,
  "user_id": "user123", "resource": "posts",
  "resource_id": "post123", "action": "edit" }
-> { "type": "ownership_check", "in_reply_to": 4,
    "allowed": true, "reason": "resource owner" }
```

## 涉及概念

- RBAC
- roles
- permissions
- resource ownership
- wildcard permissions

## 实现提示

- 权限格式为：`资源.操作`（例如 "posts.write"、"settings.delete"）
- 管理员角色拥有通配符权限 "*"，可以访问所有资源
- assign_role 将角色添加给用户，并返回更新后的完整角色列表
- check_ownership：用户始终可以对自己拥有的资源执行操作
- 判断允许的条件：用户拥有所需权限，或者是资源的所有者

## 测试用例

### 1. 检查用户权限

拥有 posts.write 权限的用户应当被允许操作。

输入：

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"user123","resource":"posts","action":"write"}}
```

期望输出：

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "permission": "posts.write"}
```

### 2. 管理员通配符权限

管理员的通配符权限应当允许访问任何资源和操作。

输入：

```json
{"src":"api","dest":"rbac","body":{"type":"check_permission","msg_id":1,"user_id":"admin123","resource":"settings","action":"delete"}}
```

期望输出：

```text
{"type": "permission_check", "in_reply_to": 1, "allowed": true, "reason": "admin has wildcard permission"}
```

## 参考资料

- [Role-Based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control)：RBAC 模型介绍，包括角色、权限和分配
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)：OWASP 授权安全速查表

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
