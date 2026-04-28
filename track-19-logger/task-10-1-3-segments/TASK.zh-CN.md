# 添加带偏移量索引的 WAL 分段文件

英文标题：Add WAL Segment Files with Offset Index
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-3-segments>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：3
短标题：WAL Segments
难度：高级
子主题：提交日志（WAL）

## 中文导读

本题要求你为 WAL 实现分段文件机制。单个 WAL 文件会无限增长，导致查找变慢且无法高效清理。通过将日志拆分为多个段文件，并建立偏移量索引，可以实现快速定位和独立管理旧数据。这正是 Kafka 等生产级系统组织日志的方式。

## 题目说明

单个 WAL 文件存在一个问题：它会无限增长。一旦文件达到几个 GB，查找操作就会变慢，而且不重写整个文件就无法进行清理。

解决方案是使用**分段文件（Segment Files）**。当一个 WAL 段超过大小阈值时，将其封存（变为不可变），然后打开一个新的活跃段。偏移量索引（Offset Index）通过将每个日志偏移量映射到正确的段文件和字节位置，实现 O(1) 的查找效率。

Kafka、etcd 以及大多数生产系统都是这样组织日志的：
1. 段文件以其起始偏移量命名（例如 `00000000.log`、`00001000.log`）
2. 每个段都有一个配套的 `.index` 文件，记录偏移量到字节位置的映射
3. 旧的已封存段可以独立删除、压缩或归档
4. 只有活跃段接收新的写入

```json
Request:  {"type": "wal_segment_config", "msg_id": 1, "max_segment_bytes": 67108864}
Response: {"type": "wal_segment_config_ok", "in_reply_to": 1, "max_segment_bytes": 67108864}

Request:  {"type": "wal_segment_info", "msg_id": 2}
Response: {"type": "wal_segment_info_ok", "in_reply_to": 2, "segments": [
    {"file": "00000000.log", "start_offset": 0, "end_offset": 999, "size_bytes": 67108000, "sealed": true},
    {"file": "00001000.log", "start_offset": 1000, "end_offset": 1050, "size_bytes": 5120, "sealed": false}
], "active_segment": "00001000.log"}
```

## 涉及概念

- `segment files`
- `log segmentation`
- `offset index`
- `fast seeks`
- `immutable segments`

## 实现提示

- 当活跃段超过大小阈值（例如 64MB）时，将其封存并打开一个新段
- 维护一个索引映射（日志偏移量 -> 段文件 + 字节偏移量），以实现 O(1) 的查找
- 已封存的段是不可变的，可以安全地压缩、归档或删除
- 段文件以起始偏移量命名：00000000.log、00001000.log 等
- 这正是 Kafka 在磁盘上组织其分区日志的方式

## 测试用例

### 1. 配置段大小阈值

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_config","msg_id":2,"max_segment_bytes":1024}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_segment_config_ok", "in_reply_to": 2, "max_segment_bytes": 1024, "msg_id": 1}}
```

### 2. 空日志时查看段信息应显示活跃段

返回的 wal_segment_info_ok 中应至少包含 1 个 sealed 为 false 的段（即活跃段）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Kafka Log Segments](https://kafka.apache.org/documentation/#design_filesystem)：介绍 Kafka 如何将分区日志组织为段文件，以实现高效存储和清理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
