# 证明 Paxos 的安全性：已选定的值不可更改

英文标题：Prove Paxos Safety: Chosen Values Are Immutable
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-3-paxos-safety>

课程：6. 共识
任务序号：13
短标题：Paxos Safety
难度：高级
子主题：Paxos

## 中文导读

本题要求你证明 Paxos 协议的核心安全性质：一旦某个值被选定，之后所有的提案最终也只会选定同一个值。这是共识算法最重要的保证——决定了就不能反悔。你需要通过编写一个模拟程序来验证这个性质，直观地展示为什么 Paxos 能做到"一锤定音"。

## 题目说明

证明在 Paxos 中，一旦某个值被选定，所有后续的提案也将选定同一个值。这就是 Paxos 的核心安全性质。

你需要实现一个模拟程序来验证这一点：

```json
Request:  {"type": "paxos_safety_test", "msg_id": 1, "nodes": 5, "chosen_value": "v1", "chosen_at_n": 3, "new_proposal_n": 7}
Response: {"type": "paxos_safety_test_ok", "in_reply_to": 1, "new_proposal_value": "v1", "forced_by_promise": true, "promise_source": "n2", "safe": true}

Request:  {"type": "paxos_invariant_check", "msg_id": 2, "proposals": [
    {"n": 1, "value": "a", "accepted_by": ["n1", "n2"]},
    {"n": 3, "value": "b", "accepted_by": ["n2", "n3", "n4"]},
    {"n": 5, "value": "b", "accepted_by": ["n3", "n4", "n5"]}
]}
Response: {"type": "paxos_invariant_check_ok", "in_reply_to": 2, "chosen_value": "b", "chosen_at_n": 3, "all_subsequent_match": true, "safe": true}
```

## 概念说明

**为什么已选定的值不会被改变？** 关键在于"多数派必然重叠"。假设值 `v` 在提案编号 `n` 时被多数派接受了，那么任何编号更大的新提案在第一阶段询问多数派时，至少会有一个节点告诉它"我之前已经接受了 `v`"。根据值选择规则，新提案者就必须继续使用 `v`，无法提出不同的值。

这就好比投票选举：如果超过半数的人已经选了某个候选人，那么任何新一轮调查只要也覆盖超过半数的人，就一定会至少问到一个已经投过票的人，从而发现之前的结果。

## 涉及概念

- `safety proof`
- `invariant`
- `chosen value`
- `consensus immutability`

## 实现提示

- 一旦值 `v` 在提案编号 `n` 被选定，之后任何 `Accept(n2, v2)`（其中 `n2 > n`）都必定满足 `v2 = v`
- 证明方法使用对提案编号的数学归纳法
- 核心洞察：任何更高编号的提案在第一阶段都必须向多数派询问，而这个多数派与之前选定值的多数派一定有交集
- 两个多数派必然存在重叠节点，所以新提案的询问中至少有一个接受者已经接受了 `v`
- 根据值选择规则，提案者必须使用承诺回复中 `accepted_n` 最高的值，也就是 `v`

## 测试用例

### 1. 新提案被强制使用已选定的值

验证说明：响应中应显示 `new_proposal_value` 为 `"v1"`、`forced_by_promise` 为 `true`、`safe` 为 `true`，表明新提案被迫采用了之前已选定的值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_safety_test","msg_id":2,"nodes":5,"chosen_value":"v1","chosen_at_n":3,"new_proposal_n":7}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 不变式在多个提案间成立

验证说明：值 `"b"` 在编号 3 首次被多数派选定，之后编号 5 的提案也选定了 `"b"`，说明 `all_subsequent_match` 为 `true`，安全性成立。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_invariant_check","msg_id":2,"proposals":[{"n":1,"value":"a","accepted_by":["n1","n2"]},{"n":3,"value":"b","accepted_by":["n2","n3","n4"]},{"n":5,"value":"b","accepted_by":["n3","n4","n5"]}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos Made Simple - Safety Proof](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)：Lamport 对 Paxos 安全性不变式的证明，解释了为什么所有提案最终会收敛到同一个值

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
