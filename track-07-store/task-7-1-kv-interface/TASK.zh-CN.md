# 实现 键值 Interface

英文标题：Implement Key-Value Interface
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-1-kv-interface>

课程：7. 存储：线性一致 KV Store
任务序号：1
短标题：KV Interface
难度：intermediate
子主题：Linearizable 键值 存储

## 中文导读

本题要求你完成 `实现 键值 Interface`。

重点关注：`key-value`、`API`、`operations`。

建议先按提示逐步实现：Support get, put, cas operations。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the key-value store interface on top of Raft:

1. GET(key) - Return current value or null
2. PUT(key, value) - Set key to value
3. CAS(key, expected, new) - Compare-and-swap

Each write operation:
1. Leader receives 请求
2. Append to Raft 日志
3. Wait用于commitment
4. Apply to state machine
5. Return result to 客户端

## 概念说明

### Building on Consensus

Raft provides ordered, replicated 日志. We build a KV store by interpreting 日志 entries as operations. All 节点 apply the same operations in order, producing the same state.

### Maelstrom KV Workloads

Maelstrom tests lin-kv (线性一致 KV)和lww-kv (last-write-wins). 线性一致 requires waiting用于Raft commit. LWW can accept local writes immediately.

## 涉及概念

- `key-value`
- `API`
- `operations`

## 实现提示

- Support get, put, cas operations
- Each operation becomes a 日志 entry
- Wait用于commit before responding

## 测试用例

### 1. Put和get key

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"write_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":1}}
```

## 参考资料

- [Maelstrom KV](https://fly.io/dist-sys/6a/)：Fly.io lin-kv challenge

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
