# 实现 Master Failover，包含Shadow Master

英文标题：Implement Master Failover，包含Shadow Master
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-4-master-failover>

课程：20. 文件系统：分布式文件存储
任务序号：9
短标题：Master Failover
难度：advanced
子主题：Fault Tolerance和Rebalancing

## 中文导读

本题要求你完成 `实现 Master Failover，包含Shadow Master`。

重点关注：`master failover`、`shadow master`、`WAL replay`、`hot standby`、`failover time`。

建议先按提示逐步实现：A shadow master replays the primary WAL periodically to stay nearly up-to-date。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The master is a single point of 故障. A shadow master mitigates this by continuously replaying the primary's WAL, staying nearly synchronized.

Failover process:
1. **Normal operation**: primary master handles all requests; shadow replays WAL entries from a shared 存储
2. **故障 detection**: if the primary misses heartbeats用于10 seconds, the shadow initiates takeover
3. **WAL catchup**: shadow replays any remaining WAL entries not yet processed
4. **Promote**: shadow becomes the new primary, starts accepting requests
5. **Redirect**: chunk servers和clients are notified to use the new master

```JSON
请求:  {"type": "shadow_status", "msg_id": 1}
响应: {"type": "shadow_status_ok", "in_reply_to": 1, "primary": "master1", "shadow": "master2", "wal_lag_entries": 5, "wal_lag_ms": 200}

请求:  {"type": "trigger_failover", "msg_id": 2, "failed_master": "master1"}
响应: {"type": "trigger_failover_ok", "in_reply_to": 2, "new_primary": "master2", "wal_entries_replayed": 5, "failover_time_ms": 450}
```

## 涉及概念

- `master failover`
- `shadow master`
- `WAL replay`
- `hot standby`
- `failover time`

## 实现提示

- A shadow master replays the primary WAL periodically to stay nearly up-to-date
- On primary 故障, the shadow takes over，包含minimal data loss (only recent WAL entries)
- The shadow cannot serve queries while the primary is alive — it is a hot standby
- Failover time = time to detect 故障 + time to replay remaining WAL entries
- After failover, chunk servers redirect heartbeats to the new master

## 测试用例

### 1. Shadow status shows WAL lag

shadow_status_ok should show primary, shadow,和wal_lag_entries.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"shadow_status","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Failover promotes shadow

trigger_failover_ok should have new_primary different from failed_master.

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

- [GFS Master Replication](https://research.google/pubs/pub51/)：GFS paper section on master 复制和shadow masters

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
