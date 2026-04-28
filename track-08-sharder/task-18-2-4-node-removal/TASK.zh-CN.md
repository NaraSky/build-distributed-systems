#处理Node Removal，包含Graceful和Crash Recovery

英文标题：Handle节点Removal，包含Graceful和Crash Recovery
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-4-node-removal>

课程：8. 分片器：水平扩展与数据迁移
任务序号：9
短标题：Node Removal
难度：advanced
子主题：Consistent Hashing

## 中文导读

本题要求你完成 `Handle节点Removal，包含Graceful和Crash Recovery`。

重点关注：`node removal`、`graceful shutdown`、`crash recovery`、`key takeover`、`successor promotion`。

建议先按提示逐步实现：On graceful shutdown: 节点 transfers its keys to its clockwise successor before leaving。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 节点 leaves the ring (graceful shutdown or crash), its key range must be taken over by its successor. The two scenarios require different handling.

**Graceful shutdown**:
1. 节点 announces it is leaving
2. 节点 transfers all its keys to its clockwise successor(s)
3. Ring topology is updated
4. No data loss, minimal disruption

**Crash recovery**:
1. Other 节点 detect the 故障 (missed heartbeats)
2. The successor takes over the key range
3. Data is recovered from replica copies
4. New replicas are created to restore the 复制 factor

```JSON
请求:  {"type": "ring_remove_node", "msg_id": 1, "节点": "n2", "mode": "graceful"}
响应: {"type": "ring_remove_node_ok", "in_reply_to": 1, "keys_migrated": 333, "target_nodes": ["n1", "n3"], "mode": "graceful"}
```

## 涉及概念

- `node removal`
- `graceful shutdown`
- `crash recovery`
- `key takeover`
- `successor promotion`

## 实现提示

- On graceful shutdown: 节点 transfers its keys to its clockwise successor before leaving
- On crash: the successor detects the 故障和takes over the key range
- Graceful is faster (pre-transfer), crash requires recovery from replicas
- With virtual 节点, keys from the removed vnodes distribute to multiple successors
- Replica copies ensure no data loss even on crash

## 测试用例

### 1. Graceful removal migrates keys

ring_remove_node_ok should show keys migrated to remaining 节点.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n2","mode":"graceful"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Crash recovery takes over key range

Crash mode should trigger recovery from replicas.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n3","mode":"crash"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing:节点Removal](https://www.akamai.com/us/en/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf)：Akamai consistent hashing paper on 节点 join/leave strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
