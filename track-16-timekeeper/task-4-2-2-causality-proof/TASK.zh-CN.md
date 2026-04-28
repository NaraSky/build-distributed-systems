# Prove Lamport 时钟 Causality和Its Limitation

英文标题：Prove Lamport Clock Causality和Its Limitation
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-2-causality-proof>

课程：16. 时间守卫：逻辑时钟
任务序号：7
短标题：Causality Proof
难度：advanced
子主题：Lamport Clocks

## 中文导读

本题要求你完成 `Prove Lamport 时钟 Causality和Its Limitation`。

重点关注：`happened-before`、`causality`、`concurrent events`、`Lamport limitation`。

建议先按提示逐步实现：If A happened-before B, then L(A) < L(B) - this is guaranteed。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Lamport clocks guarantee: if event A **happened-before** event B, then L(A) < L(B). But the converse is NOT true - L(A) < L(B) does NOT mean A caused B. Events may be **concurrent** (neither caused the other).

Your task is to build a system that:
1. Records events，包含Lamport timestamps
2. Tracks the actual causal chain (send/receive links)
3. Compares what Lamport timestamps tell us vs actual causality

Implement:
```JSON
请求:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "caused_by": null}
响应: {"type": "record_event_ok", "in_reply_to": 1, "时钟": 1}

请求:  {"type": "record_event", "msg_id": 2, "event_id": "e2", "caused_by": "e1"}
响应: {"type": "record_event_ok", "in_reply_to": 2, "时钟": 2}

请求:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
响应: {"type": "check_causality_ok", "in_reply_to": 3,
           "lamport_says": "a_before_b", "actual": "a_before_b", "correct": true}
```

## 涉及概念

- `happened-before`
- `causality`
- `concurrent events`
- `Lamport limitation`

## 实现提示

- If A happened-before B, then L(A) < L(B) - this is guaranteed
- The converse is NOT true: L(A) < L(B) does NOT imply A happened-before B
- Construct a counterexample，包含two independent 节点 that never communicate
- 节点 n1 ticks once (L=1), 节点 n2 ticks twice (L=2) - L(n1) < L(n2) but they are concurrent
- Report whether two events are causal or concurrent based on Lamport timestamps alone

## 测试用例

### 1. Record two causal events

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","caused_by":null}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","caused_by":"e1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
```

### 2. Check causality of causal pair

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","caused_by":null}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","caused_by":"e1"}}
{"src":"c1","dest":"n1","body":{"type":"check_causality","msg_id":4,"event_a":"e1","event_b":"e2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "check_causality_ok", "in_reply_to": 4, "lamport_says": "a_before_b", "actual": "a_before_b", "correct": true, "msg_id": 3}}
```

## 参考资料

- [Happened-Before Relation](https://en.wikipedia.org/wiki/Happened-before)：Wikipedia explanation of the happened-before partial order

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
