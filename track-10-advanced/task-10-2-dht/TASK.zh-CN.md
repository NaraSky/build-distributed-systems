# 构建 Distributed Hash Table (Chord)

英文标题：Build Distributed Hash Table (Chord)
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-2-dht>

课程：10. 高级主题
任务序号：2
短标题：DHT
难度：advanced
子主题：高级 Paradigms

## 中文导读

本题要求你完成 `构建 Distributed Hash Table (Chord)`。

重点关注：`DHT`、`Chord`、`finger table`。

建议先按提示逐步实现：Each 节点 has ID on hash ring。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build Chord DHT: 节点 on ring, finger tables用于routing. Achieve O(日志 n) lookups in P2P 网络.

## 概念说明

### Chord DHT

Chord arranges 节点 on hash ring. Finger tables point to 节点 2^i ahead用于O(日志 n) hops. Used in P2P systems和some databases.

## 涉及概念

- `DHT`
- `Chord`
- `finger table`

## 实现提示

- Each 节点 has ID on hash ring
- Finger table用于O(日志 n) lookup
-处理节点 join/leave

## 测试用例

### 1. Hash key to ring

Verify 响应 contains type:chord_hash_ok，包含hash value between 0和2^6-1 (0-63). Hash should be consistent (same key always produces same hash).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chord_hash","msg_id":2,"key":"mykey","m":6}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"chord_hash_ok","in_reply_to":2,"msg_id":1,"hash":7}}
```

## 参考资料

- [Chord Paper](https://pdos.csail.mit.edu/papers/chord:sigcomm01/)：Chord: A Scalable P2P Lookup

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
