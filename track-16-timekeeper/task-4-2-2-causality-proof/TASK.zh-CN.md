# 验证 Lamport 时钟的因果性及其局限

英文标题：Prove Lamport Clock Causality and Its Limitation
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-2-causality-proof>

课程：16. 时间守卫：逻辑时钟
任务序号：7
短标题：因果性验证
难度：高级
子主题：Lamport 时钟

## 中文导读

这道题让你深入理解 Lamport 时钟的能力边界。Lamport 时钟保证：如果事件 A 因果地发生在事件 B 之前，那么 A 的时间戳一定小于 B 的时间戳。但反过来不成立——时间戳小不代表有因果关系，两个事件可能完全无关（并发）。你需要构建一个系统来记录事件及其因果链，并对比 Lamport 时间戳推断的关系与实际因果关系之间的差异。

## 题目说明

Lamport 时钟提供如下保证：如果事件 A **先于（Happened-Before）** 事件 B 发生，则 `L(A) < L(B)`。但反过来不成立——`L(A) < L(B)` 并不意味着 A 导致了 B。两个事件可能是**并发的（Concurrent）**，即互不影响。

你的任务是构建一个系统，能够：
1. 记录事件及其 Lamport 时间戳
2. 跟踪实际的因果链（即发送和接收的关联关系）
3. 对比 Lamport 时间戳所暗示的顺序与实际因果关系

实现以下消息处理器：
```json
Request:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "caused_by": null}
Response: {"type": "record_event_ok", "in_reply_to": 1, "clock": 1}

Request:  {"type": "record_event", "msg_id": 2, "event_id": "e2", "caused_by": "e1"}
Response: {"type": "record_event_ok", "in_reply_to": 2, "clock": 2}

Request:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
Response: {"type": "check_causality_ok", "in_reply_to": 3,
           "lamport_says": "a_before_b", "actual": "a_before_b", "correct": true}
```

## 涉及概念

- `happened-before`
- `causality`
- `concurrent events`
- `Lamport limitation`

## 实现提示

- 如果 A 先于 B 发生，则 `L(A) < L(B)`——这是 Lamport 时钟的保证
- 反过来不成立：`L(A) < L(B)` 不能说明 A 先于 B 发生
- 可以构造一个反例：两个从不通信的独立节点
- 例如节点 n1 执行一次 tick（L=1），节点 n2 执行两次 tick（L=2），此时 `L(n1) < L(n2)` 但两者是并发的
- 需要报告两个事件究竟是因果相关还是并发的

## 测试用例

### 1. 记录两个有因果关系的事件

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

### 2. 检查因果事件对的因果关系

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

- [Happened-Before Relation](https://en.wikipedia.org/wiki/Happened-before)：关于"先于"偏序关系的维基百科解释

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
