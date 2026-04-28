# 构建因果有序的聊天系统

英文标题：Build a Causal-Order Chat System
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-3-causal-chat>

课程：16. 时间守卫：逻辑时钟
任务序号：13
短标题：因果聊天
难度：高级
子主题：向量时钟

## 中文导读

本题要求你构建一个分布式聊天系统，即使消息在网络中乱序到达，也能按因果顺序正确显示。想象一下群聊中，有人问了一个问题，另一个人回答了这个问题，但回答先到了你这里——你需要等问题到了再显示回答。这就是因果投递（Causal Delivery）要解决的问题。

## 题目说明

构建一个分布式聊天系统，让消息即使在网络上乱序到达，也能按因果顺序正确显示。每条消息都会携带发送者的向量时钟。

来自节点 `j` 的消息 `m`，携带向量时钟 `vc_m`，只有在满足以下条件时，才能在节点 `i` 上投递：
1. `vc_m[j] == vc_i[j] + 1`（这是来自节点 j 的下一条预期消息）
2. `vc_m[k] <= vc_i[k]` 对所有 `k != j` 成立（所有因果依赖都已满足）

请实现以下处理器：

```json
Request:  {"type": "chat_send", "msg_id": 1, "text": "hello everyone"}
Response: {"type": "chat_send_ok", "in_reply_to": 1, "clock": [1, 0]}

Request:  {"type": "chat_recv", "msg_id": 2, "from": "n2", "text": "reply", "sender_clock": [0, 1]}
Response: {"type": "chat_recv_ok", "in_reply_to": 2, "delivered": true, "clock": [1, 1]}

Request:  {"type": "get_chat_log", "msg_id": 3}
Response: {"type": "get_chat_log_ok", "in_reply_to": 3, "messages": [
    {"from": "n1", "text": "hello everyone", "clock": [1, 0]},
    {"from": "n2", "text": "reply", "clock": [0, 1]}
]}
```

## 涉及概念

- `causal ordering`
- `message reordering`
- `causal delivery`
- `distributed chat`

## 实现提示

- 每条聊天消息都要附带发送者的向量时钟
- 对于不满足因果顺序的消息，先放入缓冲区暂存
- 只有当一条消息的所有因果依赖都已满足时，才能投递该消息
- 因果依赖判断：对于来自节点 j 且携带向量时钟 vc 的消息，需要满足 `vc[j] == your_vc[j] + 1` 且对所有 `k != j`，`vc[k] <= your_vc[k]`
- 投递一条消息后，要重新检查缓冲区中是否有新的可投递消息

## 测试用例

### 1. 发送聊天消息会递增时钟

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

### 2. 收到顺序正确的消息会立即投递

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

- [Causal Ordering in Distributed Systems](https://www.baeldung.com/cs/causal-ordering-in-distributed-systems)：讲解如何利用向量时钟实现因果投递，保证消息的有序性

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
