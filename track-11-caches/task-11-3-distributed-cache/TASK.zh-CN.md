# 实现基于一致性哈希的分布式缓存

网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-3-distributed-cache>

课程：11. 缓存
任务序号：3
短标题：分布式缓存
难度：进阶

## 中文导读

这道题要求你使用一致性哈希（Consistent Hashing）将缓存数据分散到多个缓存节点上。单台缓存服务器的内存有限，当数据量增长时，就需要把缓存"分片"存储到多台机器上。一致性哈希能保证在增删节点时尽量少地搬迁数据，是分布式缓存的核心技术。

## 题目说明

使用一致性哈希将缓存条目分布到多个缓存节点上。这样可以将缓存容量扩展到单个节点之外，同时保持高效的键查找。

你需要实现：
1. 为缓存节点构建一致性哈希环
2. 根据键的哈希值将请求路由到对应的节点
3. 处理节点加入或离开时的数据重新分配，确保影响的键尽可能少
4. 实现客户端库，自动路由请求到正确的节点

## 概念说明

### 分布式缓存

一台缓存服务器的内存是有限的。分布式缓存将数据分片存储在多台服务器上，每个键根据其哈希值被分配到特定的服务器。这种方式的容量可以随节点数量线性扩展。

### 一致性哈希

普通的取模哈希（key % N）在节点数 N 发生变化时，会导致大部分键需要重新分配。一致性哈希则大幅减少了这种影响：增加或移除一个节点时，只有该节点和它在哈希环上相邻节点之间的键需要迁移。

### 虚拟节点

当物理节点数量较少时，哈希环上的分布可能不均匀。虚拟节点（Virtual Nodes）的做法是让每台物理服务器对应哈希环上的多个位置，从而改善数据分布的均匀性。生产环境中通常为每台服务器配置 100 到 200 个虚拟节点。

## 涉及概念

- `consistent hashing`
- `partitioning`
- `horizontal scaling`

## 实现提示

- 通过哈希键来确定应该访问哪个缓存节点
- 使用一致性哈希来保证节点变化时的稳定性
- 妥善处理节点的增加和移除
- 在单节点测试时，将所有键存储在协调节点本地，因为代理目标节点并不存在

## 测试用例

### 1. 将键哈希到节点

使用一致性哈希对键 "mykey" 进行哈希，哈希环大小为 64。返回负责该键的缓存节点和在环上的位置。

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

- [Consistent Hashing Paper](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf)：一致性哈希的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
