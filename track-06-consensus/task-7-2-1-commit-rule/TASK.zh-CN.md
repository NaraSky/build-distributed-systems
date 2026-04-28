# 实现 Raft 提交规则

网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-1-commit-rule>

课程：6. 共识：Raft 与日志复制
任务序号：6
短标题：提交规则
难度：进阶
子主题：提交与应用

## 中文导读

这道题要求你实现 Raft 协议中的提交规则。核心逻辑非常简单：一条日志被集群中多数节点复制之后，就算"已提交"。领导者（Leader）通过维护每个跟随者的匹配索引（matchIndex）来判断一条日志是否已经被多数派复制，从而决定是否推进提交索引（commitIndex）。

## 题目说明

在 Raft 协议中，提交规则（Commitment Rule）决定了一条日志条目何时可以被安全地视为"已提交"。规则本身很直观：当集群中超过半数的节点（Node）都在自己的日志中保存了这条记录，它就不可能再丢失了，此时可以安全地提交。

领导者为每个跟随者（Follower）维护一个匹配索引，记录该跟随者已经成功复制到哪个位置。领导者通过统计所有匹配索引的值，来判断哪些日志条目已经达到了多数派的要求。

需要注意的是，只有来自当前任期（Term）的日志条目才能直接推进提交索引。之前任期的日志条目只能在当前任期的日志被提交时"顺带"提交，这是 Raft 保证安全性的一个重要细节。

```json
Request:  {"type": "check_commit", "msg_id": 1, "log_length": 5, "match_indices": {"n1": 5, "n2": 5, "n3": 3, "n4": 2, "n5": 1}, "current_term": 3}
Response: {"type": "check_commit_ok", "in_reply_to": 1, "new_commit_index": 5, "majority_count": 2, "quorum": 3, "committed": true}

Request:  {"type": "advance_commit", "msg_id": 2, "old_commit_index": 3, "match_indices": {"n1": 7, "n2": 5, "n3": 5, "n4": 3, "n5": 2}, "current_term": 3}
Response: {"type": "advance_commit_ok", "in_reply_to": 2, "new_commit_index": 5, "entries_committed": 2}
```

## 涉及概念

- commitment
- majority replication
- commitIndex
- log replication

## 实现提示

- 一条日志被多数节点保存后即为已提交
- 领导者为每个跟随者维护一个匹配索引
- 当多数节点的匹配索引大于等于某个位置时，提交索引可以推进到该位置
- 只有当前任期的日志条目才能直接推进提交索引
- 之前任期的日志条目会被间接提交

## 测试用例

### 1. 多数节点复制后提交日志条目

验证：响应中的新提交索引应为 3，因为三个节点中有两个（n1 和 n2）的匹配索引已达到 3，构成了多数派。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":3,"match_indices":{"n1":3,"n2":3,"n3":1},"current_term":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 未达多数时不推进提交

验证：五个节点中只有两个的匹配索引达到了 5，而多数派需要至少三个节点，因此提交不成立。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":5,"match_indices":{"n1":5,"n2":5,"n3":1,"n4":1,"n5":1},"current_term":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft Consensus - Log Commitment](https://raft.github.io/raft.pdf)：Raft 论文第 5.3 至 5.4 节，详细介绍了提交规则

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
