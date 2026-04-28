# 构建分布式哈希表（Chord）

英文标题：Build Distributed Hash Table (Chord)
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-2-dht>

课程：10. 高级主题
任务序号：2
短标题：DHT
难度：高级
子主题：高级范式

## 中文导读

本题要求你实现 Chord 分布式哈希表（DHT）。Chord 将节点排列在一个哈希环上，通过手指表（Finger Table）实现高效路由，只需要 O(log n) 次跳转就能找到目标数据。这是点对点（P2P）网络和分布式存储系统中的核心数据结构。

## 题目说明

构建 Chord 分布式哈希表：节点分布在哈希环上，使用手指表进行路由。在点对点网络中实现 O(log n) 的查找效率。

## 概念说明

### Chord 分布式哈希表

Chord 将节点排列在一个哈希环上。手指表记录了哈希环上前方 2^i 位置的节点信息，从而实现 O(log n) 次跳转的高效查找。你可以把哈希环想象成一个时钟表盘，每个节点占据一个位置，手指表就像是提前记好了"几点钟方向有谁"，这样查找时就不用一个一个问过去。Chord 被广泛应用于 P2P 系统和部分数据库中。

## 涉及概念

- `DHT`
- `Chord`
- `finger table`

## 实现提示

- 每个节点在哈希环上有一个唯一的标识
- 构建手指表以实现 O(log n) 的查找
- 处理节点的加入和离开

## 测试用例

### 1. 将键哈希到环上

验证响应包含 chord_hash_ok 类型，哈希值在 0 到 2^6-1（即 0-63）之间。哈希应具有一致性，即相同的键总是产生相同的哈希值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chord_hash","msg_id":2,"key":"mykey","m":6}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"chord_hash_ok","in_reply_to":2,"msg_id":1,"hash":7}}
```

## 参考资料

- [Chord Paper](https://pdos.csail.mit.edu/papers/chord:sigcomm01/)：Chord 可扩展的点对点查找服务论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
