#处理Node Addition，包含Minimal Key Migration

英文标题：Handle节点Addition，包含Minimal Key Migration
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-3-node-join>

课程：8. 分片器：水平扩展与数据迁移
任务序号：8
短标题：Node Join
难度：intermediate
子主题：Consistent Hashing

## 中文导读

本题要求你完成 `Handle节点Addition，包含Minimal Key Migration`。

重点关注：`node addition`、`key migration`、`minimal disruption`、`predecessor takeover`、`data transfer`。

建议先按提示逐步实现：When a new 节点 joins, it takes keys from its clockwise neighbor。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 节点 joins, it takes over a portion of the key space from its clockwise neighbor. Only the keys that now fall in the new 节点's range need to migrate.

**Join process**:
1. New 节点 N4 calculates its position on the ring
2. N4 finds its clockwise neighbor (successor) N2
3. Keys between N4's 计数器-clockwise neighbor和N4 are transferred from N2 to N4
4. Only ~1/N of total keys are affected (minimal disruption)

**With virtual 节点**: the new 节点 takes V positions on the ring, taking small ranges from multiple existing 节点. This distributes the migration load evenly.

```JSON
请求:  {"type": "ring_add_node", "msg_id": 1, "new_node": "n4"}
响应: {"type": "ring_add_node_ok", "in_reply_to": 1, "keys_migrated": 250, "total_keys": 1000, "migration_pct": 25.0, "source_nodes": ["n1", "n2", "n3"]}
```

## 涉及概念

- `node addition`
- `key migration`
- `minimal disruption`
- `predecessor takeover`
- `data transfer`

## 实现提示

- When a new 节点 joins, it takes keys from its clockwise neighbor
- Only keys between the new 节点和its 计数器-clockwise neighbor migrate
- This is ~1/N of total keys (vs. nearly 100%，包含modulo hashing)
- During migration, the old owner continues serving reads用于migrating keys
- After migration completes, redirect new requests to the new owner

## 测试用例

### 1.节点join migrates roughly 1/N keys

migration_pct should be roughly 25% (1/4用于4 节点).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Keys are still accessible after migration

ring_lookup_ok should return the new owner用于migrated keys.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n3"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"migrated-key"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing:节点Addition](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf)：Karger et al. - Consistent Hashing和Random Trees

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
