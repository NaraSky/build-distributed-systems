# 实现向量时钟

英文标题：Implement Vector Clocks
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-3-vector-clock>

课程：2. 标识符：分布式唯一 ID
任务序号：13
短标题：向量时钟
难度：高级
子主题：Logical Clocks as IDs

## 中文导读

向量时钟（Vector Clock）弥补了 Lamport 时钟无法检测并发事件的缺陷。每个节点维护一个包含所有节点计数器的向量，通过比较向量就能准确判断两个事件之间是因果关系还是并发关系。本题要求你实现向量时钟的核心操作：本地递增和接收合并。

## 题目说明

向量时钟解决了 Lamport 时钟的局限性：它能够检测**并发事件**。每个节点维护一个包含 N 个计数器的向量（每个节点对应一个计数器）。更新规则如下：

1. **本地事件**或**发送消息**时：将向量中自己对应的计数器加 1
2. **接收消息**时：对本地向量和收到的向量做逐元素取最大值，然后将自己对应的计数器加 1

如何判断两个事件是否并发？如果两个向量谁也不能"支配"对方，它们就是并发的。所谓"支配"是指一个向量的每个分量都大于等于另一个向量的对应分量。举个例子：向量 A 的某个分量比 B 大，但 B 的另一个分量又比 A 大，那么 A 和 B 就是并发关系。

实现 `vc_tick` 处理器（本地事件触发）：
```json
请求:  {"type": "vc_tick", "msg_id": 1}
响应: {"type": "vc_tick_ok", "in_reply_to": 1, "vector": {"n1": 1, "n2": 0}}
```

实现 `vc_receive` 处理器（接收并合并远程向量）：
```json
请求:  {"type": "vc_receive", "msg_id": 2, "vector": {"n1": 0, "n2": 3}}
响应: {"type": "vc_receive_ok", "in_reply_to": 2, "vector": {"n1": 2, "n2": 3}}
```

## 涉及概念

- `vector clock`
- `causality tracking`
- `element-wise max`
- `concurrent detection`

## 实现提示

- 每个节点维护一个长度为 N 的计数器向量，集群中每个节点对应一个位置
- 本地事件或发送消息时：将自己那个位置的计数器加 1
- 接收消息时：对向量逐元素取最大值，然后将自己那个位置的计数器加 1
- 向量时钟可以区分并发事件和因果事件
- 初始化时，将向量中所有已知节点的计数器设为 0

## 测试用例

### 1. 本地事件递增自身计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
```

### 2. 合并操作先逐元素取最大值，再递增自身计数器

执行一次 tick 后，本地向量为 n1=1, n2=0。收到远程向量 {n1:0, n2:5} 后，先逐元素取最大值得到 {n1:1, n2:5}，再将自身计数器加 1，最终得到 {n1:2, n2:5}。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"vc_receive","msg_id":3,"vector":{"n1":0,"n2":5}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "vc_receive_ok", "vector": {"n1": 2, "n2": 5}, "in_reply_to": 3, "msg_id": 2}}
```

## 参考资料

- [Vector Clocks Revisited](https://riak.com/posts/technical/vector-clocks-revisited/)：Riak 文档中关于向量时钟实际应用的讲解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
