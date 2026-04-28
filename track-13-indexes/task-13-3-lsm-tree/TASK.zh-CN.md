# 实现 LSM 树

英文标题：Implement LSM Tree
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-3-lsm-tree>

课程：13. 索引
任务序号：3
短标题：LSM 树
难度：高级

## 中文导读

这道题要求你实现一个日志结构合并树（Log-Structured Merge Tree，简称 LSM 树）。LSM 树是一种为写入密集型场景优化的存储结构。它先将数据写入内存中的有序表，满了之后再批量刷写到磁盘。这种设计将随机写入转化为顺序写入，大幅提升写入吞吐量。Cassandra、RocksDB、LevelDB 等知名存储系统都采用了 LSM 树。

## 题目说明

构建一个日志结构合并树：

1. 写入操作首先进入内存中的 memtable（一个有序数据结构）
2. 当 memtable 写满后，将其刷写到磁盘上的 SSTable 文件
3. SSTable（Sorted String Table）是不可变的，且内部数据有序
4. 读取时先查 memtable，再依次查各个 SSTable（从最新的开始）
5. 后台执行压缩（Compaction），合并多个 SSTable

LSM 树通过使用顺序写入来优化写入吞吐量。

## 概念说明

### LSM 树的架构

LSM 树先将写入数据缓存在内存中（memtable），然后将有序的数据批量刷写到磁盘（SSTable）。这样就把随机写入转化为了顺序写入，极大地提高了写入性能。你可以把它想象成先在便签纸上快速记录，攒够一叠后再按顺序整理归档到文件夹中。Cassandra 和 RocksDB 等系统都使用了这种设计。

### 压缩

随着 SSTable 文件越来越多，读取性能会下降（因为需要逐一检查每个文件）。压缩操作将多个 SSTable 合并在一起，同时删除已标记删除的键，合并重叠的范围。常见的压缩策略有大小分层压缩和分层压缩两种。

## 涉及概念

- `LSM tree`
- `memtable`
- `SSTable`
- `compaction`

## 实现提示

- 写入时先写入内存中的 memtable
- memtable 满了之后刷写到有序的 SSTable 文件
- 在后台执行 SSTable 的压缩合并

## 测试用例

### 1. LSM 写入与读取

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_put","msg_id":2,"key":"x","value":100}}
{"src":"c2","dest":"n1","body":{"type":"lsm_get","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"lsm_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"lsm_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## 参考资料

- [LSM Tree Paper](https://www.cs.umb.edu/~poneil/lsmtree.pdf)：日志结构合并树的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
