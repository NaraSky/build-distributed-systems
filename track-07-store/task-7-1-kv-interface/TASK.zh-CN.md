# 实现键值存储接口

英文标题：Implement Key-Value Interface
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-1-kv-interface>

课程：7. 存储：线性一致键值存储
任务序号：1
短标题：KV Interface
难度：进阶
子主题：线性一致键值存储

## 中文导读

这道题要求你在 Raft 共识层之上实现一个键值存储（Key-Value Store）的基本接口，支持读取、写入和比较并交换三种操作。这是把底层共识协议变成可用存储服务的关键一步，也是后续所有存储相关任务的基础。

## 题目说明

在 Raft 之上实现键值存储接口，需要支持以下三种操作：

1. GET(key) - 返回键的当前值，如果不存在则返回 null
2. PUT(key, value) - 将键设置为指定值
3. CAS(key, expected, new) - 比较并交换（Compare-and-Swap），仅当键的当前值等于 expected 时才更新为 new

每个写操作的处理流程如下：
1. 领导者（Leader）接收客户端请求
2. 将操作追加到 Raft 日志
3. 等待日志条目被提交（即多数节点确认）
4. 将操作应用到状态机
5. 将结果返回给客户端

## 概念说明

### 在共识之上构建存储

Raft 提供了有序的、可复制的日志。我们把日志中的每条记录解释为一个操作，就能在此基础上构建键值存储。由于所有节点（Node）按相同顺序执行相同的操作，最终它们会得到完全一致的状态。这就好比多个人按照同一份食谱、同一顺序做菜，最后做出来的菜一定是一样的。

### Maelstrom 键值工作负载

Maelstrom 测试框架提供两种键值工作负载：lin-kv（线性一致键值存储）和 lww-kv（最后写入者胜出）。线性一致模式要求写操作必须等待 Raft 日志提交后才能返回；而最后写入者胜出模式可以在本地直接接受写入。

## 涉及概念

- `key-value`
- `API`
- `operations`

## 实现提示

- 实现 get、put、cas 三种操作
- 每个操作都对应一条日志条目
- 必须等待日志提交后才能给客户端返回响应

## 测试用例

### 1. 写入并读取键值

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

- [Maelstrom KV](https://fly.io/dist-sys/6a/)：Fly.io 的线性一致键值存储挑战

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
