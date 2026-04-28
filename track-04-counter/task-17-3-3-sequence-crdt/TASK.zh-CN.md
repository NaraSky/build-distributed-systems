# 实现 a Sequence CRDT用于Collaborative Text Editing

英文标题：Implement a Sequence CRDT用于Collaborative Text Editing
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-3-sequence-crdt>

课程：4. 计数器：分布式状态与 CRDT
任务序号：13
短标题：Sequence CRDT
难度：advanced
子主题：More CRDTs

## 中文导读

本题要求你完成 `实现 a Sequence CRDT用于Collaborative Text Editing`。

重点关注：`sequence CRDT`、`RGA`、`collaborative editing`、`position identifiers`、`concurrent inserts`。

建议先按提示逐步实现：Use RGA (Replicated Growable Array): each character has a unique position ID。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A Sequence CRDT enables collaborative text editing where multiple users can type simultaneously without conflicts. The RGA (Replicated Growable Array) assigns each character a unique, ordered position identifier.

**RGA design**:
- Each character has a unique ID: `(lamport_timestamp, node_id)`
- Characters are ordered by their IDs — the document is the sorted sequence
- Insert between positions P1和P2: create a new ID between them
- Delete: mark the character as a tombstone (keep the ID用于ordering)

**Concurrent inserts**: if two users insert at the same position, the tiebreaker is the 节点 ID. This ensures deterministic ordering across all replicas.

```JSON
请求:  {"type": "seq_insert", "msg_id": 1, "position": 0, "char": "H"}
响应: {"type": "seq_insert_ok", "in_reply_to": 1, "id": "1-n1"}

请求:  {"type": "seq_read", "msg_id": 2}
响应: {"type": "seq_read_ok", "in_reply_to": 2, "text": "Hello", "length": 5}
```

## 涉及概念

- `sequence CRDT`
- `RGA`
- `collaborative editing`
- `position identifiers`
- `concurrent inserts`

## 实现提示

- Use RGA (Replicated Growable Array): each character has a unique position ID
- Position IDs are ordered和never change — new characters get IDs between neighbors
- Delete marks a character as a tombstone (never physically removed)
-并发inserts at the same position are ordered by 节点 ID (tiebreaker)
- The final document is the sequence of non-tombstoned characters in position order

## 测试用例

### 1. Insert和read characters

seq_read_ok text should be "Hi".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"H"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"i"}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete marks character as tombstone

seq_read_ok text should be "B" (A was deleted).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"A"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"B"}}
{"src":"c1","dest":"n1","body":{"type":"seq_delete","msg_id":4,"position":0}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [RGA: Replicated Growable Array](https://doi.org/10.1016/j.jpdc.2010.12.006)：Roh et al. - Replicated abstract data types: Building blocks用于collaborative applications

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
