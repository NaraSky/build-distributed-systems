# 构建冲突检测键值存储

英文标题：Build a Conflict-Detecting Key-Value Store
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-5-conflict-kv>

课程：16. 时间守卫：逻辑时钟
任务序号：15
短标题：冲突键值存储
难度：高级
子主题：向量时钟

## 中文导读

本题要求你利用向量时钟来检测键值存储中的写冲突。当两个节点同时写入同一个键，且双方互不知道对方的写入时，就产生了并发冲突。这道题模拟了 Amazon DynamoDB 的做法：把冲突的多个值都保留下来（称为"兄弟值"），交给客户端来决定如何合并。

## 题目说明

使用向量时钟来检测键值存储中的写-写冲突。当两个节点并发地写入同一个键时（两次写入之间没有因果关系），存储会把这两个值都保留下来，称为**兄弟值（siblings）**，这与 Amazon DynamoDB 的做法类似。

冲突判断规则：
- 如果写入的向量时钟支配（dominate）已存储的向量时钟：直接覆盖
- 如果已存储的向量时钟支配写入的向量时钟：拒绝（这是过时的写入）
- 如果两者互不支配（并发）：将两个值都保存为兄弟值

请实现以下处理器：

```json
Request:  {"type": "kv_put", "msg_id": 1, "key": "user:1", "value": "Alice", "clock": [1, 0]}
Response: {"type": "kv_put_ok", "in_reply_to": 1, "status": "written"}

Request:  {"type": "kv_put", "msg_id": 2, "key": "user:1", "value": "Bob", "clock": [0, 1]}
Response: {"type": "kv_put_ok", "in_reply_to": 2, "status": "conflict", "siblings": 2}

Request:  {"type": "kv_get", "msg_id": 3, "key": "user:1"}
Response: {"type": "kv_get_ok", "in_reply_to": 3, "values": [
    {"value": "Alice", "clock": [1, 0]},
    {"value": "Bob", "clock": [0, 1]}
]}

Request:  {"type": "kv_resolve", "msg_id": 4, "key": "user:1", "value": "Alice+Bob", "clock": [1, 1]}
Response: {"type": "kv_resolve_ok", "in_reply_to": 4, "status": "resolved"}
```

## 涉及概念

- `conflict detection`
- `write-write conflict`
- `multi-value register`
- `DynamoDB style`

## 实现提示

- 每个键存储一个值及其对应的向量时钟
- 写入时，将传入的向量时钟与已存储的向量时钟进行比较
- 如果传入的时钟支配已存储的时钟，则覆盖写入（无冲突）
- 如果两者互不支配，则将两个值都保存为兄弟值（写-写冲突）
- 读取时，返回所有兄弟值，让客户端自行解决冲突

## 测试用例

### 1. 向空键写入

`kv_get_ok` 应返回单个值 "hello"，时钟为 [1, 0]。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"hello","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

### 2. 并发写入产生兄弟值

第二次写入应返回 status 为 "conflict"，siblings 为 2。读取应返回 2 个值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"v1","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":3,"key":"x","value":"v2","clock":[0,1]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":4,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

## 参考资料

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：Amazon Dynamo 的原始论文，描述了利用向量时钟进行冲突检测的方法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
