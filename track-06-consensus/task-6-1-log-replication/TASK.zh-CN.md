# 实现 日志 复制

英文标题：Implement Log Replication
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-1-log-replication>

课程：6. 共识：Raft 与日志复制
任务序号：1
短标题：日志 复制
难度：advanced
子主题：Raft 日志 复制

## 中文导读

本题要求你完成 `实现 日志 复制`。

重点关注：`log`、`replication`、`AppendEntries`。

建议先按提示逐步实现：Leader maintains 日志和nextIndex per Follower。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement Raft 日志 复制 from Leader to followers:

1. Leader receives 客户端 commands, appends to local 日志
2. Leader sends AppendEntries to all followers
3. AppendEntries includes: prevLogIndex, prevLogTerm, entries[]
4. Follower checks if 日志 matches at prevLogIndex
5. If match, append entries; if not, reject

Track nextIndex和matchIndex per Follower to manage 复制 progress.

## 概念说明

### The Replicated 日志

Raft replicates a 日志 of commands. Each entry has an 索引和term. The Leader appends entries和replicates them. Once a majority have an entry, it is committed和can be applied.

### 日志 Matching Property

If two logs have an entry，包含the same 索引和term, they are identical up to that 索引. This is guaranteed by: (1) a Leader creates at most one entry per 索引,和(2) AppendEntries consistency check.

## 涉及概念

- `log`
- `replication`
- `AppendEntries`

## 实现提示

- Leader maintains 日志和nextIndex per Follower
- AppendEntries carries 日志 entries
- Followers append if 日志 matches

## 测试用例

### 1. Leader appends entry to 日志

Leader appends entry to 日志 at 索引 1，包含correct term. Replies，包含raft_append_ok.

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

- [Raft Paper Section 5.3](https://raft.github.io/raft.pdf)：日志 复制 in Raft

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
