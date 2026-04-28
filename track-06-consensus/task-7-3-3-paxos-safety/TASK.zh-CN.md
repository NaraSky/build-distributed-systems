# Prove Paxos Safety: Chosen Values Are Immutable

英文标题：Prove Paxos Safety: Chosen Values Are Immutable
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-3-paxos-safety>

课程：6. 共识：Raft 与日志复制
任务序号：13
短标题：Paxos Safety
难度：advanced
子主题：Paxos

## 中文导读

本题要求你完成 `Prove Paxos Safety: Chosen Values Are Immutable`。

重点关注：`safety proof`、`invariant`、`chosen value`、`consensus immutability`。

建议先按提示逐步实现：Once a value v is chosen at proposal n, any future Accept(n2, v2) where n2 > n must have v2 = v。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Prove that once a value is chosen in Paxos, all future proposals will also choose the same value. This is the core safety property.

Implement a simulation that demonstrates this:

```JSON
请求:  {"type": "paxos_safety_test", "msg_id": 1, "节点": 5, "chosen_value": "v1", "chosen_at_n": 3, "new_proposal_n": 7}
响应: {"type": "paxos_safety_test_ok", "in_reply_to": 1, "new_proposal_value": "v1", "forced_by_promise": true, "promise_source": "n2", "safe": true}

请求:  {"type": "paxos_invariant_check", "msg_id": 2, "proposals": [
    {"n": 1, "value": "a", "accepted_by": ["n1", "n2"]},
    {"n": 3, "value": "b", "accepted_by": ["n2", "n3", "n4"]},
    {"n": 5, "value": "b", "accepted_by": ["n3", "n4", "n5"]}
]}
响应: {"type": "paxos_invariant_check_ok", "in_reply_to": 2, "chosen_value": "b", "chosen_at_n": 3, "all_subsequent_match": true, "safe": true}
```

## 涉及概念

- `safety proof`
- `invariant`
- `chosen value`
- `consensus immutability`

## 实现提示

- Once a value v is chosen at proposal n, any future Accept(n2, v2) where n2 > n must have v2 = v
- The proof uses induction on proposal numbers
- Key insight: any higher proposal must hear about v in Phase 1 from a majority
- Two majorities always overlap, so at least one acceptor in the new quorum accepted v
- The proposer is forced to use v (the highest accepted value from promises)

## 测试用例

### 1. New proposal forced to use chosen value

paxos_safety_test_ok should show new_proposal_value: "v1", forced_by_promise: true, safe: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_safety_test","msg_id":2,"nodes":5,"chosen_value":"v1","chosen_at_n":3,"new_proposal_n":7}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Invariant holds across multiple proposals

chosen_value: "b" at n:3 (first majority). all_subsequent_match: true since n:5 also chose "b".

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

- [Paxos Made Simple - Safety Proof](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)：Lamport proof that Paxos safety invariant holds across all proposals

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
