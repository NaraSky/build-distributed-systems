# 用一致性哈希实现分片

英文标题：Implement Consistent Hashing for Sharding
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-2-consistent-hash>

课程：8. 分片器：水平扩展与数据迁移
任务序号：2
短标题：一致性哈希
难度：进阶
子主题：Range Sharding

## 中文导读

本题要求你使用一致性哈希（Consistent Hashing）来决定每个键应该分配到哪个分片。相比传统的取模哈希，一致性哈希在节点增减时只需迁移少量数据，是分布式系统中最常用的分片策略之一。

## 题目说明

使用一致性哈希来进行分片分配：

1. 将分片放置在哈希环上
2. 对每个键计算哈希值，映射到环上的某个位置
3. 从键的位置出发，沿顺时针方向找到第一个分片，该分片即为键的归属
4. 使用虚拟节点（Virtual Nodes）来改善数据分布的均匀性
5. 当分片加入或离开时，尽量减少键的迁移量

## 概念说明

### 一致性哈希与分片

传统的取模哈希（`key % N`）在节点数量 N 发生变化时，会导致大部分键被重新分配。而一致性哈希只会将键在相邻节点之间迁移，大大减少了重平衡时的数据搬运量。

### 虚拟节点

当分片数量较少时，哈希环上的分布可能不均匀。虚拟节点的做法是让每个分片在环上占据多个位置，从而使数据分布更加平滑。通常每个分片会设置 100 到 200 个虚拟节点。

## 涉及概念

- `consistent hashing`
- `key distribution`
- `virtual nodes`

## 实现提示

- 将键哈希到环上的位置
- 使用虚拟节点来平衡负载
- 节点变更时尽量减少键的迁移

## 测试用例

### 1. 将键哈希到环上

哈希函数返回一个数值。具体的哈希值取决于实现方式，但必须是确定性的。

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
