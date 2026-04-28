# 实现有界过期的跟随者读

英文标题：Add Follower Reads with Bounded Staleness
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-3-follower-reads>

课程：7. 存储：线性一致键值存储
任务序号：8
短标题：Follower Reads
难度：高级
子主题：读优化

## 中文导读

这道题要求你实现跟随者读（Follower Reads），允许客户端从跟随者节点读取数据，前提是客户端能接受一定程度的数据过期。这种方案可以将读负载分散到集群中的所有副本上，读吞吐量随集群规模线性增长，非常适合读多写少的场景。

## 题目说明

实现带有过期时间上界的跟随者读。客户端可以选择从任意跟随者读取数据，只要能接受数据最多过期 T 秒即可。这样读吞吐量可以随集群节点数线性扩展。

```json
Request:  {"type": "follower_read", "msg_id": 1, "key": "x", "max_staleness_ms": 5000}
Response: {"type": "follower_read_ok", "in_reply_to": 1, "value": "42", "actual_staleness_ms": 200, "served_by": "n2", "linearizable": false}

Request:  {"type": "follower_read", "msg_id": 2, "key": "x", "max_staleness_ms": 0}
Response: {"type": "follower_read_ok", "in_reply_to": 2, "value": "42", "served_by": "n1", "linearizable": true, "reason": "redirected_to_leader"}
```

## 涉及概念

- `follower reads`
- `bounded staleness`
- `read scalability`
- `consistency tradeoff`

## 实现提示

- 客户端可以选择从跟随者读取数据，前提是能接受最多 T 秒的数据过期
- 跟随者跟踪自己已应用到的日志索引，只在数据足够新鲜时才处理读请求
- 这样读负载可以分散到所有副本上，而不只是集中在领导者
- 过期时间上界可以按请求粒度配置
- 对比延迟：跟随者读避免了领导者成为瓶颈

## 测试用例

### 1. 在过期时间范围内从跟随者读取

验证 follower_read_ok 中 actual_staleness_ms 不超过 5000，且 linearizable 为 false。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 零过期容忍度时重定向到领导者

当 max_staleness_ms 为 0 时，读请求应该由领导者处理，且 linearizable 为 true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CockroachDB Follower Reads](https://www.cockroachlabs.com/docs/stable/follower-reads.html)：CockroachDB 如何在地理分布式系统中实现跟随者读

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
