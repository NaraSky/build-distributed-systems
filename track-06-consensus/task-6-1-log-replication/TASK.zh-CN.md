# 实现日志复制

英文标题：Implement Log Replication
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-1-log-replication>

课程：6. 共识：Raft 与日志复制
任务序号：1
短标题：日志复制
难度：高级
子主题：Raft 日志复制

## 中文导读

这道题要求你实现 Raft 协议中最核心的功能之一——日志复制（Log Replication）。领导者（Leader）接收客户端的命令后，需要把这些命令同步到所有跟随者（Follower）上，确保集群中的每个节点都拥有一致的日志。这是构建可靠分布式系统的基础，理解了日志复制，你就理解了 Raft 的一半。

## 题目说明

实现 Raft 协议中从领导者到跟随者的日志复制机制：

1. 领导者接收客户端的命令，将其追加到本地日志中
2. 领导者向所有跟随者发送 AppendEntries 请求
3. AppendEntries 请求中包含：prevLogIndex、prevLogTerm、entries[]
4. 跟随者检查自己在 prevLogIndex 位置的日志是否匹配
5. 如果匹配，则追加新条目；如果不匹配，则拒绝

你需要为每个跟随者维护 nextIndex 和 matchIndex，用来跟踪复制进度。

## 概念说明

### 复制日志

Raft 通过复制一组命令日志来实现共识。每条日志条目都有一个索引（Index）和任期号（Term）。领导者负责追加新条目，并将它们复制到其他节点。当多数节点都拥有某条日志时，该条目就被视为"已提交"，可以安全地应用到状态机上。

你可以把这个过程想象成班长记笔记：班长先把老师说的话记在自己的本子上，然后让其他同学也抄一份。只有当超过一半的同学都抄完了，这条笔记才算"确认通过"。

### 日志匹配属性

如果两个节点的日志在某个位置拥有相同的索引和任期号，那么从开头到该位置的所有日志条目都是完全一致的。这一特性由两个条件保证：（1）领导者在同一索引位置最多只会创建一条日志；（2）AppendEntries 的一致性检查机制。

## 涉及概念

- `log`
- `replication`
- `AppendEntries`

## 实现提示

- 领导者需要维护日志，并为每个跟随者维护 nextIndex
- AppendEntries 消息中携带日志条目
- 跟随者在日志匹配时追加新条目

## 测试用例

### 1. 领导者将条目追加到日志

领导者在索引 1 的位置追加一条日志，任期号正确。回复 raft_append_ok。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"raft_append","msg_id":2,"entry":{"term":1,"command":{"op":"put","key":"x","value":1}}}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"raft_append_ok","in_reply_to":2,"msg_id":1,"index":1}}
```

## 参考资料

- [Raft Paper Section 5.3](https://raft.github.io/raft.pdf)：Raft 论文中关于日志复制的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
