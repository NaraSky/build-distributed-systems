# 实现状态机的应用通道

英文标题：Implement the Apply Channel for State Machine
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-2-apply-channel>

课程：6. 共识：Raft 与日志复制
任务序号：7
短标题：应用通道
难度：进阶
子主题：提交与应用

## 中文导读

这道题要求你实现一个应用通道（Apply Channel），将已提交的日志条目按顺序传递给状态机执行。状态机是一个简单的键值存储，支持写入、读取和删除操作。这个通道是连接"日志共识"和"实际业务逻辑"的桥梁，实现了从理论到实践的最后一步。

## 题目说明

实现一个应用通道，将已提交的日志条目传递给状态机。状态机是一个简单的键值存储，支持 `Put`、`Get` 和 `Delete` 三种操作。

```json
Request:  {"type": "apply_entries", "msg_id": 1, "entries": [
    {"index": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"index": 2, "term": 1, "command": {"op": "put", "key": "y", "value": "2"}},
    {"index": 3, "term": 1, "command": {"op": "get", "key": "x"}}
]}
Response: {"type": "apply_entries_ok", "in_reply_to": 1, "results": [
    {"index": 1, "result": "ok"},
    {"index": 2, "result": "ok"},
    {"index": 3, "result": "1"}
], "last_applied": 3}

Request:  {"type": "get_state", "msg_id": 2}
Response: {"type": "get_state_ok", "in_reply_to": 2, "state": {"x": "1", "y": "2"}, "last_applied": 3}
```

## 涉及概念

- `apply channel`
- `state machine`
- `committed entries`
- `deterministic replay`

## 实现提示

- 已提交的日志条目按顺序流入应用通道
- 状态机从通道中读取命令并按顺序执行
- 已应用的条目不能被重复应用（需要记录 lastApplied 索引）
- 状态机必须是确定性的：相同的命令序列产生相同的状态
- 命令的流转路径为：客户端 -> 领导者日志 -> 复制 -> 提交 -> 应用

## 测试用例

### 1. 应用写入命令构建状态

get_state_ok 的结果应显示 state 为 {"x": "hello"}，last_applied 为 1。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"hello"}}]}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 应用读取命令返回当前值

apply_entries_ok 的 results 中，索引 1 的结果为 ok，索引 2 的结果为 "42"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"42"}},{"index":2,"term":1,"command":{"op":"get","key":"x"}}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [State Machine Replication](https://en.wikipedia.org/wiki/State_machine_replication)：介绍复制状态机如何从日志中按确定性顺序执行命令

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
