# 实现事件补偿与 Saga 模式

英文标题：Implement Event Compensation and Sagas
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-5-event-compensation>

课程：29. 反应器：事件溯源与 CQRS
任务序号：5
短标题：Saga 模式
难度：高级
子主题：Event Sourcing

## 中文导读

本题要求你实现 Saga 模式来处理分布式事务。在微服务架构中，一个业务操作往往需要跨多个服务协调完成，但又不能像单体应用那样用一个数据库事务搞定。Saga 把整个操作拆成一系列步骤，每个步骤都有对应的"撤销"操作。一旦某个步骤失败，就按相反的顺序逐个撤销已完成的步骤。这是分布式系统中保证数据一致性的经典方案。

## 题目说明

跨多个服务的分布式事务无法使用单个数据库提交来完成。**Saga 模式**将操作拆分为一系列本地步骤，每个步骤都有对应的补偿操作。如果某个步骤失败，所有已完成的步骤都会通过按相反顺序执行补偿操作来回滚。

你需要实现一个执行 Saga 并处理失败的节点：

```json
// 所有步骤全部成功
{ "type": "execute", "msg_id": 1,
  "saga_id": "booking-123",
  "steps": ["book_flight", "book_hotel", "book_car"] }
-> { "type": "saga_completed", "in_reply_to": 1,
    "saga_id": "booking-123",
    "state": "completed", "completed_steps": 3 }

// 在 book_hotel 步骤失败，按相反顺序补偿已完成的步骤
{ "type": "execute", "msg_id": 2,
  "saga_id": "booking-124",
  "steps": ["book_flight", "book_hotel"],
  "fail_step": "book_hotel" }
-> { "type": "saga_compensated", "in_reply_to": 2,
    "saga_id": "booking-124",
    "state": "compensated",
    "compensated_steps": ["book_flight"] }
```

当某个步骤失败时，只有在它之前已经成功完成的步骤需要被补偿。失败的步骤本身不需要补偿，因为它从未完成。补偿顺序是执行顺序的逆序。

## 概念说明

Saga 模式可以用旅行预订来类比：你需要依次订机票、订酒店、订租车。如果订酒店时失败了，你需要把之前订好的机票退掉。注意退订的顺序是"后进先出"的：最后完成的步骤最先撤销，就像撤销操作的"回退栈"一样。

## 涉及概念

- `saga pattern`
- `distributed transactions`
- `compensation`
- `rollback`
- `choreography`

## 实现提示

- 按顺序执行步骤；如果某个步骤失败，按相反顺序补偿所有之前已完成的步骤
- 测试输入中的 fail_step 字段指明哪个步骤应该模拟失败
- compensated_steps 只列出在失败之前已成功执行的步骤
- 补偿顺序是执行顺序的逆序：最后完成的步骤最先被补偿
- 每个响应中都必须回传 saga_id，以便调用者进行关联

## 测试用例

### 1. 成功执行 Saga

三个步骤全部成功，completed_steps 为 3。

输入：

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-123","steps":["book_flight","book_hotel","book_car"]}}
```

期望输出：

```text
{"type": "saga_completed", "in_reply_to": 1, "saga_id": "booking-123", "state": "completed", "completed_steps": 3}
```

### 2. 失败时进行补偿

book_hotel 失败，只有之前已完成的 book_flight 需要被补偿。

输入：

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-124","steps":["book_flight","book_hotel"],"fail_step":"book_hotel"}}
```

期望输出：

```text
{"type": "saga_compensated", "in_reply_to": 1, "saga_id": "booking-124", "state": "compensated", "compensated_steps": ["book_flight"]}
```

## 参考资料

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：Chris Richardson 对分布式事务 Saga 模式的概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
