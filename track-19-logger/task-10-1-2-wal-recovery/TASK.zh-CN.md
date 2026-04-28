# 实现启动时的 WAL 恢复

英文标题：Implement WAL Recovery on Startup
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-2-wal-recovery>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：2
短标题：WAL Recovery
难度：进阶
子主题：提交日志（WAL）

## 中文导读

本题要求你实现 WAL 的崩溃恢复机制。当节点崩溃重启后，需要扫描 WAL 文件，逐条验证校验和，将有效条目重放到状态机中，从而恢复到崩溃前的一致状态。这是所有数据库实现持久化的核心能力。

## 题目说明

WAL 恢复是持久化故事的另一半。当一个节点（Node）在崩溃后重新启动时，它必须扫描 WAL 并重放所有有效条目，以重建其状态。

恢复算法的步骤如下：
1. 打开 WAL 文件，按顺序读取条目
2. 对每个条目验证校验和（重新计算 CRC32 并与存储值比较）
3. 如果校验和匹配，则重放该条目（将操作应用到状态机）
4. 如果校验和无效，说明这是一次**不完整写入（torn write）**，即崩溃发生在写入过程中。跳过该条目及其后所有条目
5. 重放完成后，状态机将反映最后一个一致的状态

所有数据库都是这样从崩溃中恢复的：PostgreSQL 重放其 WAL，SQLite 重放其日志，Raft 重放其日志。

```json
Request:  {"type": "wal_recover", "msg_id": 1, "wal_entries": [
    {"offset": 0, "payload": "set x=1", "checksum": "valid"},
    {"offset": 1, "payload": "set y=2", "checksum": "valid"},
    {"offset": 2, "payload": "set z=", "checksum": "invalid"}
]}
Response: {"type": "wal_recover_ok", "in_reply_to": 1, "entries_replayed": 2, "entries_skipped": 1, "state": {"x": "1", "y": "2"}}
```

## 涉及概念

- `crash recovery`
- `log replay`
- `checksum validation`
- `torn writes`
- `state reconstruction`

## 实现提示

- 启动时，从 WAL 文件的开头按顺序扫描
- 对每个条目，重新计算 CRC32 校验和并与存储的值进行比较
- 校验和有效的条目会被重放以重建状态；校验和无效的条目会被跳过
- 不完整写入（崩溃发生在写入过程中）会产生一个部分条目，其校验和无效
- 恢复完成后，状态机与崩溃前最后一个一致状态完全相同

## 测试用例

### 1. 恢复时重放有效条目并跳过损坏条目

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set x=1","checksum":"valid"},{"offset":1,"payload":"set y=2","checksum":"valid"},{"offset":2,"payload":"set z=","checksum":"invalid"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 2, "entries_skipped": 1, "msg_id": 1}}
```

### 2. 所有条目都有效时全部重放

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set a=10","checksum":"valid"},{"offset":1,"payload":"set b=20","checksum":"valid"},{"offset":2,"payload":"set c=30","checksum":"valid"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 3, "entries_skipped": 0, "msg_id": 1}}
```

## 参考资料

- [ARIES Recovery Algorithm](https://en.wikipedia.org/wiki/Algorithms_for_Recovery_and_Isolation_Exploiting_Semantics)：经典的 ARIES 算法，用于数据库中基于 WAL 的崩溃恢复

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
