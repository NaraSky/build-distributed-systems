# Understand Byzantine Faults，包含Real-World Examples

英文标题：Understand Byzantine Faults，包含Real-World Examples
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-1-byzantine-faults>

课程：6. 共识：Raft 与日志复制
任务序号：16
短标题：Byzantine Faults
难度：intermediate
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你完成 `Understand Byzantine Faults，包含Real-World Examples`。

重点关注：`Byzantine fault`、`crash fault`、`malicious node`、`bit flip`、`CFT vs BFT`。

建议先按提示逐步实现：A Byzantine 节点 can exhibit arbitrary behavior: lying, sending different 消息 to different 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

What is a Byzantine 故障? Unlike crash faults (节点 simply stops), Byzantine faults allow arbitrary misbehavior. A faulty 节点 can lie, send contradictory 消息, or selectively communicate.

Give 3 real-world examples和show why CFT algorithms fail:

```JSON
请求:  {"type": "classify_fault", "msg_id": 1, "scenario": "node_sends_different_values_to_different_peers"}
响应: {"type": "classify_fault_ok", "in_reply_to": 1, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "example": "equivocation attack"}

请求:  {"type": "byzantine_examples", "msg_id": 2}
响应: {"type": "byzantine_examples_ok", "in_reply_to": 2, "examples": [
    {"name": "hardware_bit_flip", "description": "Memory corruption changes stored value silently", "fault_type": "byzantine"},
    {"name": "compromised_node", "description": "Attacker controls 节点, sends malicious 消息", "fault_type": "byzantine"},
    {"name": "software_bug", "description": "Bug causes 节点 to return wrong computation result", "fault_type": "byzantine"}
]}

请求:  {"type": "cft_failure_demo", "msg_id": 3, "algorithm": "raft", "byzantine_node": "n2", "behavior": "equivocation"}
响应: {"type": "cft_failure_demo_ok", "in_reply_to": 3, "consensus_reached": true, "value_correct": false, "reason": "raft_trusted_byzantine_node_response"}
```

## 涉及概念

- `Byzantine fault`
- `crash fault`
- `malicious node`
- `bit flip`
- `CFT vs BFT`

## 实现提示

- A Byzantine 节点 can exhibit arbitrary behavior: lying, sending different 消息 to different 节点
- Crash faults are a subset of Byzantine faults (crash = silence, not lies)
- Real-world examples: hardware bit-flips, hacked 节点, software bugs returning wrong data
- CFT algorithms (Raft, Paxos) cannot handle Byzantine faults
- BFT requires N >= 3f+1 节点 to tolerate f Byzantine faults

## 测试用例

### 1. Classify equivocation as Byzantine

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"classify_fault","msg_id":2,"scenario":"node_sends_different_values_to_different_peers"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "classify_fault_ok", "in_reply_to": 2, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "msg_id": 1}}
```

### 2. List Byzantine fault examples

byzantine_examples_ok should contain at least 3 examples, all，包含fault_type: byzantine.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"byzantine_examples","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [The Byzantine Generals Problem - Lamport](https://lamport.azurewebsites.net/pubs/byz.pdf)：Original paper defining the Byzantine 故障 model

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
