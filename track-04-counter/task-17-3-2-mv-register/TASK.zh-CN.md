# 实现多值寄存器

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-2-mv-register>

课程：4. 计数器：分布式状态与 CRDT
任务序号：12
短标题：MV-Register
难度：高级
子主题：更多 CRDT

## 中文导读

这道题让你实现多值寄存器（MV-Register），它通过保留所有并发写入的值作为"兄弟版本"来处理冲突，由客户端在读取时自行决定如何解决冲突。这正是 Amazon DynamoDB 和 Riak 采用的方案，体现了"永不拒绝写入，把冲突解决权交给应用层"的设计哲学。

## 题目说明

多值寄存器（MV-Register，Multi-Value Register）通过保留所有并发写入的值作为"兄弟版本（Siblings）"来处理并发写入冲突。冲突的解决交由客户端在读取时完成。

**工作原理**：
- 每个值都附带一个向量时钟（Vector Clock）
- `write("v1")` 在向量时钟 {A:1} 时写入 -> 存储 ("v1", {A:1})
- `write("v2")` 在向量时钟 {B:1} 时写入（与上一个并发）-> 存储 ("v2", {B:1})
- `read()` 返回 ["v1", "v2"]（两个兄弟版本，由客户端选择）
- `write("v3")` 在向量时钟 {A:1, B:1} 时写入（因果上在前两者之后）-> 替换前两者

这是 Amazon DynamoDB 和 Riak 采用的方案。它最大化了可用性（永远不会拒绝写入），代价是要求客户端自行处理冲突。

```json
Request:  {"type": "mv_write", "msg_id": 1, "key": "cart", "value": ["item1", "item2"]}
Response: {"type": "mv_write_ok", "in_reply_to": 1, "vclock": {"n1": 1}}

Request:  {"type": "mv_read", "msg_id": 2, "key": "cart"}
Response: {"type": "mv_read_ok", "in_reply_to": 2, "values": [{"value": ["item1", "item2"], "vclock": {"n1": 1}}, {"value": ["item1", "item3"], "vclock": {"n2": 1}}]}
```

## 涉及概念

- `MV-Register`
- `concurrent writes`
- `sibling values`
- `vector clock`
- `conflict resolution`

## 实现提示

- 每次写入都附带向量时钟时间戳
- 并发写入会产生多个兄弟版本（类似 DynamoDB 的做法）
- 读取时返回所有并发的值，由客户端来解决冲突
- 因果上在另一个写入之后的写入会替换它（不是并发的）
- 合并：保留来自并发写入的所有值，丢弃被因果支配的值

## 测试用例

### 1. 写入并读取单个值

验证 mv_read_ok 的 values 应恰好包含一个值为 "v1" 的条目。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":3,"key":"k"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 并发写入产生兄弟版本

验证 mv_read_ok 的 values 应包含两个兄弟版本："v1" 和 "v2"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"n2","dest":"n1","body":{"type":"mv_merge","msg_id":3,"key":"k","entry":{"value":"v2","vclock":{"n2":1}}}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":4,"key":"k"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [DynamoDB Conflict Resolution](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：DeCandia 等人的论文，介绍 Amazon Dynamo 高可用键值存储

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
