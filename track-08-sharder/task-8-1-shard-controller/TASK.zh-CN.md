# 实现分片控制器

英文标题：Implement Shard Controller
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-1-shard-controller>

课程：8. 分片器：水平扩展与数据迁移
任务序号：1
短标题：分片控制器
难度：高级
子主题：Range Sharding

## 中文导读

本题要求你实现一个分片控制器（Shard Controller），它负责管理"哪个副本组拥有哪些分片"的映射关系。分片控制器是整个分片系统的"大脑"，所有节点都依赖它来获取最新的分片分配信息。理解分片控制器的工作原理，是构建可水平扩展的分布式存储系统的关键一步。

## 题目说明

构建一个分片控制器，用于管理分片的分配：

1. 维护配置信息：记录每个副本组（Replica Group）拥有哪些分片
2. 支持以下操作：加入（添加副本组）、离开（移除副本组）、移动（重新分配分片）
3. 使用 Raft 复制控制器状态，保证容错性
4. 将分片尽量均匀地分配到各个副本组
5. 提供配置查询接口

控制器是分片归属关系的唯一权威来源。

## 概念说明

### 分片（Sharding）

当数据量超过单台机器的存储能力时，就需要将数据拆分到多台机器上，每台机器负责一部分数据，这就是分片。每个分片处理一个键的子集，通过分片可以实现水平扩展。

### 分片控制器

分片控制器决定每个分片应该放在哪里。它通常由一个小型 Raft 集群来实现，以保证高可用。配置变更会带上版本号，方便协调数据迁移。

## 涉及概念

- `sharding`
- `configuration`
- `coordination`

## 实现提示

- 控制器管理分片到副本组的映射关系
- 使用 Raft 进行控制器状态复制
- 支持加入、离开、移动操作

## 测试用例

### 1. 加入新的副本组

配置版本号递增，副本组 g1 被添加，包含服务器 [s1, s2]，全部 10 个分片都分配给 g1。

输入：

```json
{"src":"c0","dest":"controller","body":{"type":"init","msg_id":1,"node_id":"controller","node_ids":["controller"]}}
{"src":"c1","dest":"controller","body":{"type":"join","msg_id":2,"gid":"g1","servers":["s1","s2"]}}
{"src":"c1","dest":"controller","body":{"type":"query","msg_id":3,"num":-1}}
```

期望输出：

```text
{"src":"controller","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"controller","dest":"c1","body":{"type":"join_ok","in_reply_to":2,"msg_id":1}}
{"src":"controller","dest":"c1","body":{"type":"query_ok","in_reply_to":3,"msg_id":2,"version":1,"groups":{"g1":["s1","s2"]},"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g1","5":"g1","6":"g1","7":"g1","8":"g1","9":"g1"}}}
```

## 参考资料

- [MIT 6.824 Lab 4](https://pdos.csail.mit.edu/6.824/labs/lab-shard.html)：分片键值存储实验

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
