# Demonstrate LWW Data Loss，包含Version Vectors

英文标题：Demonstrate LWW Data Loss，包含Version Vectors
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-4-lww-problem>

课程：3. 传播者：Gossip 信息传播
任务序号：19
短标题：LWW Problem
难度：advanced
子主题：Epidemic Algorithms和CRDT Gossip

## 中文导读

本题要求你完成 `Demonstrate LWW Data Loss，包含Version Vectors`。

重点关注：`LWW limitation`、`data loss`、`version vectors`、`conflict detection`。

建议先按提示逐步实现：LWW silently discards the loser in concurrent writes。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

LWW silently loses data when two clients write concurrently. Your task is to demonstrate this和implement a version-vector alternative that detects conflicts.

Implement two modes: `lww` (last-writer-wins)和`vv` (version-vector):

```JSON
请求:  {"type": "set_mode", "msg_id": 1, "mode": "vv"}
响应: {"type": "set_mode_ok", "in_reply_to": 1}

请求:  {"type": "vv_write", "msg_id": 2, "key": "x", "value": "a", "context": {}}
响应: {"type": "vv_write_ok", "in_reply_to": 2, "vc": {"c1": 1}}

请求:  {"type": "vv_read", "msg_id": 3, "key": "x"}
响应: {"type": "vv_read_ok", "in_reply_to": 3, "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false}
```

When concurrent writes happen in vv mode, both values are preserved:
```JSON
响应: {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}, {"value": "b", "vc": {"c2": 1}}], "conflict": true}
```

## 涉及概念

- `LWW limitation`
- `data loss`
- `version vectors`
- `conflict detection`

## 实现提示

- LWW silently discards the loser in concurrent writes
- Construct a scenario: 客户端 A writes x=1, 客户端 B writes x=2 at nearly the same time
- The write，包含the lower timestamp is lost forever
- Version vectors can detect this conflict instead of silently resolving it
- Return both values as siblings when conflict is detected

## 测试用例

### 1. Set mode to vv

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"set_mode","msg_id":2,"mode":"vv"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "set_mode_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Single vv_write和read, no conflict

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vv_write","msg_id":2,"key":"x","value":"a","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vv_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_write_ok", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false, "in_reply_to": 3, "msg_id": 2}}
```

## 参考资料

- [Amazon Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：Dynamo uses version vectors用于conflict detection

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
