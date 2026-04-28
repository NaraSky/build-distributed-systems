# 处理领导者更替：选举时追加空操作

英文标题：Handle Leader Changes with No-Op on Election
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-3-noop-on-election>

课程：6. 共识：Raft 与日志复制
任务序号：8
短标题：选举时追加空操作
难度：高级
子主题：提交与应用

## 中文导读

这道题要求你实现"选举时追加空操作（No-Op）"的技巧。新领导者当选后，它无法确定前任领导者遗留的哪些日志已经被提交。为了安全起见，新领导者会立即追加一条空操作日志。一旦这条空操作被多数节点确认，之前所有的日志就都被间接提交了。这是 Raft 中一个非常精巧的设计，解决了领导者更替时的安全性问题。

## 题目说明

当新领导者当选时，它不能直接应用前任期中未提交的日志条目。空操作（No-Op）技巧可以解决这个问题：新领导者立即在自己的任期内追加一条空操作条目。一旦这条空操作被提交（多数节点复制），之前的所有条目也随之被提交。

```json
Request:  {"type": "leader_change", "msg_id": 1, "new_leader": "n2", "new_term": 3, "log": [
    {"index": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"index": 2, "term": 2, "command": {"op": "put", "key": "y", "value": "2"}},
    {"index": 3, "term": 2, "command": {"op": "put", "key": "z", "value": "3"}}
], "commit_index": 1}
Response: {"type": "leader_change_ok", "in_reply_to": 1, "noop_appended_at": 4, "noop_term": 3, "safe_to_apply_after_commit": true}

Request:  {"type": "simulate_noop_commit", "msg_id": 2, "noop_index": 4}
Response: {"type": "simulate_noop_commit_ok", "in_reply_to": 2, "new_commit_index": 4, "entries_now_committed": [2, 3, 4]}
```

## 涉及概念

- `no-op entry`
- `leader change`
- `uncommitted entries`
- `safety`

## 实现提示

- 新领导者无法判断前任期中哪些日志已经被提交
- 空操作技巧：新领导者在自己的任期内追加一条空操作条目
- 一旦空操作被提交，之前的所有条目也随之被提交
- 这避免了新领导者错误地应用前任期中未提交的日志
- 空操作是一条不会修改状态的虚拟命令

## 测试用例

### 1. 新领导者追加空操作

leader_change_ok 的结果应显示 noop_appended_at 为 2，noop_term 为 3。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":3,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}}],"commit_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 空操作提交后推进之前所有条目

simulate_noop_commit_ok 的结果应显示 new_commit_index 为 3，entries_now_committed 为 [1, 2, 3]。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":2,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}}],"commit_index":0}}
{"src":"c1","dest":"n1","body":{"type":"simulate_noop_commit","msg_id":3,"noop_index":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft - Committing entries from previous terms](https://raft.github.io/raft.pdf)：Raft 论文第 5.4.2 节，关于如何通过空操作安全地提交前任期日志

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
