# 实现 Chunk Server Load Balancing

英文标题：Implement Chunk Server Load Balancing
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-3-load-balancing>

课程：20. 文件系统：分布式文件存储
任务序号：8
短标题：Load Balancing
难度：advanced
子主题：Fault Tolerance和Rebalancing

## 中文导读

本题要求你完成 `实现 Chunk Server Load Balancing`。

重点关注：`load balancing`、`chunk migration`、`disk utilization`、`rebalancing threshold`。

建议先按提示逐步实现：Monitor each 服务端 disk usage; if imbalance exceeds 20%, trigger rebalancing。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Over time, chunk distribution becomes uneven: new servers start empty, old servers fill up,和some receive more writes. Load balancing moves chunks to equalize utilization.

Rebalancing algorithm:
1. Periodically compute the average disk utilization across all servers
2. If any 服务端 exceeds average + 20%, it is overloaded; if below average - 20%, it is underloaded
3. For each overloaded 服务端, select chunks to migrate to underloaded servers
4. Migration: copy chunk from source to target, update master 元数据, delete from source
5. Run as a background process，包含rate limiting to avoid saturating the 网络

```JSON
请求:  {"type": "rebalance_check", "msg_id": 1}
响应: {"type": "rebalance_check_ok", "in_reply_to": 1, "average_utilization_pct": 50, "overloaded": [{"服务端": "cs1", "utilization_pct": 78}], "underloaded": [{"服务端": "cs4", "utilization_pct": 15}]}

请求:  {"type": "rebalance_execute", "msg_id": 2, "moves": [{"chunk": "ch_010", "from": "cs1", "to": "cs4"}]}
响应: {"type": "rebalance_execute_ok", "in_reply_to": 2, "moved": 1, "bytes_transferred": 67108864}
```

## 涉及概念

- `load balancing`
- `chunk migration`
- `disk utilization`
- `rebalancing threshold`

## 实现提示

- Monitor each 服务端 disk usage; if imbalance exceeds 20%, trigger rebalancing
- Move chunks from overloaded servers to underloaded ones
- Rebalancing is a background operation — do not disrupt active reads/writes
- After moving a chunk, update the master 元数据和notify affected servers
- Prefer moving chunks that are infrequently accessed to minimize disruption

## 测试用例

### 1. Check identifies overloaded和underloaded servers

rebalance_check_ok should show average_utilization_pct, overloaded,和underloaded arrays.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance_check","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Execute rebalance moves chunks

rebalance_execute_ok should show moved: 1和bytes_transferred > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance_execute","msg_id":2,"moves":[{"chunk":"ch_010","from":"cs1","to":"cs4"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [HDFS Balancer](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#Balancer)：HDFS balancer tool用于redistributing blocks across DataNodes

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
