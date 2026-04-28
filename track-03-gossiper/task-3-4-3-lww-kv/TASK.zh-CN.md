# 实现 Last-Writer-Wins 键值 存储

英文标题：Implement Last-Writer-Wins Key-Value Store
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-3-lww-kv>

课程：3. 传播者：Gossip 信息传播
任务序号：18
短标题：LWW KV 存储
难度：advanced
子主题：Epidemic Algorithms和CRDT Gossip

## 中文导读

本题要求你完成 `实现 Last-Writer-Wins 键值 存储`。

重点关注：`LWW register`、`conflict resolution`、`timestamp ordering`、`gossip replication`。

建议先按提示逐步实现：Each value is paired，包含a timestamp from when it was written。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A **Last-Writer-Wins (LWW)** register resolves conflicts by always keeping the value，包含the latest timestamp. This is simple but can lose concurrent writes.

Implement an LWW key-value store:

```JSON
请求:  {"type": "write", "msg_id": 1, "key": "x", "value": "hello"}
响应: {"type": "write_ok", "in_reply_to": 1, "ts": 1704067200.123}

请求:  {"type": "kv_read", "msg_id": 2, "key": "x"}
响应: {"type": "kv_read_ok", "in_reply_to": 2, "key": "x", "value": "hello", "ts": 1704067200.123}

请求:  {"type": "kv_merge", "msg_id": 3, "entries": {"x": {"value": "world", "ts": 1704067201.0}}}
响应: {"type": "kv_merge_ok", "in_reply_to": 3, "updated": 1}
```

## 涉及概念

- `LWW register`
- `conflict resolution`
- `timestamp ordering`
- `gossip replication`

## 实现提示

- Each value is paired，包含a timestamp from when it was written
- On merge, keep the value，包含the higher timestamp
- If timestamps tie, use a deterministic tiebreaker (e.g., 节点 ID comparison)
- LWW is simple but can silently lose concurrent writes
- Use time.time()用于timestamps

## 测试用例

### 1. Write和read back

write_ok，包含ts, then kv_read_ok，包含value="hi".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read missing key returns error

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":2,"key":"missing"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "error", "code": 20, "text": "Key not found", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Last-Writer-Wins Register](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set)：Wikipedia on LWW CRDT semantics

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
