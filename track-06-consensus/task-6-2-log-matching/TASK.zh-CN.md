# Ensure 日志 Matching Property

英文标题：Ensure Log Matching Property
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-2-log-matching>

课程：6. 共识：Raft 与日志复制
任务序号：2
短标题：日志 Matching
难度：advanced
子主题：Raft 日志 复制

## 中文导读

本题要求你完成 `Ensure 日志 Matching Property`。

重点关注：`log matching`、`consistency check`、`conflict resolution`。

建议先按提示逐步实现：Check prevLogIndex和prevLogTerm match。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the 日志 Matching safety property:

On the Follower side:
1. Receive AppendEntries，包含prevLogIndex, prevLogTerm
2. If entry at prevLogIndex has different term, reject
3. If entries conflict，包含existing, delete from conflict point
4. Append new entries
5. Update commitIndex if Leader's is higher

This ensures all committed entries are identical across 节点.

## 概念说明

### 日志 Matching Invariant

If two 节点 have entries，包含the same 索引和term, their logs are identical up to that point. This is achieved by rejecting AppendEntries when prev doesn't match, then backtracking until match is found.

### Conflict Resolution

When logs diverge (after Leader changes), the new Leader's 日志 wins. Followers truncate conflicting entries和accept the Leader's. Committed entries are never truncated - that's the Election Restriction safety.

## 涉及概念

- `log matching`
- `consistency check`
- `conflict resolution`

## 实现提示

- Check prevLogIndex和prevLogTerm match
- If conflict, truncate和replace
- Never overwrite committed entries

## 测试用例

### 1. Accept matching entries

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
