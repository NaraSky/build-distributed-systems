# 实现 a Lamport 时钟 from Scratch

英文标题：Implement a Lamport Clock from Scratch
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-1-lamport-basic>

课程：16. 时间守卫：逻辑时钟
任务序号：6
短标题：Lamport 基础
难度：intermediate
子主题：Lamport Clocks

## 中文导读

本题要求你完成 `实现 a Lamport 时钟 from Scratch`。

重点关注：`Lamport clock`、`logical time`、`happened-before`、`causal ordering`。

建议先按提示逐步实现：A Lamport 时钟 is a single integer 计数器 per 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A Lamport 时钟 is the simplest logical 时钟. Each 节点 maintains a single integer 计数器 that increases，包含every event. The rules are:

1. **Internal event**: increment the 计数器
2. **Send**: increment the 计数器, attach it to the 消息
3. **Receive**: set 计数器 = max(local_counter, message_counter) + 1

Implement a Lamport 时钟 节点，包含these handlers:

```JSON
请求:  {"type": "tick", "msg_id": 1}
响应: {"type": "tick_ok", "in_reply_to": 1, "时钟": 1}

请求:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
响应: {"type": "send_msg_ok", "in_reply_to": 2, "时钟": 2}

请求:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": 5, "payload": "hi"}
响应: {"type": "recv_msg_ok", "in_reply_to": 3, "时钟": 6}

请求:  {"type": "get_clock", "msg_id": 4}
响应: {"type": "get_clock_ok", "in_reply_to": 4, "时钟": 6}
```

## 涉及概念

- `Lamport clock`
- `logical time`
- `happened-before`
- `causal ordering`

## 实现提示

- A Lamport 时钟 is a single integer 计数器 per 节点
- Rule 1: Increment before any send event
- Rule 2: On receive, set 时钟 = max(local, msg_clock) + 1
- Rule 3: Increment on any internal event
- Test，包含3 节点 sending 消息 in a ring pattern

## 测试用例

### 1. Tick increments 时钟

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
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 2, "msg_id": 3}}
```

### 2. Receive updates 时钟 to max + 1

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":10,"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": 11, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 11, "msg_id": 3}}
```

## 参考资料

- [Time, Clocks,和the Ordering of Events - Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：The original paper by Leslie Lamport on logical clocks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
