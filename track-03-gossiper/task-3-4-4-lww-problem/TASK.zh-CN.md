# 演示最后写入者胜出的数据丢失问题与版本向量方案

英文标题：Demonstrate LWW Data Loss with Version Vectors
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-4-lww-problem>

课程：3. 传播者：Gossip 信息传播
任务序号：19
短标题：最后写入者胜出的问题
难度：高级
子主题：Epidemic Algorithms and CRDT Gossip

## 中文导读

这道题让你亲手验证"最后写入者胜出"策略的致命缺陷：当两个客户端同时写入同一个键时，其中一个写入会被悄悄丢弃。然后你需要实现版本向量（Version Vector）作为替代方案，它能检测到并发冲突并同时保留两个值，让应用层来决定如何处理。这是理解分布式系统中冲突检测与解决的核心知识点。

## 题目说明

"最后写入者胜出"策略在两个客户端并发写入时会悄悄丢失数据。你的任务是演示这个问题，并实现一个基于版本向量的替代方案来检测冲突。

需要实现两种模式：`lww`（最后写入者胜出）和 `vv`（版本向量）：

```json
请求:  {"type": "set_mode", "msg_id": 1, "mode": "vv"}
响应: {"type": "set_mode_ok", "in_reply_to": 1}

请求:  {"type": "vv_write", "msg_id": 2, "key": "x", "value": "a", "context": {}}
响应: {"type": "vv_write_ok", "in_reply_to": 2, "vc": {"c1": 1}}

请求:  {"type": "vv_read", "msg_id": 3, "key": "x"}
响应: {"type": "vv_read_ok", "in_reply_to": 3, "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false}
```

当版本向量模式下发生并发写入时，两个值都会被保留：
```json
响应: {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}, {"value": "b", "vc": {"c2": 1}}], "conflict": true}
```

## 涉及概念

- `LWW limitation`
- `data loss`
- `version vectors`
- `conflict detection`

## 实现提示

- "最后写入者胜出"策略会悄悄丢弃并发写入中"输掉"的那个值
- 构造一个场景来验证：客户端 A 写入 x=1，客户端 B 几乎同时写入 x=2
- 时间戳较小的那次写入会被永久丢失
- 版本向量能够检测到这种冲突，而不是悄悄地做出选择
- 检测到冲突时，将两个值都作为"兄弟值"返回

## 测试用例

### 1. 切换到版本向量模式

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"set_mode","msg_id":2,"mode":"vv"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "set_mode_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 单次写入后读取，无冲突

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vv_write","msg_id":2,"key":"x","value":"a","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vv_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_write_ok", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false, "in_reply_to": 3, "msg_id": 2}}
```

## 参考资料

- [Amazon Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：亚马逊 Dynamo 使用版本向量进行冲突检测的经典论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
