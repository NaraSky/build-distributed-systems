# 实现日志条目提交

英文标题：Implement Entry Commitment
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-3-commitment>

课程：6. 共识：Raft 与日志复制
任务序号：3
短标题：日志提交
难度：高级
子主题：Raft 日志复制

## 中文导读

这道题要求你实现 Raft 的日志提交（Commitment）机制。领导者需要判断一条日志是否已经被集群中的多数节点复制，如果是，就可以安全地将其标记为"已提交"。提交是 Raft 保证数据持久性和一致性的核心环节——只有已提交的日志才不会丢失。

## 题目说明

实现日志条目的提交逻辑：

1. 领导者为每个跟随者维护 matchIndex
2. 对于每个索引 N，统计有多少个节点的 matchIndex 大于等于 N
3. 如果多数节点拥有索引为 N 的条目，且该条目来自当前任期，则提交 N
4. 将 commitIndex 推进到最大的已提交索引 N
5. 在下一次心跳中，将新的 commitIndex 通知所有跟随者

重要提示：只能直接提交来自当前任期的日志条目，以满足 Raft 的安全性要求。

## 概念说明

### 提交

当领导者确认多数节点已经拥有某条日志时，该日志就算"已提交"。已提交的日志具有持久性——即使领导者更换，这些日志也不会丢失。领导者在多数节点确认后推进 commitIndex。

打个比方：投票表决时，只有超过半数的人同意，决议才算通过。同样，只有超过半数的节点都复制了某条日志，这条日志才算"提交成功"。

### 当前任期要求

领导者只能直接提交自己任期内的日志条目。前任领导者遗留的日志条目，只有在当前任期的某条日志被提交之后，才会被间接提交。这个规则看似奇怪，但它能防止一种微妙的安全性问题。

## 涉及概念

- `commitment`
- `majority`
- `quorum`

## 实现提示

- 当多数节点拥有某条日志时，该条目即为已提交
- 使用 matchIndex 来统计副本数量
- 只能直接提交来自当前任期的日志条目

## 测试用例

### 1. 多数节点复制后提交日志

多节点测试：领导者追加一条日志，等待多数节点确认（3 个节点中的 2 个），然后推进 commitIndex。验证来自当前任期的日志条目被正确提交。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Raft Commitment](https://www.youtube.com/watch?v=YbZ3zDzDnrw)：MIT 6.824 课程中关于 Raft 的讲座

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
