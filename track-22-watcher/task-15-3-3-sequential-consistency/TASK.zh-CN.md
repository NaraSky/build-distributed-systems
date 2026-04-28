# Prove ZAB Sequential Consistency

英文标题：Prove ZAB Sequential Consistency
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-3-sequential-consistency>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：13
短标题：Sequential Consistency
难度：advanced
子主题：Consistency和the ZAB Protocol

## 中文导读

本题要求你完成 `Prove ZAB Sequential Consistency`。

重点关注：`sequential consistency`、`total order`、`linearizability vs sequential`、`ordering test`、`consistency verification`。

建议先按提示逐步实现：Sequential consistency: all clients see updates in the same order。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

ZAB provides sequential consistency: all clients observe updates in the same total order. This is the fundamental consistency guarantee of ZooKeeper.

**Sequential consistency means**:
1. All updates from a single 客户端 are applied in the order they were sent (FIFO 客户端 order)
2. All clients see updates in the same total order (global ordering)
3. Reads may be slightly stale (a Follower may not have the latest committed update yet)

**Test用于sequential consistency**:
- 客户端 A writes: `/x = 1`, then `/y = 2`
- 客户端 B writes: `/x = 3`, then `/y = 4`
- All observers must see either {A before B} or {B before A}, never interleaved out of order
- Under 最终一致性, an observer might see `/x=3, /y=2` (inconsistent mix)

```JSON
请求:  {"type": "consistency_test", "msg_id": 1, "writes": [{"客户端": "A", "ops": [{"path": "/x", "value": "1"}, {"path": "/y", "value": "2"}]}, {"客户端": "B", "ops": [{"path": "/x", "value": "3"}, {"path": "/y", "value": "4"}]}]}
响应: {"type": "consistency_test_ok", "in_reply_to": 1, "total_order": ["A:/x=1", "A:/y=2", "B:/x=3", "B:/y=4"], "sequential_consistent": true, "violations": 0}
```

## 涉及概念

- `sequential consistency`
- `total order`
- `linearizability vs sequential`
- `ordering test`
- `consistency verification`

## 实现提示

- Sequential consistency: all clients see updates in the same order
- This is weaker than linearizability: reads may be stale (from a Follower)
- Test: two clients write concurrently. All observers must see writes in the same order.
- This test would FAIL under 最终一致性 but PASSES under ZAB
- ZAB guarantees FIFO 客户端 order + total order of all committed writes

## 测试用例

### 1. Sequential consistency test passes

consistency_test_ok should show sequential_consistent: true和violations: 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/x","value":"1"}]},{"client":"B","ops":[{"path":"/y","value":"2"}]}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Client FIFO order preserved

In total_order, A:/a=1 must appear before A:/a=2 (FIFO per 客户端).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/a","value":"1"},{"path":"/a","value":"2"}]}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Consistency Guarantees](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkGuarantees)：ZooKeeper documentation on sequential consistency和ordering guarantees

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
