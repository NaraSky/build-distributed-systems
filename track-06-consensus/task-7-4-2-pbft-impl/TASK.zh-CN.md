# 实现 Simplified PBFT，包含4 Nodes

英文标题：Implement Simplified PBFT，包含4 Nodes
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-2-pbft-impl>

课程：6. 共识：Raft 与日志复制
任务序号：17
短标题：PBFT Implementation
难度：advanced
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你完成 `实现 Simplified PBFT，包含4 Nodes`。

重点关注：`PBFT`、`pre-prepare`、`prepare`、`commit`、`three-phase protocol`。

建议先按提示逐步实现：PBFT uses 3 phases: Pre-prepare, Prepare, Commit。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a simplified PBFT (Practical Byzantine 故障 Tolerance)，包含4 节点 (f=1 Byzantine 故障).

PBFT Three-Phase Protocol:
1. **Pre-prepare**: Primary assigns sequence number, broadcasts (pre-prepare, v, n, d) to all
2. **Prepare**: Each replica broadcasts (prepare, v, n, d, i) to all. Prepare-certificate = 2f matching prepares
3. **Commit**: Each replica broadcasts (commit, v, n, d, i) to all. Commit-certificate = 2f+1 matching commits

```JSON
请求:  {"type": "pbft_request", "msg_id": 1, "operation": "set x=42", "客户端": "c1"}
响应: {"type": "pbft_request_ok", "in_reply_to": 1, "sequence_number": 1, "view": 0, "phase": "pre-prepare"}

请求:  {"type": "pbft_status", "msg_id": 2, "sequence_number": 1}
响应: {"type": "pbft_status_ok", "in_reply_to": 2, "phase": "committed", "prepares_received": 3, "commits_received": 4, "executed": true}
```

## 涉及概念

- `PBFT`
- `pre-prepare`
- `prepare`
- `commit`
- `three-phase protocol`

## 实现提示

- PBFT uses 3 phases: Pre-prepare, Prepare, Commit
- Pre-prepare: primary broadcasts the 请求 to all replicas
- Prepare: each replica broadcasts Prepare to all other replicas. Wait用于2f matching Prepares
- Commit: each replica broadcasts Commit. Wait用于2f+1 matching Commits
- With f=1 Byzantine 故障, need N=4 节点 (3f+1=4)

## 测试用例

### 1. Request starts pre-prepare phase

pbft_request_ok should show sequence_number: 1, view: 0, phase: pre-prepare.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=42","client":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Status shows execution after all phases

pbft_status_ok should show phase: committed or executed if all phases completed.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=1","client":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pbft_status","msg_id":3,"sequence_number":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Practical Byzantine Fault Tolerance - Castro & Liskov](https://pmg.csail.mit.edu/papers/osdi99.pdf)：The original PBFT paper from OSDI 1999

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
