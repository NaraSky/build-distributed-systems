# 实现块服务器的负载均衡

英文标题：Implement Chunk Server Load Balancing
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-3-load-balancing>

课程：20. 文件系统：容错与再平衡
任务序号：8
短标题：Load Balancing
难度：高级
子主题：Fault Tolerance and Rebalancing

## 中文导读

这道题要求你实现数据块在服务器间的负载均衡。随着时间推移，数据块的分布会变得不均匀：新加入的服务器上没有数据，老服务器快被塞满。负载均衡就是在后台把数据块从"太满"的服务器搬到"太闲"的服务器上，让整个集群的磁盘使用率趋于均匀。

## 题目说明

随着时间推移，数据块的分布会变得不均匀：新服务器刚加入时是空的，老服务器逐渐填满，有些服务器接收了更多的写入。负载均衡通过迁移数据块来均衡各服务器的使用率。

再平衡算法：
1. 定期计算所有服务器的平均磁盘使用率
2. 如果某台服务器的使用率超过平均值 +20%，则为"过载"；低于平均值 -20%，则为"轻载"
3. 对于每台过载服务器，选择一些数据块迁移到轻载服务器上
4. 迁移过程：将数据块从源服务器复制到目标服务器，更新主节点元数据，然后从源服务器删除
5. 以后台进程方式运行，并限制传输速率，避免占满网络带宽

```json
Request:  {"type": "rebalance_check", "msg_id": 1}
Response: {"type": "rebalance_check_ok", "in_reply_to": 1, "average_utilization_pct": 50, "overloaded": [{"server": "cs1", "utilization_pct": 78}], "underloaded": [{"server": "cs4", "utilization_pct": 15}]}

Request:  {"type": "rebalance_execute", "msg_id": 2, "moves": [{"chunk": "ch_010", "from": "cs1", "to": "cs4"}]}
Response: {"type": "rebalance_execute_ok", "in_reply_to": 2, "moved": 1, "bytes_transferred": 67108864}
```

## 涉及概念

- `load balancing`
- `chunk migration`
- `disk utilization`
- `rebalancing threshold`

## 实现提示

- 监控每台服务器的磁盘使用率；如果不均衡程度超过 20%，触发再平衡
- 将数据块从过载服务器迁移到轻载服务器
- 再平衡是后台操作，不应影响正在进行的读写
- 迁移数据块后，更新主节点的元数据并通知相关服务器
- 优先迁移访问频率低的数据块，以减少对业务的影响

## 测试用例

### 1. 检查并发现过载和轻载服务器

rebalance_check_ok 应当包含 average_utilization_pct、overloaded 和 underloaded 数组。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance_check","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 执行再平衡迁移数据块

rebalance_execute_ok 应当显示 moved: 1 和 bytes_transferred > 0。

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

- [HDFS Balancer](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#Balancer)：HDFS 的均衡工具，用于在 DataNode 之间重新分配数据块

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
