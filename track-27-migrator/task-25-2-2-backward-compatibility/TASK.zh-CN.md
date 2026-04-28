# 实现 Backward-Compatible API Changes

英文标题：Implement Backward-Compatible API Changes
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-2-backward-compatibility>

课程：27. 迁移器：数据与协议演进
任务序号：7
短标题：Backward Compatibility
难度：intermediate
子主题：Protocol和API Evolution

## 中文导读

本题要求你完成 `实现 Backward-Compatible API Changes`。

重点关注：`backward compatibility`、`additive changes`、`field deprecation`、`consumer-driven contracts`。

建议先按提示逐步实现：Old clients must work without modification when new optional fields are added。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Backward compatibility means old clients continue to work after an API update. The golden rule: only make **additive** changes (new optional fields, new endpoints). Renaming, removing, or changing the type of existing fields breaks old clients.

Implement a 节点 that serves both old和new clients from the same endpoint:

```JSON
// v1 客户端: gets the fields it knows about (no new fields needed)
{ "type": "get_users", "msg_id": 1 }  // from client_v1
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1",
    "users": [{"id":1,"email":"user@example.com","name":"John Doe"}] }

// v2 客户端: gets new fields added in v2
{ "type": "get_users", "msg_id": 2 }  // from client_v2
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com",
               "full_name":"John Doe","phone":"+1234567890"}] }

// Deprecated field: return both old和new, flag old as deprecated
{ "type": "create_user", "msg_id": 3,
  "user": {"email":"new@example.com","name":"Jane"} }
-> { "type": "user_created", "in_reply_to": 3,
    "user": {"id":2,"full_name":"Jane"},
    "__deprecated": ["name"] }
```

## 涉及概念

- `backward compatibility`
- `additive changes`
- `field deprecation`
- `consumer-driven contracts`

## 实现提示

- Old clients must work without modification when new optional fields are added
- New clients receive the new fields; old clients ignore them
- Deprecated fields: return the old field alongside the new one, flag it in __deprecated
- Contract validation: ensure API 响应 matches the expected contract version
- Never remove or rename required fields — add new optional ones instead

## 测试用例

### 1. 添加 optional field (backward compatible)

Old 客户端 should receive only the fields it knows about.

输入：

```json
{"src":"client_v1","dest":"api","body":{"type":"get_users","msg_id":1}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "name": "John Doe"}], "version": "v1"}
```

### 2. New client uses new fields

New 客户端 should receive full_name和phone added in v2.

输入：

```json
{"src":"client_v2","dest":"api","body":{"type":"get_users","msg_id":1}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe", "phone": "+1234567890"}], "version": "v2"}
```

## 参考资料

- [Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html)：Testing backward compatibility，包含consumer-driven contract tests
- [OpenAPI Specification](https://swagger.io/specification/)：OpenAPI/Swagger specification

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
