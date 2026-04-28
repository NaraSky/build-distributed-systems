# 实现 Consistent Hashing用于Sharding

英文标题：Implement Consistent Hashing用于Sharding
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-2-consistent-hash>

课程：8. 分片器：水平扩展与数据迁移
任务序号：2
短标题：Consistent Hash
难度：intermediate
子主题：Range Sharding

## 中文导读

本题要求你完成 `实现 Consistent Hashing用于Sharding`。

重点关注：`consistent hashing`、`key distribution`、`virtual nodes`。

建议先按提示逐步实现：Hash keys to ring positions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Use consistent hashing用于分片 assignment:

1. Place shards on a hash ring
2. Hash each key to a ring position
3. Find the next 分片 clockwise from key position
4. Use virtual 节点用于better distribution
5. Minimize key movement when shards join/leave

## 概念说明

### Consistent Hashing用于Sharding

Traditional modulo hashing (key % N) redistributes most keys when N changes. Consistent hashing only moves keys between affected neighbors, minimizing data migration during rebalancing.

### Virtual Nodes

With few shards, the ring may be imbalanced. Virtual 节点 give each 分片 multiple ring positions, smoothing distribution. Typically 100-200 virtual 节点 per 分片.

## 涉及概念

- `consistent hashing`
- `key distribution`
- `virtual nodes`

## 实现提示

- Hash keys to ring positions
- Use virtual 节点用于balance
- Minimal movement on changes

## 测试用例

### 1. Hash key to ring

Hash returns a numeric value. Exact hash depends on implementation but must be deterministic.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hash_key","msg_id":2,"key":"mykey"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"hash_key_ok","in_reply_to":2,"msg_id":1,"key":"mykey"}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
