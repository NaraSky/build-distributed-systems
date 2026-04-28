# 实现 a Write-Ahead 日志

英文标题：Implement a Write-Ahead Log
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-1-wal-impl>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：1
短标题：WAL Implementation
难度：intermediate
子主题：The Commit 日志 (WAL)

## 中文导读

本题要求你完成 `实现 a Write-Ahead 日志`。

重点关注：`write-ahead log`、`append-only`、`checksum`、`durability`、`fsync`。

建议先按提示逐步实现：Each entry format: [4-byte length][4-byte CRC32 checksum][payload bytes]。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The Write-Ahead 日志 (WAL) is the most fundamental durability primitive in 分布式系统. Every database (PostgreSQL, MySQL, SQLite), every 共识 algorithm (Raft, Paxos),和every 消息 broker (Kafka) uses a WAL at its core.

The key insight: **日志 the change BEFORE applying it to state**. If the system crashes at any point, the WAL can be replayed to recover the exact pre-crash state.

Implement a WAL，包含these properties:
1. **Append-only**: entries are never modified, only appended
2. **Checksummed**: each entry includes a CRC32 checksum to detect corruption
3. **Durable**: entries are fsynced to disk before acknowledging

Entry format: `[4-byte length][4-byte CRC32 checksum][payload bytes]`

```JSON
请求:  {"type": "wal_append", "msg_id": 1, "payload": "set x=42"}
响应: {"type": "wal_append_ok", "in_reply_to": 1, "offset": 0, "length": 8, "checksum": "abc123"}

请求:  {"type": "wal_read", "msg_id": 2, "offset": 0}
响应: {"type": "wal_read_ok", "in_reply_to": 2, "payload": "set x=42", "checksum_valid": true}

请求:  {"type": "wal_info", "msg_id": 3}
响应: {"type": "wal_info_ok", "in_reply_to": 3, "entries": 1, "total_bytes": 16, "fsynced": true}
```

## 涉及概念

- `write-ahead log`
- `append-only`
- `checksum`
- `durability`
- `fsync`

## 实现提示

- Each entry format: [4-byte length][4-byte CRC32 checksum][payload bytes]
- Write to disk和fsync BEFORE acknowledging the caller — this is the "write-ahead" guarantee
- The checksum detects torn writes: if a crash happens mid-write, the partial entry will have an invalid checksum
- Use CRC32用于checksums — fast和sufficient用于detecting corruption
- The WAL is append-only: never modify existing entries, only add new ones at the end

## 测试用例

### 1. Append a single entry和read it back

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=42"}}
{"src":"c1","dest":"n1","body":{"type":"wal_read","msg_id":3,"offset":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_read_ok", "in_reply_to": 3, "payload": "set x=42", "checksum_valid": true, "msg_id": 2}}
```

### 2. Multiple appends increment offset

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"op1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"op2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":4,"payload":"op3"}}
{"src":"c1","dest":"n1","body":{"type":"wal_info","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 3, "offset": 1, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 4, "offset": 2, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_info_ok", "in_reply_to": 5, "entries": 3, "msg_id": 4}}
```

## 参考资料

- [Write-Ahead Logging - PostgreSQL](https://www.postgresql.org/docs/current/wal-intro.html)：PostgreSQL WAL documentation explaining write-ahead logging fundamentals

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
