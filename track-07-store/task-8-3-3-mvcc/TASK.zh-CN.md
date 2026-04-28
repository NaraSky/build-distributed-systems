# 实现多版本并发控制

英文标题：Implement Multi-Version Concurrency Control
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-3-mvcc>

课程：7. 存储：线性一致键值存储
任务序号：13
短标题：MVCC
难度：高级
子主题：基于 Raft 的事务

## 中文导读

这道题要求你实现多版本并发控制（Multi-Version Concurrency Control，简称 MVCC）。MVCC 为每个键保留多个历史版本，读操作可以获取某个时间点的一致快照，完全不需要阻塞写操作。这是 PostgreSQL、MySQL InnoDB 和 TiKV 等主流数据库的核心并发控制机制。

## 题目说明

实现多版本并发控制：为每个键保留多个版本。读操作可以获取一致的快照，而不会阻塞写操作。

```json
Request:  {"type": "mvcc_put", "msg_id": 1, "key": "x", "value": "v1", "timestamp": 100}
Response: {"type": "mvcc_put_ok", "in_reply_to": 1, "version": 1, "timestamp": 100}

Request:  {"type": "mvcc_put", "msg_id": 2, "key": "x", "value": "v2", "timestamp": 200}
Response: {"type": "mvcc_put_ok", "in_reply_to": 2, "version": 2, "timestamp": 200}

Request:  {"type": "mvcc_get", "msg_id": 3, "key": "x", "read_timestamp": 150}
Response: {"type": "mvcc_get_ok", "in_reply_to": 3, "value": "v1", "version": 1, "as_of_timestamp": 100}

Request:  {"type": "mvcc_get", "msg_id": 4, "key": "x", "read_timestamp": 250}
Response: {"type": "mvcc_get_ok", "in_reply_to": 4, "value": "v2", "version": 2, "as_of_timestamp": 200}
```

## 涉及概念

- `MVCC`
- `versioned storage`
- `snapshot isolation`
- `readers never block writers`

## 实现提示

- 为每个键保留 N 个版本，每个版本标记一个提交时间戳
- 读操作根据自己的开始时间戳获取一致的快照
- 写操作创建新版本，不会阻塞正在进行的读操作
- 需要定期回收不再需要的旧版本
- PostgreSQL、MySQL InnoDB 和 TiKV 内部都是这样实现的

## 测试用例

### 1. 用旧时间戳读取到旧版本

验证 mvcc_get_ok 返回 value 为 "old"，因为读时间戳 150 小于新版本的写入时间戳 200。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":150}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 用当前时间戳读取到最新版本

验证 mvcc_get_ok 返回 value 为 "new"，因为读时间戳 300 大于最新版本的写入时间戳 200。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":300}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [MVCC in PostgreSQL](https://www.postgresql.org/docs/current/mvcc-intro.html)：PostgreSQL 如何通过 MVCC 实现并发访问

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
