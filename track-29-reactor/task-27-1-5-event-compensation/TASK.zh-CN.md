# 实现 Event Compensation和Sagas

英文标题：Implement Event Compensation和Sagas
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-5-event-compensation>

课程：29. 反应器：事件溯源与 CQRS
任务序号：5
短标题：Sagas
难度：advanced
子主题：Event Sourcing

## 中文导读

本题要求你完成 `实现 Event Compensation和Sagas`。

重点关注：`saga pattern`、`distributed transactions`、`compensation`、`rollback`、`choreography`。

建议先按提示逐步实现：Execute steps in order; on any 故障, compensate all previously completed steps in reverse order。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distributed transactions across multiple services cannot use a single database commit. A **saga** breaks the operation into a sequence of local steps, each，包含a corresponding compensation action. If any step fails, all already-completed steps are rolled back by executing their compensations in reverse order.

Implement a 节点 that executes sagas和handles failures:

```JSON
// Execute all steps successfully
{ "type": "execute", "msg_id": 1,
  "saga_id": "booking-123",
  "steps": ["book_flight", "book_hotel", "book_car"] }
-> { "type": "saga_completed", "in_reply_to": 1,
    "saga_id": "booking-123",
    "state": "completed", "completed_steps": 3 }

// Fail at book_hotel, compensate completed steps in reverse
{ "type": "execute", "msg_id": 2,
  "saga_id": "booking-124",
  "steps": ["book_flight", "book_hotel"],
  "fail_step": "book_hotel" }
-> { "type": "saga_compensated", "in_reply_to": 2,
    "saga_id": "booking-124",
    "state": "compensated",
    "compensated_steps": ["book_flight"] }
```

When a step fails, only the steps that were successfully completed before it need to be compensated — the failing step itself is not compensated because it never completed. Compensation order is the reverse of execution order.

## 涉及概念

- `saga pattern`
- `distributed transactions`
- `compensation`
- `rollback`
- `choreography`

## 实现提示

- Execute steps in order; on any 故障, compensate all previously completed steps in reverse order
- fail_step in the test input tells you which step should fail — simulate that 故障
- compensated_steps must list only the steps that were successfully executed before the 故障
- The compensation order is reverse of execution: last completed step is compensated first
- saga_id must be echoed back in every 响应 so the caller can correlate requests

## 测试用例

### 1. Execute saga successfully

All three steps succeed, completed_steps=3.

输入：

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-123","steps":["book_flight","book_hotel","book_car"]}}
```

期望输出：

```text
{"type": "saga_completed", "in_reply_to": 1, "saga_id": "booking-123", "state": "completed", "completed_steps": 3}
```

### 2. Compensate on failure

book_hotel fails, only book_flight (already completed) is compensated.

输入：

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-124","steps":["book_flight","book_hotel"],"fail_step":"book_hotel"}}
```

期望输出：

```text
{"type": "saga_compensated", "in_reply_to": 1, "saga_id": "booking-124", "state": "compensated", "compensated_steps": ["book_flight"]}
```

## 参考资料

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：Chris Richardson's overview of the saga pattern用于distributed transactions

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
