# 实现命令端校验与执行

英文标题：Implement Command Side Validation and Execution
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-2-command-side>

课程：29. 反应器：事件溯源与 CQRS
任务序号：7
短标题：命令端
难度：进阶
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你实现 CQRS 中命令端的校验和执行逻辑。命令端是整个系统的"写入路径"，每个写入操作在真正执行之前都必须通过两道关卡：格式校验（字段是否完整、类型是否正确）和业务规则校验（是否满足业务约束）。只有两道关卡都通过了，才会真正执行命令并产生领域事件。

## 题目说明

命令端是 CQRS 中的写入路径。在任何状态变更被应用之前，命令必须通过两层校验：**格式校验（Schema Validation）**（字段和类型是否正确）和**业务规则校验（Business Rule Validation）**（领域约束是否满足）。只有校验全部通过，才会执行命令并产生领域事件（Domain Event）。

你需要实现一个通过两层校验来处理命令的节点：

```json
// 格式错误：缺少必填字段
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John"} }      // 缺少 email
-> { "type": "validation_failed", "in_reply_to": 1,
    "valid": false, "errors": ["Email is required"] }

// 业务规则错误：年龄约束
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John", "email": "j@example.com", "age": 16} }
-> { "type": "validation_failed", "in_reply_to": 2,
    "valid": false, "errors": ["User must be 18 or older"] }

// 所有校验通过：执行命令并产生领域事件
{ "type": "CreateUser", "msg_id": 3,
  "payload": {"name": "John", "email": "j@example.com", "age": 25} }
-> { "type": "command_executed", "in_reply_to": 3,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>"}}] }
```

当有多条校验失败时，应收集所有错误信息一起返回。只要有任何校验不通过，就绝不执行命令。

## 涉及概念

- `command validation`
- `business rules`
- `command handler`
- `domain events`
- `invariant enforcement`

## 实现提示

- 格式校验优先执行：先检查必填字段和类型，再进行业务规则校验
- 业务规则校验：强制执行领域约束（年龄大于等于 18、邮箱唯一等）
- 将所有校验错误收集在一起返回，而不是只返回第一个
- 只有所有校验都通过后，才调用命令处理器
- 产生的领域事件应描述"发生了什么"（UserCreated），而不是"请求了什么"

## 测试用例

### 1. 校验命令格式

缺少 email 字段应导致格式校验失败。

输入：

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John"}}}
```

期望输出：

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["Email is required"]}
```

### 2. 校验业务规则

年龄小于 18 应导致业务规则校验失败。

输入：

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com","age":16}}}
```

期望输出：

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["User must be 18 or older"]}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：CQRS 架构与命令端设计

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
