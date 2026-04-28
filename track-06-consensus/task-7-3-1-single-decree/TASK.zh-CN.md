# 实现单法令 Paxos 第一阶段（准备/承诺）

英文标题：Implement Single-Decree Paxos Phase 1 (Prepare/Promise)
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-1-single-decree>

课程：6. 共识
任务序号：11
短标题：Paxos Phase 1
难度：高级
子主题：Paxos

## 中文导读

本题要求你实现单法令 Paxos（Single-Decree Paxos）协议的第一阶段，也就是"准备/承诺"流程。Paxos 是分布式系统中最经典的共识算法，理解它的第一阶段是掌握整个协议的基础。通过这道题，你将学会提案者（Proposer）如何发起提案，以及接受者（Acceptor）如何根据提案编号做出承诺。

## 题目说明

实现单法令 Paxos 的第一阶段，目标是让多个节点就一个值达成一致。

第一阶段的工作流程如下：
1. 提案者选择一个唯一的提案编号 `n`
2. 提案者向所有接受者发送 `Prepare(n)` 消息
3. 每个接受者收到请求后：如果 `n` 大于自己已经承诺过的最高编号（`highest_promised`），就把 `highest_promised` 更新为 `n`，然后回复 `Promise(n, accepted_value, accepted_n)`，表示"我承诺不再接受编号比 `n` 小的提案"
4. 如果 `n` 小于或等于 `highest_promised`，接受者拒绝这个请求

```json
Request:  {"type": "paxos_prepare", "msg_id": 1, "proposal_n": 1}
Response: {"type": "paxos_promise", "in_reply_to": 1, "promised": true, "accepted_n": null, "accepted_value": null}

Request:  {"type": "paxos_prepare", "msg_id": 2, "proposal_n": 5}
Response: {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null}

Request:  {"type": "paxos_prepare", "msg_id": 3, "proposal_n": 3}
Response: {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "reason": "already_promised_higher", "highest_promised": 5}
```

## 概念说明

**提案编号的作用**：可以把提案编号想象成"排队号码"。接受者只会理睬拿着更大号码的人，如果你的号码比上一个人小，就会被拒绝。这个机制保证了系统总是朝着最新的提案推进，避免了旧提案干扰新提案。

**承诺的含义**：接受者发出承诺后，就相当于跟提案者做了一个约定——"我不会再接受比你编号更小的提案了"。这是 Paxos 保证安全性的关键。

## 涉及概念

- `Paxos`
- `single-decree`
- `Prepare`
- `Promise`
- `proposal number`

## 实现提示

- 提案者选择一个唯一的提案编号 `n`，然后向所有接受者发送 `Prepare(n)` 消息
- 如果 `n` 大于接受者已见过的最大编号，接受者就回复承诺，并附上自己之前已接受的值（如果有的话）
- 如果接受者已经承诺过一个更大的编号，就拒绝这次准备请求
- 提案编号必须全局唯一，可以使用"节点编号 + 递增序列号"的方式来生成
- 提案者需要收到多数派的承诺后，才能进入第二阶段

## 测试用例

### 1. 首次准备请求总是被承诺

验证说明：当接受者没有收到过任何提案时，它会承诺第一个收到的准备请求。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
```

### 2. 较高的提案编号会取代较低的

验证说明：先用编号 5 做准备并成功，再用编号 3 做准备时会被拒绝，因为接受者已经承诺了更大的编号 5。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":3,"proposal_n":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "highest_promised": 5, "msg_id": 2}}
```

## 参考资料

- [Paxos Made Simple - Lamport](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)：Lamport 对 Paxos 算法的简化讲解，是理解 Paxos 最推荐的入门论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
