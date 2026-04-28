# 检测并防御"说谎"攻击

英文标题：Detect and Handle Equivocation Attacks
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-3-equivocation-defense>

课程：6. 共识
任务序号：18
短标题：Equivocation Defense
难度：高级
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你模拟一种典型的拜占庭攻击——"说谎"攻击（Equivocation），即恶意节点向不同的伙伴发送互相矛盾的消息。你需要展示 PBFT 如何正确处理这种情况，确保共识不被破坏。通过这道题，你将深刻理解为什么拜占庭容错协议要求如此多的消息交换，以及这些额外的通信如何帮助诚实节点识别出"叛徒"。

## 题目说明

模拟一个拜占庭节点向不同的伙伴发送互相矛盾的消息（即"说谎"攻击），并展示 PBFT 能正确处理这种情况。

所谓"说谎"攻击，就是一个恶意节点在同一轮协议中，告诉节点 A "我投了值 X"，又告诉节点 B "我投了值 Y"。当诚实节点相互对比消息后，就能发现矛盾，从而识别出恶意节点。

```json
Request:  {"type": "simulate_equivocation", "msg_id": 1, "byzantine_node": "n2", "sequence": 1, "messages_sent": {
    "to_n1": {"prepare": {"value": "A"}},
    "to_n3": {"prepare": {"value": "B"}},
    "to_n4": {"prepare": {"value": "A"}}
}}
Response: {"type": "simulate_equivocation_ok", "in_reply_to": 1, "equivocation_detected": true, "evidence": {"node": "n2", "conflicting_values": ["A", "B"]}, "consensus_safe": true, "chosen_value": "A", "reason": "majority_agreed_on_A"}

Request:  {"type": "equivocation_report", "msg_id": 2}
Response: {"type": "equivocation_report_ok", "in_reply_to": 2, "byzantine_nodes_detected": ["n2"], "total_equivocations": 1}
```

## 概念说明

**"说谎"攻击为什么危险？** 想象一个投票场景：恶意节点同时告诉两拨人不同的投票结果，可能让双方都误以为自己的选择获得了多数支持，导致系统做出互相矛盾的决定。

**PBFT 如何防御？** PBFT 的准备阶段要求每个节点都把自己的消息广播给所有人，这样大家可以"核对笔记"。由于提交需要 `2f+1` 个一致的消息，而恶意节点最多只有 `f` 个，它们无法伪造出足够多的一致消息来欺骗系统。

## 涉及概念

- `equivocation`
- `contradictory messages`
- `evidence collection`
- `Byzantine detection`

## 实现提示

- "说谎"攻击指拜占庭节点向不同伙伴发送不同的消息
- 检测方式：伙伴之间对比收到的消息，发现矛盾
- 证据：同一个节点针对同一个序列号发出了包含不同值的两条签名消息
- PBFT 能应对这种攻击，因为提交需要 `2f+1` 个匹配的消息
- 发送矛盾消息的节点实际上会被忽略，因为它无法产生足够多的一致消息来影响结果

## 测试用例

### 1. 检测到"说谎"行为

验证说明：响应中应显示 `equivocation_detected` 为 `true` 且 `consensus_safe` 为 `true`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_equivocation","msg_id":2,"byzantine_node":"n2","sequence":1,"messages_sent":{"to_n1":{"prepare":{"value":"A"}},"to_n3":{"prepare":{"value":"B"}},"to_n4":{"prepare":{"value":"A"}}}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 报告中列出拜占庭节点

验证说明：报告中应在 `byzantine_nodes_detected` 列表中包含 `"n2"`。

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

- [Equivocation and BFT](https://decentralizedthoughts.github.io/2019-12-22-what-is-a-byzantine-agreement-problem/)：讲解"说谎"攻击的原理以及拜占庭容错协议如何防御

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
