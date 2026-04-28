# 实现 Anti-Entropy，包含Digest Comparison

英文标题：Implement Anti-Entropy，包含Digest Comparison
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-4-anti-entropy>

课程：3. 传播者：Gossip 信息传播
任务序号：9
短标题：Anti-Entropy
难度：advanced
子主题：Gossip Protocol

## 中文导读

本题要求你完成 `实现 Anti-Entropy，包含Digest Comparison`。

重点关注：`anti-entropy`、`digest`、`set reconciliation`、`bandwidth optimization`。

建议先按提示逐步实现：A digest is a compact summary of your state (e.g., sorted hash of all 消息 IDs)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Full state sync wastes bandwidth when 节点 are mostly in sync. **Anti-entropy** optimizes this: first exchange compact digests. Only transfer full state if digests differ.

Implement digest-based anti-entropy:

1. `digest` handler returns a hash of the current 消息 set
2. `digest_sync` handler compares digests和only transfers if different
3. Track bandwidth savings

```JSON
请求:  {"type": "digest", "msg_id": 1}
响应: {"type": "digest_ok", "in_reply_to": 1, "digest": "abc123", "count": 5}
```

```JSON
请求:  {"type": "digest_sync", "msg_id": 2, "remote_digest": "abc123", "remote_messages": null}
响应: {"type": "digest_sync_ok", "in_reply_to": 2, "match": true, "transferred": 0}
```

If digests differ, the remote sends its 消息:
```JSON
请求:  {"type": "digest_sync", "msg_id": 3, "remote_digest": "xyz789", "remote_messages": [1,2,3]}
响应: {"type": "digest_sync_ok", "in_reply_to": 3, "match": false, "transferred": 2, "local_messages": [1,2,3,4,5]}
```

## 涉及概念

- `anti-entropy`
- `digest`
- `set reconciliation`
- `bandwidth optimization`

## 实现提示

- A digest is a compact summary of your state (e.g., sorted hash of all 消息 IDs)
- Compare digests first; only transfer full state if they differ
- This saves bandwidth when 节点 are mostly in sync
- Use a simple hash of sorted 消息 IDs as the digest
- Track bytes saved by使用digests vs full sync

## 测试用例

### 1. Digest of empty set

digest_ok should have count=0和a non-empty digest string.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Digest sync，包含matching digest

digest_ok should have count=1. The digest value can be used用于subsequent digest_sync.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Merkle Trees用于Anti-Entropy](https://en.wikipedia.org/wiki/Merkle_tree)：How Merkle trees enable efficient set reconciliation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
