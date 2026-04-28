# 实现 Paxos 第二阶段（接受阶段）

网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-2-accept-phase>

课程：6. 共识
任务序号：12
短标题：Paxos Phase 2
难度：高级
子主题：Paxos

## 中文导读

这道题要求你实现 Paxos 协议的第二阶段，也就是"接受"阶段。在第一阶段中，提议者（Proposer）已经获得了多数派的承诺；现在进入第二阶段，提议者要向接受者（Acceptor）发送一个具体的值，请求大家正式接受。当多数派都接受了同一个值，共识就达成了。这是 Paxos 从"协商"走向"定论"的关键一步。

## 题目说明

在 Paxos 的第一阶段中，提议者通过准备请求获得了多数派接受者的承诺。进入第二阶段后，提议者向接受者发送接受请求 `Accept(n, v)`，携带提案编号 `n` 和要提议的值 `v`。

值的选择规则是 Paxos 安全性的核心所在。如果在第一阶段收到的承诺回复中，有接受者报告自己此前已经接受过某个值，那么提议者必须选用其中提案编号最大的那个已接受值。只有当所有承诺回复都没有携带已接受值时，提议者才能自由选择要提议的值。

可以这样理解这条规则：如果之前已经有值被"半路接受"了，新的提议者不能随意覆盖它，而是必须尊重先前的结果、继续推进那个值。这保证了即使有多个提议者同时竞争，也不会出现相互矛盾的结论。

接受者收到接受请求后，会检查提案编号是否大于等于自己已承诺的最高编号。如果是，就接受该提案；否则拒绝。当一个值被多数派接受后，它就被"选定"了，此后任何新提案都无法改变这个结果。

```json
Request:  {"type": "paxos_accept", "msg_id": 1, "proposal_n": 5, "value": "consensus_value"}
Response: {"type": "paxos_accepted", "in_reply_to": 1, "accepted": true, "proposal_n": 5, "value": "consensus_value"}

Request:  {"type": "paxos_accept", "msg_id": 2, "proposal_n": 3, "value": "late_value"}
Response: {"type": "paxos_accepted", "in_reply_to": 2, "accepted": false, "reason": "promised_higher", "highest_promised": 5}

Request:  {"type": "paxos_chosen", "msg_id": 3}
Response: {"type": "paxos_chosen_ok", "in_reply_to": 3, "value": "consensus_value", "chosen_at_n": 5}
```

## 涉及概念

- Paxos
- Accept
- Accepted
- value selection
- consensus

## 实现提示

- 提议者在第二阶段向接受者发送 `Accept(n, v)` 请求
- 值 `v` 的确定方式：取第一阶段承诺回复中提案编号最大的那个已接受值；如果没有任何已接受值，则由提议者自由选择
- 接受者只在提案编号大于等于自己已承诺的最高编号时，才接受该提案
- 当多数派都接受了同一个提案，共识就达成了，值被正式选定
- 一旦值被选定，后续的任何提案都无法改变它

## 测试用例

### 1. 承诺之后接受成功

验证：先用编号 5 完成准备阶段，再用同一编号发送接受请求，应当成功接受。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":5,"value":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": true, "proposal_n": 5, "value": "hello", "msg_id": 2}}
```

### 2. 较低编号的接受请求被拒绝

验证：节点已经承诺了编号 5，之后收到编号 3 的接受请求会被拒绝，因为承诺过的编号更高。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":3,"value":"old"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": false, "highest_promised": 5, "msg_id": 2}}
```

## 参考资料

- [Understanding Paxos](https://www.cs.rutgers.edu/~pxk/417/notes/paxos.html)：对 Paxos 协议各阶段的逐步讲解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
