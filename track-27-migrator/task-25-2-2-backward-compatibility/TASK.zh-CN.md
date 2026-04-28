# 实现向后兼容的 API 变更

英文标题：Implement Backward-Compatible API Changes
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-2-backward-compatibility>

课程：27. 迁移器：数据与协议演进
任务序号：7
短标题：Backward Compatibility
难度：进阶
子主题：Protocol and API Evolution

## 中文导读

这道题要求你实现一个能同时服务新旧客户端的节点。向后兼容（Backward Compatibility）的黄金法则是：只做"加法"变更，比如添加新的可选字段或新的接口端点。重命名、删除或修改现有字段的类型都会导致旧客户端崩溃。理解这个原则对于维护长期运行的分布式系统至关重要。

## 题目说明

向后兼容意味着 API 更新后，旧客户端仍然能正常工作。黄金法则是：只做**加法变更**（新增可选字段、新增端点）。重命名、删除或修改现有字段的类型都会破坏旧客户端。

请实现一个能从同一个端点同时服务新旧客户端的节点：

```json
// v1 客户端：只获取它认识的字段（不需要新字段）
{ "type": "get_users", "msg_id": 1 }  // 来自 client_v1
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1",
    "users": [{"id":1,"email":"user@example.com","name":"John Doe"}] }

// v2 客户端：获取 v2 新增的字段
{ "type": "get_users", "msg_id": 2 }  // 来自 client_v2
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com",
               "full_name":"John Doe","phone":"+1234567890"}] }

// 废弃字段：同时返回新旧字段，并标记旧字段为已废弃
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

- 添加新的可选字段后，旧客户端必须无需修改即可正常工作
- 新客户端接收新字段，旧客户端会忽略它们
- 废弃字段：在返回新字段的同时保留旧字段，并在 `__deprecated` 中标记
- 契约验证：确保 API 响应符合对应版本的预期契约
- 绝不能删除或重命名必填字段，只能新增可选字段

## 测试用例

### 1. 添加可选字段（向后兼容）

旧客户端应只收到它认识的字段。

输入：

```json
{"src":"client_v1","dest":"api","body":{"type":"get_users","msg_id":1}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "name": "John Doe"}], "version": "v1"}
```

### 2. 新客户端使用新字段

新客户端应收到 v2 新增的 full_name 和 phone 字段。

输入：

```json
{"src":"client_v2","dest":"api","body":{"type":"get_users","msg_id":1}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe", "phone": "+1234567890"}], "version": "v2"}
```

## 参考资料

- [Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html)：使用消费者驱动的契约测试来验证向后兼容性
- [OpenAPI Specification](https://swagger.io/specification/)：OpenAPI/Swagger 规范

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
