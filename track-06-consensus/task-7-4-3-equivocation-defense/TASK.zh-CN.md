# Detect和Handle Equivocation Attacks

英文标题：Detect和Handle Equivocation Attacks
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-3-equivocation-defense>

课程：6. 共识：Raft 与日志复制
任务序号：18
短标题：Equivocation Defense
难度：advanced
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你完成 `Detect和Handle Equivocation Attacks`。

重点关注：`equivocation`、`contradictory messages`、`evidence collection`、`Byzantine detection`。

建议先按提示逐步实现：Equivocation: a Byzantine 节点 sends different 消息 to different peers。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Simulate a Byzantine 节点 that sends contradictory 消息 to different peers (equivocation). Show that PBFT correctly handles this.

```JSON
请求:  {"type": "simulate_equivocation", "msg_id": 1, "byzantine_node": "n2", "sequence": 1, "messages_sent": {
    "to_n1": {"prepare": {"value": "A"}},
    "to_n3": {"prepare": {"value": "B"}},
    "to_n4": {"prepare": {"value": "A"}}
}}
响应: {"type": "simulate_equivocation_ok", "in_reply_to": 1, "equivocation_detected": true, "evidence": {"节点": "n2", "conflicting_values": ["A", "B"]}, "consensus_safe": true, "chosen_value": "A", "reason": "majority_agreed_on_A"}

请求:  {"type": "equivocation_report", "msg_id": 2}
响应: {"type": "equivocation_report_ok", "in_reply_to": 2, "byzantine_nodes_detected": ["n2"], "total_equivocations": 1}
```

## 涉及概念

- `equivocation`
- `contradictory messages`
- `evidence collection`
- `Byzantine detection`

## 实现提示

- Equivocation: a Byzantine 节点 sends different 消息 to different peers
- Detection: peers compare received 消息和find contradictions
- Evidence: two signed 消息 from the same 节点，包含different values用于the same sequence
- PBFT handles this because 2f+1 matching 消息 are required用于commit
- The contradictory 节点 is effectively ignored when it cannot produce enough matching 消息

## 测试用例

### 1. Equivocation is detected

simulate_equivocation_ok should show equivocation_detected: true和consensus_safe: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_equivocation","msg_id":2,"byzantine_node":"n2","sequence":1,"messages_sent":{"to_n1":{"prepare":{"value":"A"}},"to_n3":{"prepare":{"value":"B"}},"to_n4":{"prepare":{"value":"A"}}}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Equivocation report lists Byzantine nodes

equivocation_report_ok should list n2 in byzantine_nodes_detected.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_equivocation","msg_id":2,"byzantine_node":"n2","sequence":1,"messages_sent":{"to_n1":{"prepare":{"value":"X"}},"to_n3":{"prepare":{"value":"Y"}},"to_n4":{"prepare":{"value":"X"}}}}}
{"src":"c1","dest":"n1","body":{"type":"equivocation_report","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Equivocation和BFT](https://decentralizedthoughts.github.io/2019-12-22-what-is-a-byzantine-agreement-problem/)：How equivocation attacks work和how BFT protocols defend against them

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
