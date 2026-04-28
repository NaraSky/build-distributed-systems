# 实现命令查询职责分离基础

英文标题：Implement CQRS Fundamentals
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-1-cqrs-fundamentals>

课程：29. 反应器：事件溯源与 CQRS
任务序号：6
短标题：CQRS 基础
难度：进阶
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你实现命令查询职责分离（CQRS）的基本框架。核心思想很简单：把"写操作"和"读操作"彻底分开处理。写操作走命令总线，读操作走查询总线，两边各自优化互不干扰。这是构建高性能、可扩展分布式系统的重要架构模式。

## 题目说明

命令查询职责分离（CQRS，Command Query Responsibility Segregation）把每个操作严格划分为**命令**（写操作，改变系统状态）或**查询**（读操作，不改变任何状态）。命令和查询由各自独立的总线处理，使用各自独立的数据模型，这样两边就可以分别进行优化。

你需要实现一个将消息路由到正确总线的节点：

```json
// 命令：校验参数，应用变更，返回产生的事件
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John", "email": "john@example.com"} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>", "name": "John"}}] }

// 命令校验失败
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John"} }    // 缺少 email
-> { "type": "command_result", "in_reply_to": 2,
    "success": false,
    "errors": ["Email is required"] }

// 查询：从读取模型中获取数据，不改变任何状态
{ "type": "GetUser", "msg_id": 3,
  "params": {"user_id": "user-123"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe"} }
```

关键规则是：如果操作会改变状态，那它就是命令；如果只是读取数据，那它就是查询。一个操作绝不能同时做读和写两件事。

## 概念说明

你可以把命令查询职责分离想象成一个餐厅的运作方式。厨房（写入端）只负责做菜，服务窗口（读取端）只负责出菜给客人。两边各有专门的流程和优化方式，互不干扰。命令总线就像点菜单传到厨房的通道，查询总线就像客人查看菜品状态的窗口。把读和写分开后，厨房可以专注于快速出菜，窗口可以专注于高效服务，不会互相拖后腿。

## 涉及概念

- `CQRS`
- `command bus`
- `query bus`
- `command validation`
- `read model`
- `write model separation`

## 实现提示

- 命令改变状态并产生事件；查询只读取数据，绝不修改状态
- 命令处理器负责校验参数、应用变更，并返回产生的事件
- 查询处理器从预先构建的读取模型中读取数据并返回
- 校验失败时应返回 success=false 以及错误信息数组
- 根据消息的 type 字段进行路由：CreateUser 走命令总线，GetUser 走查询总线

## 测试用例

### 1. 处理命令

有效的命令应成功执行并返回产生的事件。

输入：

```json
{"src":"client","dest":"commandbus","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com"}}}
```

期望输出：

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"type": "UserCreated", "payload": {"id": ".*", "name": "John"}}]}
```

### 2. 执行查询

查询应从读取模型中返回数据，不改变任何状态。

输入：

```json
{"src":"client","dest":"querybus","body":{"type":"GetUser","msg_id":1,"params":{"user_id":"user-123"}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John Doe"}}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：Martin Fowler 对命令查询职责分离模式的解释

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
