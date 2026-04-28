# 实现混合逻辑时钟的接收规则

英文标题：Implement HLC Receive Rule
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-2-hlc-receive>

课程：2. 标识符：分布式唯一 ID
任务序号：17
短标题：混合逻辑时钟接收
难度：高级
子主题：Hybrid Logical Clocks (HLC)

## 中文导读

当一个节点收到来自其他节点的消息时，需要将消息中携带的时钟与本地时钟进行合并。混合逻辑时钟的接收规则比 Lamport 时钟复杂一些，需要同时考虑物理时间和逻辑计数器。本题要求你实现这一接收合并逻辑，这是保证分布式系统中因果一致性的关键步骤。

## 题目说明

混合逻辑时钟的接收规则比 Lamport 时钟更加复杂。当收到一条携带混合逻辑时钟 `(msg.pt, msg.lc)` 的消息时，更新步骤如下：

1. `new_pt = max(local.pt, msg.pt, now_ms())`——取本地物理时间、消息物理时间和当前系统时间三者中的最大值
2. 如果 `new_pt == local.pt == msg.pt`：三方物理时间相同，取两个逻辑计数器的最大值再加 1，即 `new_lc = max(local.lc, msg.lc) + 1`
3. 否则如果 `new_pt == local.pt`：本地物理时间最大，沿用本地逻辑计数器加 1，即 `new_lc = local.lc + 1`
4. 否则如果 `new_pt == msg.pt`：消息物理时间最大，沿用消息逻辑计数器加 1，即 `new_lc = msg.lc + 1`
5. 否则（当前系统时间是最新的）：物理时间已经前进，逻辑计数器归零，即 `new_lc = 0`

实现 `hlc_receive` 处理器：
```json
请求:  {"type": "hlc_receive", "msg_id": 1, "remote_pt": 1000, "remote_lc": 5}
响应: {"type": "hlc_receive_ok", "in_reply_to": 1, "pt": 1000, "lc": 6}
```

## 涉及概念

- `HLC merge`
- `receive rule`
- `clock synchronization`
- `causal consistency`

## 实现提示

- 接收消息时：取本地物理时间、收到的物理时间和当前系统时间三者的最大值
- 如果最大物理时间等于本地和收到的物理时间，则从两个逻辑计数器的最大值开始递增
- 如果最大物理时间只等于其中一方，则从那一方的逻辑计数器开始递增
- 如果最大物理时间是当前系统时间（说明物理时间向前推进了），则将逻辑计数器重置为 0
- 混合逻辑时钟必须始终向前推进，永远不能倒退

## 测试用例

### 1. 收到来自超前远端的消息，推进本地时钟

远端的物理时间在遥远的未来。此时 new_pt 等于 remote_pt，new_lc 等于 remote_lc + 1 = 6。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":2,"remote_pt":9999999999999,"remote_lc":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "hlc_receive_ok", "pt": 9999999999999, "lc": 6, "in_reply_to": 2, "msg_id": 1}}
```

### 2. 收到来自落后远端的消息，沿用本地时钟

执行一次 tick 后，本地物理时间为当前时间。远端 pt=0 落后于本地。此时 new_pt 取 max(local, 0, now)，逻辑计数器的值取决于当前系统时间是否有所推进。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":3,"remote_pt":0,"remote_lc":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CockroachDB and HLC](https://www.cockroachlabs.com/blog/living-without-atomic-clocks/)：CockroachDB 如何使用混合逻辑时钟来实现事务排序

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
