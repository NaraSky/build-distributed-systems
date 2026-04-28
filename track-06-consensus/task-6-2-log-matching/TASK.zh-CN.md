# 确保日志匹配属性

英文标题：Ensure Log Matching Property
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-2-log-matching>

课程：6. 共识：Raft 与日志复制
任务序号：2
短标题：日志匹配
难度：高级
子主题：Raft 日志复制

## 中文导读

这道题要求你在跟随者（Follower）端实现日志匹配的安全性检查。当跟随者收到领导者发来的 AppendEntries 请求时，必须先验证日志是否一致，再决定是否接受新条目。这个机制是 Raft 保证所有节点日志最终一致的关键所在。

## 题目说明

实现日志匹配（Log Matching）安全属性：

在跟随者端：
1. 接收 AppendEntries 请求，其中包含 prevLogIndex 和 prevLogTerm
2. 如果跟随者在 prevLogIndex 位置的日志条目的任期号不同，则拒绝该请求
3. 如果新条目与已有条目冲突，则从冲突点开始删除旧条目
4. 追加新的日志条目
5. 如果领导者的 commitIndex 更高，则更新本地的 commitIndex

这一机制确保所有已提交的日志条目在各节点上完全一致。

## 概念说明

### 日志匹配不变式

如果两个节点在同一索引位置拥有相同任期号的日志条目，那么它们从头到该位置的所有日志都是完全一致的。实现方式是：当 AppendEntries 中的前一条日志不匹配时，跟随者会拒绝请求，领导者则不断回退，直到找到匹配的位置。

### 冲突解决

当日志出现分歧时（比如领导者更换后），新领导者的日志具有最高优先级。跟随者会截断冲突的日志条目，接受领导者的版本。已提交的条目永远不会被截断——这正是选举限制（Election Restriction）安全性所保障的。

## 涉及概念

- `log matching`
- `consistency check`
- `conflict resolution`

## 实现提示

- 检查 prevLogIndex 和 prevLogTerm 是否匹配
- 如果发生冲突，截断并替换旧条目
- 永远不要覆盖已提交的日志条目

## 测试用例

### 1. 接受匹配的日志条目

输入：

```json
{"src":"c0","dest":"n2","body":{"type":"init","msg_id":1,"node_id":"n2","node_ids":["n1","n2","n3"]}}
{"src":"n1","dest":"n2","body":{"type":"append_entries","msg_id":2,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[{"term":1,"index":1,"command":{"op":"put","key":"x","value":1}}],"leader_commit":0}}
```

期望输出：

```text
{"src":"n2","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n2","dest":"n1","body":{"type":"append_entries_ok","in_reply_to":2,"msg_id":1,"success":true,"match_index":1}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
