# 演示 Lamport 时钟的因果性局限

英文标题：Demonstrate Lamport Clock Causality Limitation
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-2-lamport-limitation>

课程：2. 标识符：分布式唯一 ID
任务序号：12
短标题：因果性局限
难度：进阶
子主题：Logical Clocks as IDs

## 中文导读

Lamport 时钟（Lamport Clock）有一个重要的局限：它只能保证"如果事件 A 发生在 B 之前，那么 A 的时钟值一定小于 B 的时钟值"，但反过来不成立——时钟值小并不意味着事件真的先发生。本题要求你构建一个事件追踪器，演示并检测这个局限性。理解这一点是后续学习向量时钟的基础。

## 题目说明

Lamport 时钟有一条核心保证：如果事件 A 因果上先于事件 B 发生（即 A happens-before B），那么 A 的 Lamport 时钟值一定小于 B 的时钟值，即 L(A) < L(B)。

但是，**反过来并不成立**：L(A) < L(B) 并不能说明 A 一定发生在 B 之前。两个分别在不同节点（Node）上独立发生的并发事件，它们的时钟值可以是任意大小关系。

打个比方：你和朋友分别在两个城市写日记，你写了第 1 页，朋友写了第 2 页。页码虽然有大小，但这并不意味着朋友是在你之后写的——你们是各写各的，互不影响。

你的任务是构建一个事件追踪器来演示这个局限：

1. 在本地节点上记录事件，并附带 Lamport 时间戳
2. 接收来自远程节点的事件及其时间戳
3. 实现 `check_causality` 处理器，给定两个事件的标识，报告仅凭 Lamport 时钟能否判断它们的因果关系

```json
请求:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "data": "write x=1"}
响应: {"type": "record_event_ok", "in_reply_to": 1, "event_id": "e1", "clock": 1, "node": "n1"}
```

```json
请求:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
响应: {"type": "check_causality_ok", "in_reply_to": 3,
           "clock_a": 1, "clock_b": 2,
           "lamport_says": "a_before_b",
           "actual": "unknown"}
```

其中 `lamport_says` 字段表示 Lamport 时钟排序给出的结论，`actual` 字段表示真实的因果关系。对于同一节点上的两个事件，因果关系可以确定；但对于不同节点上的事件，由于 Lamport 时钟无法判断真实的因果关系，`actual` 应为 `"unknown"`。

## 涉及概念

- `causality`
- `concurrent events`
- `partial order`
- `happens-before relation`

## 实现提示

- L(A) < L(B) 并不能推导出 A 发生在 B 之前
- 两个不同节点上的独立事件，其时钟值可以是任意排列
- 可以构造这样的场景：两个事件的时钟值有明确大小关系，但实际上它们是并发的
- Lamport 时钟的逆命题不成立：有序的时钟值并不意味着因果关系
- 正是这个局限性，催生了向量时钟的诞生

## 测试用例

### 1. 记录事件后返回时钟值和节点标识

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

### 2. 检查两个本地事件之间的因果关系

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

- [Logical Clocks - Martin Kleppmann](https://martin.kleppmann.com/2020/12/02/bloom-filter-hash-graph-sync.html)：关于时钟系统与分布式排序的深入讲解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
