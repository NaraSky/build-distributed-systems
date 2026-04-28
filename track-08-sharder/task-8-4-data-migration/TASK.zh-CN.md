# 实现数据迁移

英文标题：Implement Data Migration
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-8-4-data-migration>

课程：8. 分片器：水平扩展与数据迁移
任务序号：4
短标题：数据迁移
难度：高级
子主题：Range Sharding

## 中文导读

本题要求你实现副本组之间的数据迁移。当分片的归属发生变化时，数据需要从旧的副本组搬到新的副本组。这个过程必须保证原子性和一致性，同时还要处理失败重试等异常情况，是分片系统中最复杂的环节之一。

## 题目说明

实现副本组之间的数据迁移：

1. 源副本组：停止接受待迁移分片的写入请求
2. 创建分片数据和客户端会话的快照
3. 将快照发送给目标副本组
4. 目标副本组：安装快照，开始服务该分片
5. 源副本组：收到确认后删除本地分片数据

需要处理各种失败情况：重试、幂等性、回滚。

## 概念说明

### 数据迁移

迁移分片就是搬运数据。每个分片的迁移必须是原子性的，且要保持一致性。在迁移过程中，分片可能暂时不可用，或者仍由源端提供服务（允许过时读取），直到传输完成。

### 客户端会话迁移

别忘了客户端的去重状态。如果不把会话信息一起迁移，客户端在重试时可能会看到操作被重复执行。因此，客户端会话表需要和分片数据一起传输。

## 涉及概念

- `migration`
- `data transfer`
- `consistency`

## 实现提示

- 迁移期间停止对该分片的服务
- 传输所有键值对
- 包含客户端会话状态

## 测试用例

### 1. 准备分片迁移

分片 3 被锁定，创建快照，其中包含数据 {x:1, y:2}。

输入：

```json
{"src":"c0","dest":"g1","body":{"type":"init","msg_id":1,"node_id":"g1","node_ids":["g1","g2"]}}
{"src":"c0","dest":"g1","body":{"type":"seed_shard","msg_id":2,"shard":3,"data":{"x":1,"y":2}}}
{"src":"c0","dest":"g1","body":{"type":"prepare_migration","msg_id":3,"shard":3,"target_gid":"g2"}}
```

期望输出：

```text
{"src":"g1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"g1","dest":"c0","body":{"type":"seed_shard_ok","in_reply_to":2,"msg_id":1}}
{"src":"g1","dest":"c0","body":{"type":"prepare_migration_ok","in_reply_to":3,"msg_id":2,"shard":3,"target_gid":"g2","snapshot":{"data":{"x":1,"y":2}}}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
