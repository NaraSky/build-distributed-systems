# 实现 Saga Pattern

英文标题：Implement Saga Pattern
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-4-sagas>

课程：9. 协调器：分布式事务
任务序号：4
短标题：Sagas
难度：advanced
子主题：Two-Phase Commit

## 中文导读

本题要求你完成 `实现 Saga Pattern`。

重点关注：`saga`、`compensation`、`eventual consistency`。

建议先按提示逐步实现：Each step has compensating action。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Sagas: sequence of local transactions，包含compensations. On 故障, compensate in reverse order.

## 概念说明

### Sagas

Sagas break transactions into local steps，包含compensations. No locks held. Eventually consistent.

## 涉及概念

- `saga`
- `compensation`
- `eventual consistency`

## 实现提示

- Each step has compensating action
- On 故障, run compensations in reverse
- 最终一致性

## 测试用例

### 1. Execute all steps in sequence

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"saga_execute","msg_id":2,"saga_id":"saga1","steps":[{"name":"reserve_inventory","action":"reserve","compensation":"release"},{"name":"charge_payment","action":"charge","compensation":"refund"},{"name":"ship_order","action":"ship","compensation":"cancel_shipment"}]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"saga_execute_ok","in_reply_to":2,"msg_id":1,"saga_id":"saga1","status":"completed","steps_executed":["reserve_inventory","charge_payment","ship_order"]}}
```

## 参考资料

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：Microservices saga pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
