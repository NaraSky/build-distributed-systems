# 实现带原子快照的 WAL 压缩

英文标题：Implement WAL Compaction with Atomic Snapshot
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-4-compaction>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：4
短标题：WAL Compaction
难度：高级
子主题：提交日志（WAL）

## 中文导读

本题要求你实现 WAL 的压缩机制。如果不做压缩，WAL 会永远增长下去。核心做法是：定期对状态机做快照，然后截断快照之前的所有日志条目。关键在于这个过程必须是原子性的，即使中途崩溃也不能丢失数据。

## 题目说明

如果不做压缩，WAL 会永远增长。所有数据库都用同一个模式来解决这个问题：定期对状态机做一次**快照（Snapshot）**，然后**截断**快照之前的所有 WAL 条目。

压缩算法的步骤如下：
1. 将当前状态机序列化到快照文件
2. 记录拍摄快照时的 WAL 偏移量
3. 删除该偏移量之前的所有 WAL 条目（段）
4. 恢复时：先加载快照，然后只重放快照偏移量之后的条目

关键要求是**原子性（Atomicity）**。如果系统在拍摄快照和截断 WAL 之间崩溃，不能有任何数据丢失。标准做法是：
- 先将快照写入临时文件
- 将临时文件原子性地重命名为最终的快照路径
- 重命名成功后，再删除旧的 WAL 段

```json
Request:  {"type": "wal_snapshot", "msg_id": 1}
Response: {"type": "wal_snapshot_ok", "in_reply_to": 1, "snapshot_offset": 500, "snapshot_size_bytes": 2048}

Request:  {"type": "wal_compact", "msg_id": 2, "snapshot_at_offset": 500}
Response: {"type": "wal_compact_ok", "in_reply_to": 2, "snapshot_offset": 500, "entries_before": 1000, "entries_after": 500, "bytes_freed": 32000}
```

## 涉及概念

- `log compaction`
- `snapshot`
- `truncation`
- `atomic operation`
- `space reclamation`

## 实现提示

- 一旦状态机的快照已生成，快照之前的旧 WAL 条目就不再需要了
- 流程为：拍摄快照 -> 记录快照偏移量 -> 删除该偏移量之前的 WAL 条目
- 快照和截断这两个操作必须是原子性的：如果在两者之间崩溃，就会导致数据丢失
- 先将快照写入临时文件，然后原子性地重命名到正式位置
- 恢复时：先加载快照，然后只重放快照偏移量之后的 WAL 条目

## 测试用例

### 1. 对当前状态拍摄快照

返回的 wal_snapshot_ok 中应包含 snapshot_offset >= 2 且 snapshot_size_bytes > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"set y=2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_snapshot","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 压缩释放旧条目

返回的 wal_compact_ok 中应显示 entries_after < entries_before 且 bytes_freed > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_compact","msg_id":2,"snapshot_at_offset":500}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Log Compaction in Kafka](https://kafka.apache.org/documentation/#compaction)：介绍 Kafka 如何实现日志压缩，在保留最新值的同时回收磁盘空间

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
