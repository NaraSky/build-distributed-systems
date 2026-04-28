# 实现 an In-Memory MemTable

英文标题：Implement an In-Memory MemTable
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-1-memtable>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：6
短标题：MemTable
难度：intermediate
子主题：LSM Tree (日志-Structured Merge Tree)

## 中文导读

本题要求你完成 `实现 an In-Memory MemTable`。

重点关注：`MemTable`、`sorted tree`、`skip list`、`write path`、`in-memory buffer`。

建议先按提示逐步实现：All writes go to the MemTable first — it is the "write buffer" of the LSM tree。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The MemTable is the entry point用于all writes in an LSM tree. It is an in-memory sorted data structure (typically a skip list or red-black tree) that acts as a write buffer.

How it works in the LSM write path:
1. **Write**: insert the key-value pair into the MemTable (O(日志 N))
2. **Read**: check the MemTable first. If the key is found, return it immediately (freshest data). If not, check SSTables on disk.
3. **Flush**: when the MemTable exceeds a size threshold (e.g. 4MB), freeze it, create a new empty MemTable用于new writes,和flush the frozen one to disk as an immutable SSTable.

The MemTable must support:
- `put(key, value)` — insert or update
- `get(key)` — point lookup
- `scan(start, end)` — range scan (sorted iteration)

```JSON
请求:  {"type": "memtable_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
响应: {"type": "memtable_put_ok", "in_reply_to": 1, "size_bytes": 64}

请求:  {"type": "memtable_get", "msg_id": 2, "key": "user:1"}
响应: {"type": "memtable_get_ok", "in_reply_to": 2, "value": "Alice", "source": "memtable"}

请求:  {"type": "memtable_scan", "msg_id": 3, "start": "user:1", "end": "user:5"}
响应: {"type": "memtable_scan_ok", "in_reply_to": 3, "entries": [
    {"key": "user:1", "value": "Alice"},
    {"key": "user:3", "value": "Bob"}
]}
```

## 涉及概念

- `MemTable`
- `sorted tree`
- `skip list`
- `write path`
- `in-memory buffer`

## 实现提示

- All writes go to the MemTable first — it is the "write buffer" of the LSM tree
- Use a sorted data structure (skip list or red-black tree)用于O(日志 N) inserts和sorted iteration
- Reads check the MemTable BEFORE checking any on-disk SSTables (freshest data wins)
- When the MemTable exceeds a threshold (e.g. 4MB), it is frozen和flushed to disk as an SSTable
- The MemTable supports range scans because it is sorted — unlike a hash map

## 测试用例

### 1. Put和get from memtable

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"memtable_put","msg_id":2,"key":"k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"memtable_get","msg_id":3,"key":"k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_put_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_get_ok", "in_reply_to": 3, "value": "v1", "source": "memtable", "msg_id": 2}}
```

### 2. Get用于missing key returns null

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"memtable_get","msg_id":2,"key":"nonexistent"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_get_ok", "in_reply_to": 2, "value": null, "source": "memtable", "msg_id": 1}}
```

## 参考资料

- [LSM Tree MemTable](https://www.scylladb.com/glossary/memtable/)：How memtables work as the in-memory write buffer in LSM-based 存储 engines

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
