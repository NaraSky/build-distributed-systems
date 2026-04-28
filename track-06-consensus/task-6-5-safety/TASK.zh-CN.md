# 实现选举限制以保证安全性

英文标题：Implement Election Restriction for Safety
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-5-safety>

课程：6. 共识：Raft 与日志复制
任务序号：5
短标题：安全性
难度：高级
子主题：Raft 日志复制

## 中文导读

这道题要求你实现 Raft 的选举限制（Election Restriction）机制。在选举过程中，投票者需要判断候选人的日志是否足够"新"，只有日志足够新的候选人才能赢得选举。这个限制是 Raft 安全性的核心保障——它确保新当选的领导者一定拥有所有已提交的日志条目，从而不会丢失数据。

## 题目说明

实现选举限制以保证安全性：

候选人（Candidate）必须拥有"足够新"的日志才能赢得选举：
1. 投票者将自己的日志与候选人的日志进行比较
2. 如果候选人的 lastLogTerm 大于投票者的 lastLogTerm，说明候选人的日志更新
3. 如果任期号相同，则比较 lastLogIndex
4. 只有当候选人的日志至少和投票者一样新时，才投赞成票

这一规则确保当选的领导者一定拥有所有已提交的日志条目。

## 概念说明

### 选举限制

这是 Raft 最关键的安全性属性。通过只选举日志足够新的候选人，我们确保已提交的日志条目永远不会丢失。领导者完整性（Leader Completeness）属性正是由此而来。

打个比方：选班长时，只有笔记记得最全的同学才有资格当选。这样一来，新班长的笔记一定包含了之前所有"确认通过"的内容。

### 比较逻辑

任期号大的一方胜出。如果任期号相同，日志更长的一方胜出。这精确地定义了"更新"的含义。按照这个规则选出的领导者，一定包含在其当选之前所有已提交的日志。

## 涉及概念

- `election restriction`
- `safety`
- `up-to-date`

## 实现提示

- 投票者需要检查候选人的日志是否足够新
- 先比较最后一条日志的任期号，再比较索引
- 如果候选人的日志落后于投票者，则拒绝投票

## 测试用例

### 1. 对更高任期的候选人投赞成票

输入：

```json
{"src":"c0","dest":"n2","body":{"type":"init","msg_id":1,"node_id":"n2","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n2","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n1","dest":"n2","body":{"type":"request_vote","msg_id":3,"term":3,"candidate_id":"n1","last_log_index":0,"last_log_term":0}}
```

期望输出：

```text
{"src":"n2","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n2","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n2","dest":"n1","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":3,"vote_granted":true}}
```

## 参考资料

- [Raft Safety](https://raft.github.io/raft.pdf)：Raft 论文中关于安全性的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
