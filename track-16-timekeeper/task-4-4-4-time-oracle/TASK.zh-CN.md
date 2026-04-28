# 构建 a Time Oracle 服务，包含Failover

英文标题：Build a Time Oracle Service，包含Failover
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-4-time-oracle>

课程：16. 时间守卫：逻辑时钟
任务序号：19
短标题：Time Oracle
难度：advanced
子主题：混合逻辑 Clocks

## 中文导读

本题要求你完成 `构建 a Time Oracle 服务，包含Failover`。

重点关注：`time oracle`、`centralized clock`、`failover`、`backup oracle`、`single point of failure`。

建议先按提示逐步实现：The oracle maintains an HLC和issues globally consistent timestamps。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a centralized time oracle service that 节点 query用于globally consistent HLC timestamps. This avoids the problem of unbounded 时钟 skew between 节点.

Architecture:
- **Primary oracle**: maintains an HLC, issues timestamps on 请求
- **Backup oracle**: monitors the primary, takes over on 故障
- **节点**: query the oracle instead of使用local clocks

故障 mode: if primary crashes after issuing timestamp T but before the backup knows, the backup must start，包含T + safety_margin to avoid issuing duplicate timestamps.

Implement handlers:

```JSON
请求:  {"type": "oracle_get_time", "msg_id": 1}
响应: {"type": "oracle_get_time_ok", "in_reply_to": 1, "pt": 1000, "c": 0, "oracle": "primary"}

请求:  {"type": "oracle_fail_primary", "msg_id": 2}
响应: {"type": "oracle_fail_primary_ok", "in_reply_to": 2, "new_oracle": "backup", "safety_margin_ms": 100}

请求:  {"type": "oracle_get_time", "msg_id": 3}
响应: {"type": "oracle_get_time_ok", "in_reply_to": 3, "pt": 1100, "c": 0, "oracle": "backup"}

请求:  {"type": "oracle_status", "msg_id": 4}
响应: {"type": "oracle_status_ok", "in_reply_to": 4, "primary_alive": false, "active_oracle": "backup", "timestamps_issued": 2}
```

## 涉及概念

- `time oracle`
- `centralized clock`
- `failover`
- `backup oracle`
- `single point of failure`

## 实现提示

- The oracle maintains an HLC和issues globally consistent timestamps
- 节点 query the oracle instead of使用their own clocks用于ordering
- If the primary oracle crashes, the backup takes over，包含a higher 计数器
- The backup oracle must start，包含a timestamp guaranteed to be higher than any issued by the primary
- Use a lease mechanism: the oracle is valid only while its lease is active

## 测试用例

### 1. Primary oracle issues timestamps

Two oracle_get_time_ok responses from primary oracle. Second timestamp must be strictly greater than first.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Failover to backup oracle

After oracle_fail_primary, oracle_get_time_ok should show oracle: backup和pt >= last_primary_pt + safety_margin.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_fail_primary","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TiDB - Timestamp Oracle Design](https://docs.pingcap.com/tidb/stable/tidb-architecture)：How TiDB uses a centralized timestamp oracle (TSO)用于事务 ordering

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
