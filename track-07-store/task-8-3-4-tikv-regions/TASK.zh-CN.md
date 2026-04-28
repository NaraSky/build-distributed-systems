# 构建 a Mini TiKV，包含Raft + MVCC Regions

英文标题：Build a Mini TiKV，包含Raft + MVCC Regions
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-4-tikv-regions>

课程：7. 存储：线性一致 KV Store
任务序号：14
短标题：TiKV Regions
难度：advanced
子主题：Transactions on Raft

## 中文导读

本题要求你完成 `构建 a Mini TiKV，包含Raft + MVCC Regions`。

重点关注：`TiKV`、`regions`、`range partitioning`、`Raft per region`、`multi-region`。

建议先按提示逐步实现：TiKV splits the key space into ranges called regions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a mini version of TiKV: partition the key space into regions, each，包含its own Raft group和MVCC 存储.

```JSON
请求:  {"type": "region_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
响应: {"type": "region_put_ok", "in_reply_to": 1, "region_id": 1, "key_range": ["a", "m"]}

请求:  {"type": "region_get", "msg_id": 2, "key": "user:1"}
响应: {"type": "region_get_ok", "in_reply_to": 2, "value": "Alice", "region_id": 1}

请求:  {"type": "region_info", "msg_id": 3}
响应: {"type": "region_info_ok", "in_reply_to": 3, "regions": [
    {"id": 1, "range": ["a", "m"], "Leader": "n1", "size_bytes": 1024},
    {"id": 2, "range": ["m", "z"], "Leader": "n2", "size_bytes": 512}
]}

请求:  {"type": "region_split", "msg_id": 4, "region_id": 1, "split_key": "g"}
响应: {"type": "region_split_ok", "in_reply_to": 4, "new_regions": [
    {"id": 1, "range": ["a", "g"]},
    {"id": 3, "range": ["g", "m"]}
]}
```

## 涉及概念

- `TiKV`
- `regions`
- `range partitioning`
- `Raft per region`
- `multi-region`

## 实现提示

- TiKV splits the key space into ranges called regions
- Each region has its own Raft group用于复制
- A region splits when it gets too large (e.g., > 96MB)
- Cross-region transactions use 2-phase commit
- The placement driver (PD) manages region-to-节点 mapping

## 测试用例

### 1. Put routes to correct region

region_put_ok should include the region_id routing to the correct range.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"region_put","msg_id":2,"key":"apple","value":"fruit"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Region info shows partitions

region_info_ok should list at least 1 region，包含id, range,和Leader.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"region_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TiKV Architecture](https://tikv.org/docs/deep-dive/introduction/)：TiKV deep dive: regions, Raft groups,和MVCC

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
