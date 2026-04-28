# 实现 Multi-Paxos 无限日志

网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-4-multi-paxos>

课程：6. 共识
任务序号：14
短标题：Multi-Paxos
难度：高级
子主题：Paxos

## 中文导读

这道题要求你将单次决策的 Paxos 扩展为 Multi-Paxos，构建一个无限日志系统。每个日志槽位独立运行一个 Paxos 实例来决定该位置写入什么值。关键优化在于：一旦领导者身份稳定下来，后续槽位可以跳过第一阶段直接进入第二阶段，从而大幅减少通信开销。这正是实际生产系统中广泛采用的做法。

## 题目说明

单次决策的 Paxos（Single-decree Paxos）每次只能对一个值达成共识，但实际系统需要持续不断地做决策——比如数据库要不断写入新的记录。Multi-Paxos 的做法是维护一个无限长的日志，为每个日志槽位（Slot）分别运行一个独立的 Paxos 实例，从而形成一个有序的操作序列。

Multi-Paxos 最核心的优化是"跳过第一阶段"。可以把 Paxos 的第一阶段想象成"竞选领导者"的过程：当领导者的地位已经稳固后，就不需要每次提交新值都重新竞选了，直接用领导者的身份发起第二阶段即可。这让正常情况下的延迟从两轮网络往返降低到一轮，性能提升非常显著。如果领导者发生了变更，下一个槽位才需要重新走第一阶段。

从本质上讲，Raft 的工作方式和 Multi-Paxos 非常相似，只是使用了不同的术语和稍有不同的流程组织。

```json
Request:  {"type": "multi_paxos_propose", "msg_id": 1, "slot": 1, "value": "set x=1"}
Response: {"type": "multi_paxos_propose_ok", "in_reply_to": 1, "slot": 1, "phase1_skipped": false, "chosen": true, "value": "set x=1"}

Request:  {"type": "multi_paxos_propose", "msg_id": 2, "slot": 2, "value": "set y=2"}
Response: {"type": "multi_paxos_propose_ok", "in_reply_to": 2, "slot": 2, "phase1_skipped": true, "chosen": true, "value": "set y=2"}

Request:  {"type": "multi_paxos_log", "msg_id": 3}
Response: {"type": "multi_paxos_log_ok", "in_reply_to": 3, "log": [
    {"slot": 1, "value": "set x=1", "status": "chosen"},
    {"slot": 2, "value": "set y=2", "status": "chosen"}
]}
```

## 涉及概念

- Multi-Paxos
- infinite log
- Phase 1 skip
- stable leader

## 实现提示

- 为每个日志槽位运行一个独立的 Paxos 实例
- 优化：当领导者稳定后，后续槽位可以跳过第一阶段
- 领导者只需要执行第二阶段（接受/已接受）就能提交新的日志条目
- 如果领导者发生变更，下一个槽位必须重新执行第一阶段
- Raft 的工作原理与 Multi-Paxos 本质相同，只是术语不同

## 测试用例

### 1. 第一个槽位需要执行第一阶段

验证：第一个提案的响应中 `phase1_skipped` 应为 `false`，因为此时还没有确立领导者，必须先走第一阶段竞选。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 后续槽位跳过第一阶段

验证：第二个提案的 `phase1_skipped` 应为 `true`，因为领导者已经稳定，不需要重新竞选。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":3,"slot":2,"value":"cmd2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos Made Live - Google](https://research.google/pubs/pub33002/)：介绍谷歌如何在生产环境中实现 Multi-Paxos（Chubby 锁服务）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
