# 实现 a Consistent Hash Ring

英文标题：Implement a Consistent Hash Ring
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-1-hash-ring>

课程：8. 分片器：水平扩展与数据迁移
任务序号：6
短标题：Hash Ring
难度：intermediate
子主题：Consistent Hashing

## 中文导读

本题要求你完成 `实现 a Consistent Hash Ring`。

重点关注：`consistent hashing`、`hash ring`、`key ownership`、`clockwise lookup`、`minimal disruption`。

建议先按提示逐步实现：Place 节点 at positions hash(node_id) % 2^32 on a circular ring。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Consistent hashing places 节点和keys on a circular ring, minimizing key redistribution when 节点 join or leave. Unlike modulo hashing (`hash(key) % N`), adding a 节点 only moves ~1/N of keys.

**Hash ring construction**:
1. For each 节点, compute `position = hash(node_id) % 2^32`
2. Place 节点 on a circle of size 2^32

**Key lookup**:
1. Compute `position = hash(key) % 2^32`
2. Walk clockwise from that position until you find a 节点
3. That 节点 owns the key

**Key redistribution on 节点 join**: only keys between the new 节点和its 计数器-clockwise neighbor need to move. All other keys stay in place.

```JSON
请求:  {"type": "ring_lookup", "msg_id": 1, "key": "user:42"}
响应: {"type": "ring_lookup_ok", "in_reply_to": 1, "key": "user:42", "节点": "n2", "position": 1048576}
```

## 涉及概念

- `consistent hashing`
- `hash ring`
- `key ownership`
- `clockwise lookup`
- `minimal disruption`

## 实现提示

- Place 节点 at positions hash(node_id) % 2^32 on a circular ring
- A key is owned by the first 节点 clockwise from hash(key) % 2^32
- When a 节点 joins, only keys between the new 节点和its predecessor migrate
- When a 节点 leaves, only its keys move to its successor
- Compare，包含modulo hashing: adding a 节点 remaps ~1/N keys vs. nearly all keys

## 测试用例

### 1. Key maps to nearest clockwise node

ring_lookup_ok should return a valid 节点 from the ring.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Same key always maps to same node

Both lookups should return the same 节点.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"k1"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)：Wikipedia article on consistent hashing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
