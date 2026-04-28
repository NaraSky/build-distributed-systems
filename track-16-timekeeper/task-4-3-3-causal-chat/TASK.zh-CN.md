# 构建 a Causal-Order Chat System

英文标题：Build a Causal-Order Chat System
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-3-causal-chat>

课程：16. 时间守卫：逻辑时钟
任务序号：13
短标题：Causal Chat
难度：advanced
子主题：向量 Clocks

## 中文导读

本题要求你完成 `构建 a Causal-Order Chat System`。

重点关注：`causal ordering`、`message reordering`、`causal delivery`、`distributed chat`。

建议先按提示逐步实现：Attach the sender vector 时钟 to every chat 消息。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a distributed chat system where 消息 are displayed in causal order even when they arrive out of 网络 order. Each 消息 carries the sender's vector 时钟.

A 消息 `m` from 节点 `j`，包含vector 时钟 `vc_m` is **deliverable** at 节点 `i` when:
1. `vc_m[j] == vc_i[j] + 1` (it is the next expected 消息 from j)
2. `vc_m[k] <= vc_i[k]`用于all `k != j` (all causal dependencies are met)

Implement handlers:

```JSON
请求:  {"type": "chat_send", "msg_id": 1, "text": "hello everyone"}
响应: {"type": "chat_send_ok", "in_reply_to": 1, "时钟": [1, 0]}

请求:  {"type": "chat_recv", "msg_id": 2, "from": "n2", "text": "reply", "sender_clock": [0, 1]}
响应: {"type": "chat_recv_ok", "in_reply_to": 2, "delivered": true, "时钟": [1, 1]}

请求:  {"type": "get_chat_log", "msg_id": 3}
响应: {"type": "get_chat_log_ok", "in_reply_to": 3, "消息": [
    {"from": "n1", "text": "hello everyone", "时钟": [1, 0]},
    {"from": "n2", "text": "reply", "时钟": [0, 1]}
]}
```

## 涉及概念

- `causal ordering`
- `message reordering`
- `causal delivery`
- `distributed chat`

## 实现提示

- Attach the sender vector 时钟 to every chat 消息
- Buffer incoming 消息 that arrive out of causal order
- A 消息 is deliverable when all of its causal dependencies are satisfied
- Causal dependency:用于消息 from 节点 j，包含vc, you need vc[j] == your_vc[j] + 1和vc[k] <= your_vc[k]用于all k != j
- After delivering a 消息, check the buffer用于newly deliverable 消息

## 测试用例

### 1. Send a chat 消息 increments 时钟

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"chat_send","msg_id":2,"text":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "chat_send_ok", "in_reply_to": 2, "clock": [1, 0], "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 3, "clock": [1, 0], "msg_id": 2}}
```

### 2. Receive in-order 消息 is delivered immediately

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"n2","dest":"n1","body":{"type":"chat_recv","msg_id":2,"from":"n2","text":"hi","sender_clock":[0,1]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "chat_recv_ok", "in_reply_to": 2, "delivered": true, "clock": [1, 1], "msg_id": 1}}
```

## 参考资料

- [Causal Ordering in Distributed Systems](https://www.baeldung.com/cs/causal-ordering-in-distributed-systems)：How causal delivery guarantees 消息 ordering使用vector clocks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
