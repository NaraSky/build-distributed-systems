# 添加快照支持以压缩日志

英文标题：Add Snapshot Support for Log Compaction
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-4-snapshot>

课程：6. 共识：Raft 与日志复制
任务序号：9
短标题：快照
难度：高级
子主题：提交与应用

## 中文导读

这道题要求你为 Raft 添加快照（Snapshot）支持，用于压缩日志。随着系统运行，日志会越来越长，不可能无限增长。快照的思路很简单：把状态机的当前状态保存下来，然后丢弃之前的日志。如果某个跟随者落后太多，领导者可以直接发送快照而不是逐条发送日志。这是让 Raft 在生产环境中可用的关键功能。

## 题目说明

为 Raft 添加快照支持以压缩日志。当日志增长超过阈值时，对状态机进行快照。落后太多的跟随者将收到快照，而不是逐条接收日志条目。

```json
Request:  {"type": "take_snapshot", "msg_id": 1, "threshold": 5}
Response: {"type": "take_snapshot_ok", "in_reply_to": 1, "snapshot_index": 5, "snapshot_term": 2, "state_size_bytes": 256, "log_entries_trimmed": 5}

Request:  {"type": "install_snapshot", "msg_id": 2, "snapshot_index": 5, "snapshot_term": 2, "state": {"x": "1", "y": "2", "z": "3"}}
Response: {"type": "install_snapshot_ok", "in_reply_to": 2, "applied": true, "new_last_applied": 5}

Request:  {"type": "get_log_info", "msg_id": 3}
Response: {"type": "get_log_info_ok", "in_reply_to": 3, "first_index": 6, "last_index": 8, "snapshot_index": 5, "total_entries": 3}
```

## 涉及概念

- `snapshot`
- `log compaction`
- `InstallSnapshot RPC`
- `state transfer`

## 实现提示

- 当日志超过阈值（例如 1000 条）时，对状态机进行快照
- 快照记录了在某个索引和任期下的完整状态
- 快照完成后，该索引之前的日志条目可以被丢弃
- 落后太多的跟随者通过 InstallSnapshot RPC 接收快照
- 快照会替换状态机的状态以及快照索引之前的日志

## 测试用例

### 1. 快照后裁剪日志

take_snapshot_ok 的结果应显示 snapshot_index 为 3，log_entries_trimmed 为 3。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}},{"index":3,"term":1,"command":{"op":"put","key":"z","value":"3"}}]}}
{"src":"c1","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"threshold":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 安装快照恢复状态

install_snapshot_ok 的 applied 字段为 true。get_state_ok 的 state 应为 {"a": "1", "b": "2"}。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"install_snapshot","msg_id":2,"snapshot_index":5,"snapshot_term":2,"state":{"a":"1","b":"2"}}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft - Log Compaction](https://raft.github.io/raft.pdf)：Raft 论文第 7 节，关于日志压缩和快照的说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
