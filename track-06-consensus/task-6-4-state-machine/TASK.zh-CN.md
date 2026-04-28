# 将已提交的日志应用到状态机

英文标题：Apply Committed Entries to State Machine
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-4-state-machine>

课程：6. 共识：Raft 与日志复制
任务序号：4
短标题：状态机
难度：进阶
子主题：Raft 日志复制

## 中文导读

这道题要求你实现将已提交的日志条目应用到状态机（State Machine）的逻辑。日志复制和提交只是保证了各节点拥有一致的日志，而真正让系统"干活"的是状态机——它按顺序执行日志中的命令，产生实际的业务结果。理解这一步，你就能看到 Raft 如何从共识走向实际应用。

## 题目说明

将已提交的日志条目应用到状态机：

1. 维护 lastApplied——已应用到状态机的最高日志索引
2. 当 commitIndex 大于 lastApplied 时，按顺序应用日志条目
3. 状态机执行每条命令
4. 每次应用完一条日志后，递增 lastApplied

状态机必须是确定性的——相同的命令序列必须产生相同的状态。

## 概念说明

### 状态机复制

Raft 负责复制日志，状态机负责解读日志。每个节点按照相同的顺序执行相同的命令，因此所有节点最终都会收敛到相同的状态。这就是复制式服务的基础。

打个比方：所有节点就像是同一堂课的学生，大家按照相同的顺序做相同的练习题，最终得到的答案一定是一样的。

### 应用顺序

日志条目必须严格按照索引顺序应用。不允许跳过——如果第 5 条日志已提交但第 4 条还没有，必须等待。实际上，提交本身就是按顺序进行的，所以这通常不会成为问题。

## 涉及概念

- `state machine`
- `apply`
- `determinism`

## 实现提示

- 按顺序应用日志条目
- 维护 lastApplied 索引
- 状态机必须是确定性的

## 测试用例

### 1. 按顺序应用日志条目

状态机按顺序应用两条日志。最终状态为 {x:1, y:2}，lastApplied 等于 2。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_committed_log","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":1}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":2}}],"commit_index":2}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_committed_log_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":3,"msg_id":2,"state":{"x":1,"y":2},"last_applied":2}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
