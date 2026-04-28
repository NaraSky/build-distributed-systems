# 处理请求投票 RPC

网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-4-request-vote>

课程：5. 选举器：领导者选举
任务序号：4
短标题：请求投票
难度：高级
子主题：Raft 领导者选举

## 中文导读

这道题让你实现 Raft 的请求投票 RPC。候选人向其他节点请求投票，节点根据任期号和投票状态来决定是否投票。每个任期内每个节点最多只能投一票，这保证了每个任期最多只有一个领导者，是 Raft 安全性的核心保障。

## 题目说明

实现请求投票（RequestVote）RPC。候选人向其他节点请求投票。节点在满足以下条件时授予投票：候选人的任期号（Term）不低于自己的任期号，且自己在当前任期内还没有投过票。

## 概念说明

### 投票授予规则

一个节点在以下条件下授予投票：候选人的任期号至少和自己的一样新，并且自己在这个任期内还没有给其他候选人投过票。这确保了每个任期内最多只有一个领导者。就像选举中每人只有一票，投了就不能再改，保证了不会同时选出两个领导者。

## 涉及概念

- `voting`
- `term comparison`
- `vote granting`

## 实现提示

- 当候选人的任期号大于等于自己的任期号时，才考虑投票
- 每个任期内只能投一次票
- 如果候选人的任期号更高，先更新自己的任期号

## 测试用例

### 1. 为相同任期的候选人投票

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n2","dest":"n1","body":{"type":"request_vote","msg_id":3,"term":2,"candidate_id":"n2","last_log_index":0,"last_log_term":0}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"n2","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":2,"vote_granted":true}}
```

## 参考资料

- [Raft Lecture](https://www.youtube.com/watch?v=YbZ3zDzDnrw)：MIT 6.824 课程中 Robert Morris 讲授的 Raft 讲座

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
