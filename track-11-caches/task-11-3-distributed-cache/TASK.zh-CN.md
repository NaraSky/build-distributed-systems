# 实现 Distributed 缓存，包含Consistent Hashing

英文标题：Implement Distributed Cache，包含Consistent Hashing
网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-3-distributed-cache>

课程：11. 缓存
任务序号：3
短标题：Distributed 缓存
难度：intermediate

## 中文导读

本题要求你完成 `实现 Distributed 缓存，包含Consistent Hashing`。

重点关注：`consistent hashing`、`partitioning`、`horizontal scaling`。

建议先按提示逐步实现：Hash keys to determine 缓存 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distribute 缓存 entries across multiple 缓存 节点使用consistent hashing. This scales 缓存 capacity beyond a single 节点 while maintaining efficient key lookup.

Implement:
1. Consistent hash ring用于缓存 节点
2. Key routing to appropriate 节点
3.处理 节点 join/leave，包含minimal key redistribution
4. 客户端 library that routes requests automatically

## 概念说明

### Distributed Caching

A single 缓存 服务端 has limited memory. Distributed caching shards data across multiple servers. Each key goes to a specific 服务端 based on its hash. This scales linearly，包含节点.

### Consistent Hashing

Regular modulo hashing (key % N) redistributes most keys when N changes. Consistent hashing minimizes redistribution: adding/removing a 节点 only affects keys between it和its neighbor on the ring.

### Virtual Nodes

With few physical 节点, the ring may be unbalanced. Virtual 节点 map each physical 服务端 to many ring positions, improving distribution. Most production systems use 100-200 virtual 节点 per 服务端.

## 涉及概念

- `consistent hashing`
- `partitioning`
- `horizontal scaling`

## 实现提示

- Hash keys to determine 缓存 节点
- Use consistent hashing用于stability
-处理节点 additions和removals gracefully
- Store all keys locally on the coordinator 节点 - in single-节点 testing the 代理 target does not exist

## 测试用例

### 1. Hash key to node

Hash key "mykey"使用consistent hashing，包含ring size 64. Returns responsible 缓存 节点和ring position.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","cache1","cache2","cache3"]}}
{"src":"c1","dest":"n1","body":{"type":"hash_key","msg_id":2,"key":"mykey","ring_size":64}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"hash_key_ok","in_reply_to":2,"msg_id":1,"key":"mykey","node":"cache2","ring_position":42}}
```

## 参考资料

- [Consistent Hashing Paper](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf)：Original consistent hashing paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
