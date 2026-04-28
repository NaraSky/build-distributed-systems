# 实现向量时钟

英文标题：Implement Vector Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-1-vector-clock-impl>

课程：16. 时间守卫：逻辑时钟
任务序号：11
短标题：向量时钟实现
难度：进阶
子主题：向量时钟

## 中文导读

本题要求你实现一个向量时钟（Vector Clock）系统。向量时钟是分布式系统中判断事件因果关系的核心工具，它为集群中的每个节点维护一个计数器，从而精确追踪"谁先于谁发生"。掌握向量时钟是理解分布式一致性的基础。

## 题目说明

向量时钟（Vector Clock）是兰伯特时钟（Lamport Clock）的增强版本。兰伯特时钟只用一个计数器，而向量时钟为集群中的每个节点（Node）都维护一个计数器，构成一个长度为 N 的整数数组。这样做的好处是：你可以判断两个事件之间是否存在因果关系。

更新规则如下：
1. **本地事件**：把自己对应位置的计数器加 1，即 `vc[self] += 1`
2. **发送消息**：先把自己对应位置的计数器加 1，然后把整个向量附在消息中一起发出去
3. **接收消息**：把本地向量和消息中携带的向量逐位取最大值，即 `vc[i] = max(vc[i], msg_vc[i])`，然后再把自己的计数器加 1

请实现以下向量时钟处理器：

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": [1, 0, 0]}

Request:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
Response: {"type": "send_msg_ok", "in_reply_to": 2, "clock": [2, 0, 0]}

Request:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": [0, 5, 0], "payload": "hi"}
Response: {"type": "recv_msg_ok", "in_reply_to": 3, "clock": [3, 5, 0]}

Request:  {"type": "get_clock", "msg_id": 4}
Response: {"type": "get_clock_ok", "in_reply_to": 4, "clock": [3, 5, 0]}
```

## 涉及概念

- `vector clock`
- `causal ordering`
- `partial order`
- `distributed time`

## 实现提示

- 每个节点维护一个长度为 N 的整数数组，集群中的每个节点各占一个位置
- 发生任何本地事件时，把自己对应位置的计数器加 1
- 发送消息时，先递增自己的计数器，再把完整的向量附在消息中
- 接收消息时，把本地向量和收到的向量逐位取最大值，然后递增自己的计数器
- 启动时所有位置初始化为 0

## 测试用例

### 1. 本地事件只递增自己的计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0, 0], "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": [2, 0, 0], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 0, 0], "msg_id": 3}}
```

### 2. 接收消息时逐位取最大值进行合并

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":[0,7],"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0], "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": [2, 7], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 7], "msg_id": 3}}
```

## 参考资料

- [Vector Clocks - Why It Is Hard to Tell the Time](https://riak.com/posts/technical/vector-clocks-revisited/index.html)：通过实际案例通俗讲解向量时钟的工作原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
