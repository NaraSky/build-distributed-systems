# 实现基于影子主节点的主节点故障切换

英文标题：Implement Master Failover with Shadow Master
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-4-master-failover>

课程：20. 文件系统：容错与再平衡
任务序号：9
短标题：Master Failover
难度：高级
子主题：Fault Tolerance and Rebalancing

## 中文导读

这道题要求你实现主节点的故障切换机制。主节点是整个系统的单点故障：它一旦宕机，整个文件系统就瘫痪了。影子主节点（Shadow Master）通过持续回放主节点的预写日志来保持近乎同步的状态，一旦主节点故障就能快速接管。

## 题目说明

主节点是系统的单点故障。影子主节点通过持续回放主主节点的预写日志（WAL）来缓解这个问题，使其保持近乎同步的状态。

故障切换流程：
1. **正常运行**：主主节点处理所有请求；影子主节点从共享存储中回放 WAL 条目
2. **故障检测**：如果主主节点 10 秒未发送心跳，影子主节点启动接管流程
3. **WAL 追赶**：影子主节点回放所有尚未处理的 WAL 条目
4. **提升**：影子主节点成为新的主主节点，开始接受请求
5. **重定向**：通知块服务器和客户端使用新的主节点

```json
Request:  {"type": "shadow_status", "msg_id": 1}
Response: {"type": "shadow_status_ok", "in_reply_to": 1, "primary": "master1", "shadow": "master2", "wal_lag_entries": 5, "wal_lag_ms": 200}

Request:  {"type": "trigger_failover", "msg_id": 2, "failed_master": "master1"}
Response: {"type": "trigger_failover_ok", "in_reply_to": 2, "new_primary": "master2", "wal_entries_replayed": 5, "failover_time_ms": 450}
```

## 涉及概念

- `master failover`
- `shadow master`
- `WAL replay`
- `hot standby`
- `failover time`

## 实现提示

- 影子主节点定期回放主主节点的预写日志，保持近乎最新的状态
- 当主主节点故障时，影子主节点接管，只会丢失最近的少量 WAL 条目
- 在主主节点存活期间，影子主节点不能对外提供查询服务，它是一个热备（Hot Standby）
- 故障切换时间 = 故障检测时间 + 回放剩余 WAL 条目的时间
- 故障切换完成后，块服务器将心跳重定向到新的主节点

## 测试用例

### 1. 影子主节点状态显示 WAL 延迟

shadow_status_ok 应当包含 primary、shadow 和 wal_lag_entries。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"shadow_status","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 故障切换提升影子主节点

trigger_failover_ok 中的 new_primary 应当与 failed_master 不同。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"trigger_failover","msg_id":2,"failed_master":"n1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Master Replication](https://research.google/pubs/pub51/)：GFS 论文中关于主节点复制和影子主节点的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
