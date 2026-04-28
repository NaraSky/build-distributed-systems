# 实现乐观并发控制

英文标题：Implement Optimistic Concurrency Control
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-2-occ>

课程：7. 存储：线性一致键值存储
任务序号：12
短标题：OCC
难度：高级
子主题：基于 Raft 的事务

## 中文导读

这道题要求你实现乐观并发控制（Optimistic Concurrency Control，简称 OCC）。OCC 的核心思想是"先乐观地执行，提交时再检查冲突"。读取数据时记录版本号，提交时检查版本号是否发生变化，如果没变就提交成功，如果变了就中止并重试。这种方式在冲突较少的场景下效率很高。

## 题目说明

实现乐观并发控制。读取键时记录其版本号，提交事务时检查所有读取过的键的版本号是否发生了变化，只有全部未变时才允许提交。

```json
Request:  {"type": "occ_begin", "msg_id": 1}
Response: {"type": "occ_begin_ok", "in_reply_to": 1, "txn_id": "t1"}

Request:  {"type": "occ_read", "msg_id": 2, "txn_id": "t1", "key": "x"}
Response: {"type": "occ_read_ok", "in_reply_to": 2, "value": "42", "version": 5}

Request:  {"type": "occ_commit", "msg_id": 3, "txn_id": "t1", "writes": [{"key": "x", "value": "43"}], "read_versions": [{"key": "x", "version": 5}]}
Response: {"type": "occ_commit_ok", "in_reply_to": 3, "committed": true, "new_version": 6}
```

## 涉及概念

- `OCC`
- `version check`
- `conflict detection`
- `abort and retry`

## 实现提示

- 读取一组键并记录它们的版本号
- 提交时检查这些键的版本号是否发生了变化
- 如果版本号匹配则事务提交成功，否则中止并重试
- 乐观并发控制在冲突较少时效果很好（这正是"乐观"的含义）
- 高竞争场景下会导致大量中止和重试

## 测试用例

### 1. 版本号匹配时提交成功

验证 occ_commit_ok 中 committed 为 true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_begin","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":3,"txn_id":"t1","writes":[{"key":"x","value":"1"}],"read_versions":[]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 版本号不匹配时事务中止

验证 occ_commit_ok 中 committed 为 false，因为版本号 999 与实际版本不匹配。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":2,"txn_id":"t1","writes":[{"key":"x","value":"new"}],"read_versions":[{"key":"x","version":999}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Optimistic Concurrency Control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)：乐观并发控制概述，包括读、验证、写三个阶段

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
