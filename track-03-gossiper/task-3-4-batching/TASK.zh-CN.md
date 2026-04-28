# 添加消息批处理以降低网络开销

英文标题：Add Message Batching to Reduce Network Overhead
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-batching>

课程：3. 传播者：Gossip 信息传播
任务序号：4
短标题：消息批处理
难度：进阶
子主题：朴素广播（洪泛）

## 中文导读

这道题让你实现消息批处理——不再收到一条消息就立刻发送，而是先攒一批，然后一次性发出去。这是分布式系统中非常常见的优化手段，能显著降低网络开销，但代价是增加了一点延迟。理解这个权衡对设计高性能系统至关重要。

## 题目说明

通过将多条消息打包成一次传输来降低网络开销。不再立即发送每条消息，而是先将消息放入缓冲区，然后按照定时或者缓冲区达到阈值时批量发送。

## 概念说明

### 批处理的权衡

批处理（Batching）通过减少每条消息的传输开销来提升吞吐量，但同时也增加了延迟。最优的批处理大小取决于消息速率、网络延迟和一致性要求。

可以类比寄快递：你可以每收到一个包裹就跑一趟快递站，也可以攒够几个包裹再一起去寄。后者省了跑腿次数，但每个包裹都要等一会儿才能寄出。

## 涉及概念

- `batching`
- `throughput optimization`
- `latency tradeoff`

## 实现提示

- 先将消息放入缓冲区，不要立即发送
- 使用基于时间的定时刷新机制
- 在延迟和吞吐量之间寻找平衡点

## 测试用例

### 1. 消息被批量打包处理

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":1}}
{"src":"c2","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":2}}
{"src":"c3","dest":"n1","body":{"type":"broadcast","msg_id":5,"message":3}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":6}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"topology_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"broadcast_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c2","body":{"type":"broadcast_ok","in_reply_to":4,"msg_id":3}}
{"src":"n1","dest":"c3","body":{"type":"broadcast_ok","in_reply_to":5,"msg_id":4}}
{"src":"n1","dest":"c4","body":{"type":"read_ok","in_reply_to":6,"msg_id":5,"messages":[1,2,3]}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
