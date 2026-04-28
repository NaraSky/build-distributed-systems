# Demonstrate Lamport 时钟 Causality Limitation

英文标题：Demonstrate Lamport Clock Causality Limitation
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-2-lamport-limitation>

课程：2. 标识符：分布式唯一 ID
任务序号：12
短标题：Causality Limitation
难度：intermediate
子主题：Logical Clocks as IDs

## 中文导读

本题要求你完成 `Demonstrate Lamport 时钟 Causality Limitation`。

重点关注：`causality`、`concurrent events`、`partial order`、`happens-before relation`。

建议先按提示逐步实现：L(A) < L(B) does NOT imply A happened before B。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Lamport clocks guarantee: if A happens-before B, then L(A) < L(B). But the **converse is not true**: L(A) < L(B) does NOT mean A happened before B. Two concurrent events on different 节点 can have any relative 时钟 values.

Your task is to build an event tracker that demonstrates this limitation:

1. Track events on the local 节点，包含their Lamport timestamps
2. Accept events from remote 节点，包含their timestamps  
3. Implement a `check_causality` handler that, given two event IDs, reports whether causality can be determined from Lamport clocks alone

```JSON
请求:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "data": "write x=1"}
响应: {"type": "record_event_ok", "in_reply_to": 1, "event_id": "e1", "时钟": 1, "节点": "n1"}
```

```JSON
请求:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
响应: {"type": "check_causality_ok", "in_reply_to": 3,
           "clock_a": 1, "clock_b": 2,
           "lamport_says": "a_before_b",
           "actual": "unknown"}
```

The `lamport_says` field reports what Lamport ordering suggests. The `actual` field is always "unknown"用于events on different 节点 (since Lamport clocks cannot determine true causality in that case).

## 涉及概念

- `causality`
- `concurrent events`
- `partial order`
- `happens-before relation`

## 实现提示

- L(A) < L(B) does NOT imply A happened before B
- Two independent events on different 节点 can have any 时钟 ordering
- Construct a scenario where two events have ordered clocks but are concurrent
- The converse of the Lamport property fails: ordered clocks do not imply causality
- This limitation motivates vector clocks

## 测试用例

### 1. Record event returns 时钟和node

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","data":"write x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e1", "clock": 1, "node": "n1", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Check causality between two local events

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","data":"a"}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","data":"b"}}
{"src":"c1","dest":"n1","body":{"type":"check_causality","msg_id":4,"event_a":"e1","event_b":"e2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e1", "clock": 1, "node": "n1", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e2", "clock": 2, "node": "n1", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "check_causality_ok", "clock_a": 1, "clock_b": 2, "lamport_says": "a_before_b", "actual": "causal", "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Logical Clocks - Martin Kleppmann](https://martin.kleppmann.com/2020/12/02/bloom-filter-hash-graph-sync.html)：Kleppmann on 时钟 systems和distributed ordering

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
