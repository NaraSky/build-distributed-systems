# 实现内存中的 MemTable

英文标题：Implement an In-Memory MemTable
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-1-memtable>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：6
短标题：MemTable
难度：进阶
子主题：LSM 树（Log-Structured Merge Tree）

## 中文导读

本题要求你实现一个内存表（MemTable），它是 LSM 树中所有写入操作的入口。MemTable 本质上是一个内存中的有序数据结构，充当写入缓冲区。理解它的工作原理，是掌握 LSM 存储引擎写入路径的第一步。

## 题目说明

内存表（MemTable）是 LSM 树中所有写入操作的入口。它是一个内存中的有序数据结构（通常是跳表或红黑树），充当写入缓冲区。

它在 LSM 写入路径中的工作方式如下：
1. **写入**：将键值对插入 MemTable（时间复杂度 O(log N)）
2. **读取**：先查 MemTable。如果找到了键，立即返回（这是最新的数据）。如果没找到，再去磁盘上的 SSTable 中查找
3. **刷盘**：当 MemTable 超过大小阈值（例如 4MB）时，将其冻结，创建一个新的空 MemTable 接收新写入，然后将冻结的 MemTable 刷写到磁盘，生成一个不可变的 SSTable

MemTable 必须支持以下操作：
- `put(key, value)` —— 插入或更新
- `get(key)` —— 单点查询
- `scan(start, end)` —— 范围扫描（有序遍历）

```json
Request:  {"type": "memtable_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
Response: {"type": "memtable_put_ok", "in_reply_to": 1, "size_bytes": 64}

Request:  {"type": "memtable_get", "msg_id": 2, "key": "user:1"}
Response: {"type": "memtable_get_ok", "in_reply_to": 2, "value": "Alice", "source": "memtable"}

Request:  {"type": "memtable_scan", "msg_id": 3, "start": "user:1", "end": "user:5"}
Response: {"type": "memtable_scan_ok", "in_reply_to": 3, "entries": [
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

- 所有写入都先进入 MemTable，它是 LSM 树的"写入缓冲区"
- 使用有序数据结构（跳表或红黑树），以实现 O(log N) 的插入和有序遍历
- 读取时先查 MemTable，再查磁盘上的 SSTable（最新数据优先）
- 当 MemTable 超过阈值（例如 4MB）时，将其冻结并刷写到磁盘生成 SSTable
- MemTable 支持范围扫描，因为它是有序的，这一点与哈希表不同

## 测试用例

### 1. 写入并读取

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

### 2. 查询不存在的键返回 null

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

- [LSM Tree MemTable](https://www.scylladb.com/glossary/memtable/)：介绍内存表在基于 LSM 的存储引擎中如何作为内存写入缓冲区工作

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
