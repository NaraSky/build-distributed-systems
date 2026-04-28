# 构建迷你 TiKV：Raft + MVCC 分区

英文标题：Build a Mini TiKV with Raft + MVCC Regions
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-4-tikv-regions>

课程：7. 存储：线性一致键值存储
任务序号：14
短标题：TiKV Regions
难度：高级
子主题：基于 Raft 的事务

## 中文导读

这道题要求你构建一个迷你版的 TiKV：将整个键空间按范围划分为多个分区（Region），每个分区拥有独立的 Raft 组和 MVCC 存储。这是理解 TiKV 等工业级分布式存储系统架构的核心练习，让你亲手体验如何将一个单 Raft 组的键值存储扩展为支持海量数据的分布式系统。

## 题目说明

构建一个迷你版的 TiKV：将键空间划分为多个分区，每个分区拥有独立的 Raft 组和 MVCC 存储。

```json
Request:  {"type": "region_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
Response: {"type": "region_put_ok", "in_reply_to": 1, "region_id": 1, "key_range": ["a", "m"]}

Request:  {"type": "region_get", "msg_id": 2, "key": "user:1"}
Response: {"type": "region_get_ok", "in_reply_to": 2, "value": "Alice", "region_id": 1}

Request:  {"type": "region_info", "msg_id": 3}
Response: {"type": "region_info_ok", "in_reply_to": 3, "regions": [
    {"id": 1, "range": ["a", "m"], "leader": "n1", "size_bytes": 1024},
    {"id": 2, "range": ["m", "z"], "leader": "n2", "size_bytes": 512}
]}

Request:  {"type": "region_split", "msg_id": 4, "region_id": 1, "split_key": "g"}
Response: {"type": "region_split_ok", "in_reply_to": 4, "new_regions": [
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

- TiKV 将键空间按范围划分为多个分区
- 每个分区拥有独立的 Raft 组来进行数据复制
- 当一个分区过大时（例如超过 96MB）会进行分裂
- 跨分区的事务需要使用两阶段提交
- 调度驱动器（PD）负责管理分区到节点的映射关系

## 测试用例

### 1. 写入路由到正确的分区

验证 region_put_ok 中包含正确的 region_id，指向键所属的分区范围。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"region_put","msg_id":2,"key":"apple","value":"fruit"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 查看分区信息

验证 region_info_ok 中至少列出 1 个分区，包含分区编号、键范围和领导者信息。

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

- [TiKV Architecture](https://tikv.org/docs/deep-dive/introduction/)：TiKV 深入解析，涵盖分区、Raft 组和 MVCC

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
